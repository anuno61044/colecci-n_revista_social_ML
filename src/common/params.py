from abc import ABC, abstractmethod

class Params(ABC):
    def __init__(self, params_domains : dict[str, list[int]]):
        self._params_domains = params_domains

    @abstractmethod
    def select_combinations(self) -> list[dict[str, int]]:
        pass

class ExhaustiveParams(Params):
    def select_combinations(self) -> list[dict[str, int]]:
        keys = list(self._params_domains.keys())
        combinations = []
        self._backtrack(keys, {}, combinations, 0)
        return combinations
    
    def _backtrack(
            self,
            keys : list[str],
            combination : dict[str, int],
            combinations : list[dict[str, int]],
            index : int
        ) -> None:

        if index >= len(keys):
            combinations.append(combination.copy())
            return

        key = keys[index]
        values = self._params_domains[key]
        
        for value in values:
            combination[key] = value
            self._backtrack(keys, combination, combinations, index+1)
            