import numpy as np

from pymop.problem import Problem


class Ackley(Problem):

    def __init__(self, n_var=10, C1=20, C2=.2, C3=2 * np.pi):
        self.n_var = n_var
        self.c1 = C1
        self.c2 = C2
        self.c3 = C3
        self.n_constr = 0
        self.n_obj = 1
        self.func = self._evaluate
        self.xl = -32 * np.ones(self.n_var)
        self.xu = 32 * np.ones(self.n_var)

    def _evaluate(self, x, f, *args, **kwargs):
        part1 = -1. * self.c1 * np.exp(-1. * self.c2 * np.sqrt((1. / self.n_var) * np.sum(x * x, axis=1)))
        part2 = -1. * np.exp((1. / self.n_var) * np.sum(np.cos(self.c3 * x), axis=1))
        f[:, 0] = part1 + part2 + self.c1 + np.exp(1)

    def _calc_pareto_front(self):
        return np.zeros((1, 1))


