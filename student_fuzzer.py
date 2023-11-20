from fuzzingbook import GreyboxFuzzer as gbf
from fuzzingbook import Coverage as cv
from fuzzingbook import MutationFuzzer as mf

from typing import List, Set, Any, Tuple, Dict, Union, Sequence
import numpy as np
import traceback
import numpy as np
import time
import random

from bug import entrypoint
from bug import get_initial_corpus

## You can re-implement the coverage class to change how
## the fuzzer tracks new behavior in the SUT

class MyCoverage(cv.Coverage):
    # result = np.array()
    # indice = np.array()
    dic = dict()
    def coverage(self) -> Set[cv.Location]:
        """The s et of executed lines, as (function_name, line_number) pairs"""
        return self._trace
    
        # n-grams
        # self.temp = tuple(set(self._trace))
        # if self.temp in self.dic:
        #     #print(123123)
        #     return self.dic[self.temp] 
        # self.result = np.array(self._trace)
        # #print(self.result[-10:])
        # self.result = self.result[::-1]
        # _, self.indice = np.unique(self.result, axis = 0,return_index=True)
        # self.indice.sort()
        # self.result = self.result[self.indice]
        # self.result = [tuple(item) for item in self.result]
        # self.dic[self.temp] = self.result[:4] if len(self.result) >= 4 else self.result
        # #print(self.dic[self.temp])
        # #(self.result[:3] if len(self.result) >= 3 else self.result,self.result[1:4] if len(self.result) >= 4 else self.result[-3:])
        # return self.result[:4] if len(self.result) >= 4 else self.result


## You can re-implement the runner class to change how
## the fuzzer tracks new behavior in the SUT

class MyFunctionCoverageRunner(mf.FunctionRunner):
    #previous_trace = set()
    
    def run_function(self, inp: str) -> Any:
        #print(2)
        with MyCoverage() as cov:
            #print(cov.coverage())
            try:
                result = super().run_function(inp)

            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc
        #print(cov.coverage())
        self._coverage = cov.coverage()
        return result

    def coverage(self) -> Set[cv.Location]:
        #print(3)
        # print(self._coverage)
        # result = set.union(set(self._coverage), self.previous_trace)
        # self.previous_trace = set(self._coverage)
        # print(result)
        return self._coverage


## You can re-implement the fuzzer class to change your
## fuzzer's overall structure

## The Mutator and Schedule classes can also be extended or
## replaced by you to create your own fuzzer!
class MyMutator(gbf.Mutator):
    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character,
            self.flip_two,
            self.flip_three,
            #self.arith
        ]

    def insert_random_character(self, s: str) -> str:
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]
    def delete_random_character(self, s: str) -> str:
        """Returns s with a random character deleted"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        return s[:pos] + s[pos + 1:]
    def flip_random_character(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]
    def flip_two(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)
        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 3 << random.randint(0, 5)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]
    def flip_three(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)
        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 7 << random.randint(0, 4)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]
    def arith(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)
        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        temp = ord(c) + random.randint(-35, 36)
        temp = min(max(32, temp), 126)
        new_c = chr(temp)
        return s[:pos] + new_c + s[pos + 1:]
    def mutate(self, inp: Any) -> Any:  # can be str or Seed (see below)
        """Return s with a random mutation applied. Can be overloaded in subclasses."""
        mutator = random.choice(self.mutators)
        return mutator(inp)

class DictMutator(gbf.Mutator):
    """Variant of `Mutator` inserting keywords from a dictionary"""

    def __init__(self, dictionary: Sequence[str]) -> None:
        """Constructor.
        `dictionary` - a list of strings that can be used as keywords
        """
        super().__init__()
        self.dictionary = dictionary
        self.mutators.append(self.insert_from_dictionary)

    def insert_from_dictionary(self, s: str) -> str:
        """Returns `s` with a keyword from the dictionary inserted"""
        pos = random.randint(0, len(s))
        random_keyword = random.choice(self.dictionary)
        return s[:pos] + random_keyword + s[pos:]
    
# When executed, this program should run your fuzzer for a very 
# large number of iterations. The benchmarking framework will cut 
# off the run after a maximum amount of time
#
# The `get_initial_corpus` and `entrypoint` functions will be provided
# by the benchmarking framework in a file called `bug.py` for each 
# benchmarking run. The framework will track whether or not the bug was
# found by your fuzzer -- no need to keep track of crashing inputs
if __name__ == "__main__":
    seed_inputs = get_initial_corpus()
    fast_schedule = gbf.AFLFastSchedule(5)
    line_runner = MyFunctionCoverageRunner(entrypoint)

    fast_fuzzer = gbf.CountingGreyboxFuzzer(seed_inputs, MyMutator(), fast_schedule)
    fast_fuzzer.runs(line_runner, trials=9999999)
