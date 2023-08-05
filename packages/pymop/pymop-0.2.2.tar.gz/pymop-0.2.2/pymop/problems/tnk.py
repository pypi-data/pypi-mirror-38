import numpy as np

from pymop import load_pareto_front_from_file
from pymop.problem import Problem


class TNK(Problem):
    def __init__(self):
        Problem.__init__(self)
        self.n_var = 2
        self.n_constr = 2
        self.n_obj = 2
        self.func = self._evaluate
        self.xl = np.array([0, 1e-30])
        self.xu = np.array([np.pi, np.pi])

    def _evaluate(self, x, f, g, *args, **kwargs):
        f[:, 0] = x[:, 0]
        f[:, 1] = x[:, 1]
        g[:, 0] = -(np.square(x[:, 0]) + np.square(x[:, 1]) - 1.0 - 0.1 * np.cos(16.0 * np.arctan(x[:, 0] / x[:, 1])))
        g[:, 1] = 2 * (np.square(x[:, 0] - 0.5) + np.square(x[:, 1] - 0.5)) - 1

    def _calc_pareto_front(self, *args, **kwargs):
        return load_pareto_front_from_file("tnk.pf")
