import yaml
import os
import subprocess
from collections import namedtuple

from .types.traditional import ProblemTraditional
from .languages import get_language

class ProblemException(BaseException):
    pass


class Problem:
    all_types = {
        "traditional": ProblemTraditional
    }

    def __init__(self, path=".", config=None):
        self.path = path
        config_file = os.path.join(self.path, "problem.yml")
        try:
            with open(config_file, 'r') as stream:
                try:
                    self.config = yaml.load(stream)
                except yaml.YAMLError:
                    raise
        except FileNotFoundError as e:
            raise ProblemException("File {file} doesn't exist, run `syzoj config` first".format(file=config_file)) from e

        self.cases = []
        cases = self.config["cases"]
        cases_global = self.config.get("cases-global", {})
        if isinstance(cases, int):
            self.cases = [ProblemCase(self, i, cases_global.copy()) for i in range(cases)]
        else:
            for index, config in enumerate(self.config["cases"]):
                merged_config = cases_global.copy()
                merged_config.update(config)
                self.cases.append(ProblemCase(self, index, merged_config))

        for case in self.cases:
            if not case.gen_input and not os.path.isfile(case.input_data):
                raise ProblemException("Input file %s for testcase %s doesn't exist" % (case.input_data, case.name))
            if not case.gen_answer and not os.path.isfile(case.answer_data):
                raise ProblemException("Answer file %s for testcase %s doesn't exist" % (case.answer_data, case.name))

        self.case_by_name = {}
        for index, case in enumerate(self.cases):
            self.case_by_name[case.name] = index

        self.subtasks = []
        if not "subtasks" in self.config:
            subtask_count = len(self.cases)
            subtask_score = 100. / subtask_count
            for index, case in enumerate(self.cases):
                config = {
                    "score": subtask_score,
                    "testcases": [case.name]
                }
                subtask = ProblemSubtask(self, index, config)
                self.subtasks.append(subtask)
        else:
            for index, config in enumerate(self.config["subtasks"]):
                subtask = ProblemSubtask(self, index, config)
                for case in subtask.testcases:
                    if not case in self.case_by_name:
                        raise ProblemException("Subtask %d: Test case with name %s does not exist" % (index, case))
                self.subtasks.append(subtask)

        self.assertions = []
        if "assertions" in self.config:
            for assertion in self.config["assertions"]:
                self.assertions.append(ProblemAssertion(self, assertion))

        self.build_config = ProblemBuild(self, self.config.get("build", {}))
        for case in self.cases:
            if case.gen_input and self.build_config.input_gen == None:
                raise ProblemException("Case %s requires input generation but input generator is not defined" % case.name)
            if case.gen_answer and self.build_config.answer_gen == None:
                raise ProblemException("Case %s requires answer generation but answer generator is not defined" % case.name)

        type_id = self.config.get("type", "traditional")
        if not type_id in Problem.all_types:
            raise ProblemException("Unsupported problem type %s" % type_id)
        self.type = Problem.all_types[type_id](self)

    
    def build(self, force=False):
        if self.build_config.input_gen != None:
            input_gen_path, _ = os.path.splitext(self.build_config.input_gen) 
            lang = get_language(self.build_config.input_gen)(self)
            if not os.path.isfile(input_gen_path) or os.path.getmtime(input_gen_path) < os.path.getmtime(self.build_config.input_gen):
                print("Compiling input generator")
                lang.compile(self.build_config.input_gen, input_gen_path)
                force = True

        if self.build_config.answer_gen != None:
            answer_gen_path, _ = os.path.splitext(self.build_config.answer_gen)
            lang = get_language(self.build_config.answer_gen)(self)
            if not os.path.isfile(answer_gen_path) or os.path.getmtime(input_gen_path) < os.path.getmtime(self.build_config.answer_gen):
                print("Compiling answer generator")
                lang.compile(self.build_config.answer_gen, answer_gen_path)
                force = True

        for case in self.cases:
            if case.gen_input and (force or not os.path.isfile(case.input_data)):
                print("Generating input for case %s" % case.name)
                args = lang.get_args(input_gen_path, *case.build_args)
                with open(case.input_data, "wb") as input_file:
                    subprocess.run(args, stdin=subprocess.DEVNULL, stdout=input_file, check=True)

            if case.gen_answer and (force or not os.path.isfile(case.answer_data)):
                print("Generating answer for case %s" % case.name)
                args = lang.get_args(answer_gen_path, *case.build_args)
                with open(case.input_data, "rb") as input_file:
                    with open(case.answer_data, "wb") as answer_file:
                        subprocess.run(args, stdin=input_file, stdout=answer_file, check=True)
    
    def test(self):
        success = True
        for i, assertion in enumerate(self.assertions):
            result = self.judge(assertion.prog, lazy=False)
            if not result.success:
                print("Assertion %d failed: compile failed" % i)
                success = False
            if assertion.score and assertion.score != result.score:
                print("Assertion %d failed: score mismatch" % i)
                success = False
            for subtask in assertion.subtasks:
                subtask_result = result.subtask_result[subtask["id"]]
                if "passed" in subtask:
                    passed = subtask_result.last_case == None
                    if passed != subtask["passed"]:
                        print("Assertion %d failed: subtask %d: passed mismatch" % (i, subtask["id"]))
                        success = False
                if "score" in subtask:
                    real_score = subtask_result.score * self.subtasks[subtask["id"]].score
                    if real_score != subtask["score"]:
                        print("Assertion %d failed: subtask %d: score mismatch, expected %f, got %f" % (i, subtask["id"], subtask["score"], real_score))
                        success = False
                if "last-message" in subtask:
                    last_case = result.subtask_result[subtask["id"]].last_case
                    if last_case == None:
                        print("Assertion %d failed: subtask %d: passed but last-message is specified" % (i, subtask["id"]))
                        success = False
                    else:
                        message = result.case_result[last_case].run_result.message
                        if message != subtask["last-message"]:
                            print("Assertion %d failed: subtask %d: last-message mismatch: expected %s, got %s" % (i, subtask["id"], subtask["last-message"], result.case_result[last_case].message))
                            success = False
            for case in assertion.testcases:
                result = result.case_result[case["name"]]
                if "score" in case:
                    if result.score != case.score:
                        print("Assertion %d failed: case %s: score mismatch, expected %f, got %f" % (i, case.name, result.score, case.score))
                        success = False
        return success

    def judge(self, source, lazy=True):
        session = self.type.judge_session(source)
        pre_judge_result = session.pre_judge()
        if pre_judge_result != None:
            return JudgeResult(success=False, score=0, message=pre_judge_result)

        case_result = {}
        subtask_result = []
        score_sum = 0.
        if not lazy:
            for case in self.cases:
                case_result[case.name] = session.do_judge(case)

        for i, subtask in enumerate(self.subtasks):
            print("Judging subtask %d" % i)
            score = 1.
            last_case = None

            for j in subtask.testcases:
                if j in case_result:
                    if lazy:
                        print("Skipping testcase %s because it is already judged" % j)
                else:
                    case = self.cases[self.case_by_name[j]]
                    case_result[j] = session.do_judge(case)

                result = case_result[j]
                if result.success:
                    score = min(score, result.score)
                    continue
                else:
                    score = 0.
                    last_case = j
                    break

            print("Subtask %d result: %s" % (i, score))
            subtask_result.append(SubtaskResult(score, last_case))
            score_sum += score * subtask.score

        session.post_judge()
        return JudgeResult(success=True, case_result=case_result, subtask_result=subtask_result, score=score_sum)

