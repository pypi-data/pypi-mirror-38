import numpy as np

from pymop.problem import Problem


class BNH(Problem):

    def __init__(self):
        Problem.__init__(self)
        self.n_var = 2
        self.n_constr = 2
        self.n_obj = 2
        self.func = self._evaluate
        self.xl = np.zeros(self.n_var)
        self.xu = np.array([5.0, 3.0])

    def _evaluate(self, x, f, g, *args, **kwargs):
        f[:, 0] = 4 * x[:, 0] ** 2 + 4 * x[:, 1] ** 2
        f[:, 1] = (x[:, 0] - 5) ** 2 + (x[:, 1] - 5) ** 2
        g[:, 0] = (1 / 25) * ((x[:, 0] - 5) ** 2 + x[:, 1] ** 2 - 25)
        g[:, 1] = -1 / 7.7 * ((x[:, 0] - 8) ** 2 + (x[:, 1] + 3) ** 2 - 7.7)

    def _calc_pareto_front(self, n_pareto_points):
        x1 = np.linspace(0, 5, n_pareto_points)
        x2 = np.copy(x1)
        x2[x1 >= 3] = 3
        return np.vstack((4 * np.square(x1) + 4 * np.square(x2), np.square(x1 - 5) + np.square(x2 - 5))).T






