from pymop import *

STR_TO_PROBLEM = {
    'ackley': Ackley,
    'bnh': BNH,
    'carside': Carside,
    'dtlz1': DTLZ1,
    'dtlz2': DTLZ2,
    'dtlz3': DTLZ3,
    'dtlz4': DTLZ4,
    'dtlz5': DTLZ5,
    'dtlz6': DTLZ6,
    'dtlz7': DTLZ7,
    'griewank': Griewank,
    'knp': Knapsack,
    'kursawe': Kursawe,
    'osy': OSY,
    'rastrigin': Rastrigin,
    'rosenbrock': Rosenbrock,
    'schwefel': Schwefel,
    'sphere': Sphere,
    'tnk': TNK,
    'truss2d': Truss2D,
    'welded_beam': WeldedBeam,
    'zakharov': Zakharov,
    'zdt1': ZDT1,
    'zdt2': ZDT2,
    'zdt3': ZDT3,
    'zdt4': ZDT4,
    'zdt6': ZDT6
}


def get_problem(name, *args, **kwargs):
    return STR_TO_PROBLEM[name.lower()](*args, **kwargs)


def get_problem_from_func(func, xl, xu, n_var=None, func_args={}):
    if xl is None or xu is None:
        raise Exception("Please provide lower and upper bounds for the problem.")
    if isinstance(xl, (int, float)):
        xl = xl * np.ones(n_var)
    if isinstance(xu, (int, float)):
        xu = xu * np.ones(n_var)

    # determine through a test evaluation details about the problem
    n_var = xl.shape[0]
    n_obj = -1
    n_constr = 0

    res = func(xl[None, :], **func_args)

    if isinstance(res, tuple):
        # if there are constraints it is a tuple of length two
        if len(res) > 1:
            n_constr = res[1].shape[1]
        n_obj = res[0].shape[1]
    else:
        n_obj = res.shape[1]

    class MyProblem(Problem):
        def __init__(self):
            Problem.__init__(self)
            self.n_var = n_var
            self.n_constr = n_constr
            self.n_obj = n_obj
            self.func = self._evaluate
            self.xl = xl
            self.xu = xu

        def _evaluate(self, x, f, g, *args, **kwargs):
            if g is None:
                f[:, :] = func(x, **func_args)
            else:
                f[:, :], g[:, :] = func(x, **func_args)

    return MyProblem()