class ProblemCase:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = self.config.get("name", str(self.index + 1))
        self.input_data = os.path.join(self.problem.path, self.config.get("input-data", "data/{name}.in").format(name=self.name))
        self.answer_data = os.path.join(self.problem.path, self.config.get("answer-data", "data/{name}.out").format(name=self.name))
        self.gen = self.config.get("gen", False)
        self.gen_input = self.config.get("gen-input", self.gen)
        self.gen_answer = self.config.get("gen-answer", self.gen)
        if self.gen_input:
            self.build_args = list(map(lambda s: s.format(name=self.name), self.config.get("args", [])))
        
        self.time_limit = ProblemCase.parse_time_limit(self.config["time-limit"])
        self.memory_limit = ProblemCase.parse_memory_limit(self.config["memory-limit"])

    def parse_time_limit(val):
        if val.endswith("ms"):
            return float(val[:-2])
        elif val.endswith("us"):
            return float(val[:-2]) / 100
        elif val.endswith("s"):
            return float(val[:-1]) * 1000
        else:
            raise ProblemException("Invalid time limit: %s" % val)
    
    def parse_memory_limit(val):
        if val.endswith("KB"):
            return float(val[:-2])
        elif val.endswith("MB"):
            return float(val[:-2]) * 1024
        elif val.endswith("GB"):
            return float(val[:-2]) * 1048576

class ProblemSubtask:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = str(self.config.get("name", self.index + 1))
        self.testcases = list(map(str, self.config["testcases"]))
        self.score = self.config["score"]

class JudgeResult:
    def __init__(self, success=False, score=0, case_result=None, subtask_result=None, message=None):
        self.success = success
        self.score = score
        self.case_result = case_result
        self.subtask_result = subtask_result
        self.message = message
        
    def __repr__(self):
        return "JudgeResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class SubtaskResult:
    def __init__(self, score, last_case):
        self.score = score
        self.last_case = last_case
        
    def __repr__(self):
        return "SubtaskResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class ProblemAssertion:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        self.prog = self.config["prog"]
        self.score = self.config.get("score")
        self.subtasks = self.config.get("subtasks", [])
        self.testcases = self.config.get("testcases", [])

class ProblemBuild:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        if "input-gen" in self.config:
            self.input_gen = os.path.join(self.problem.path, self.config["input-gen"])
        else:
            self.input_gen = None
        if "answer-gen" in self.config:
            self.answer_gen = os.path.join(self.problem.path, self.config["answer-gen"])
        else:
            self.answer_gen = None
