import cvxopt
import numpy as np

###


class Optimizer():
    def __cvxopt_formulation(self, points, classes, kernel):
        """
        Lagrangian Formulation \\
        `min L(w,b)` \\
        `max L(λ)` \\
        `L(w, b, λ) = 1/2 * ||w||^2 + ∑ λi * (yi * (w * xi + b) - 1)`

        Dual of Lagrangian Formulation \\
        `max F(λ)` \\
        `F(λ) = ∑ λi - 1/2 * (∑ ∑ λi * λj * yi * yj * xi * xj)`
        
        CVXOPT Formulation \\
        `min F(x)` \\
        `F(x) = 1/2 * (x.T * P * x) + (q.T * x)` \\
        `Gx ≤ h` \\
        `Ax = b`

        Our problem is to `maximize` the `F(λ)` (lagrangian dual-problem), but the
        library CVXOPT accepts a problem formulated as a `minimization` problem.
        In order to obtain a MIN problem, we start from the dual and we multiply
        by -1 the entire objective function `F(λ)`.

        Lagrangian Dual Problem as Minimization Problem \\
        `min -F(λ)` \\
        `-F(λ) = 1/2 * (∑ ∑ λi * λj * yi * yj * xi * xj) - ∑ λi`

        CVXOPT Formulation Applied \\
        `min -F(λ)` \\
        `-F(λ) = 1/2 * (λ.T * (X * Y) * λ) - (I.T * λ)` \\
        `(-1 * I * λi) ≤ 0` \\
        `∑ λi * yi = 0`

        CVXOPT Variables:
         - P = (X * Y)
         - q = -I.T
         - G = -I
         - h = 0 (vector)
         - A = Y
         - b = 0 (number)
        """

        ### number of Lagrangian multipliers parameters.
        N = classes.shape[0]

        # {cvxopt} Parameters Formulation
        P_raw = np.outer(classes, classes.T) * kernel
        q_raw = np.full(N, 1) * -1
        G_raw = np.identity(N) * -1
        h_raw = np.full(N, 0)
        A_raw = classes
        b_raw = .0

        ### {cvxopt} matrix shape compatibility (for moltiplication).
        A_raw = A_raw.reshape((1, N))
        ###  {cvxopt} array types compatibility.
        q_raw = q_raw.astype(np.double)
        G_raw = G_raw.astype(np.double)
        h_raw = h_raw.astype(np.double)

        ###  {cvxopt} casting required.
        P = cvxopt.matrix(P_raw)
        q = cvxopt.matrix(q_raw)
        G = cvxopt.matrix(G_raw)
        h = cvxopt.matrix(h_raw)
        A = cvxopt.matrix(A_raw)
        b = cvxopt.matrix(b_raw)

        return (P, q, G, h, A, b)

    #

    def initialize(self):
        cvxopt.solvers.options['show_progress'] = False

    def cvxopt_solve(self, points, classes, kernel):
        P, q, G, h, A, b = self.__cvxopt_formulation(points, classes, kernel)

        return cvxopt.solvers.qp(P, q, G, h, A, b)

    def scipy_solve(self, points, classes, kernel=None):
        pass