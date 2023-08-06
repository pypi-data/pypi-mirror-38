# -*- coding: utf-8 -*-
# Copyright (C) 2016-2018 by Cristina Garcia-Cardona <cgarciac@lanl.gov>
#                            Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. BSD 3-clause License.
# This file is part of the SPORCO package. Details of the copyright
# and user license can be found in the 'LICENSE.txt' file distributed
# with the package.

"""Base classes for FISTA algorithms"""

from __future__ import division
from __future__ import print_function
from builtins import range

import copy
import numpy as np

from sporco import cdict
from sporco import util
from sporco import common
import sporco.linalg as sl


__author__ = """Cristina Garcia-Cardona <cgarciac@lanl.gov>"""



class FISTA(common.IterativeSolver):
    r"""Base class for Fast Iterative Shrinkage/Thresholding algorithm
    (FISTA) algorithms :cite:`beck-2009-fast`.

    Solve optimisation problems of the form

    .. math::
       \mathrm{argmin}_{\mathbf{x}} \; f(\mathbf{x}) + g(\mathbf{x}) \;\;,

    where :math:`f, g` are convex functions and :math:`f` is smooth.

    This class is intended to be a base class of other classes that
    specialise to specific optimisation problems.

    After termination of the :meth:`solve` method, attribute
    :attr:`itstat` is a list of tuples representing statistics of each
    iteration. The default fields of the named tuple
    ``IterationStats`` are:

       ``Iter`` : Iteration number

       ``ObjFun`` : Objective function value

       ``FVal`` :  Value of smooth objective function component :math:`f`

       ``GVal`` : Value of objective function component :math:`g`

       ``F_Btrack`` : Value of objective function :math:`f + g`
       (see Sec. 2.2 of :cite:`beck-2009-fast`)

       ``Q_Btrack`` : Value of Quadratic approximation :math:`Q_L`
       (see Sec. 2.3 of :cite:`beck-2009-fast`)

       ``IterBtrack`` : Number of iterations in backtracking

       ``Rsdl`` : Residual

       ``L`` : Inverse of gradient step parameter

       ``Time`` : Cumulative run time
    """

    class Options(cdict.ConstrainedDict):
        r"""ADMM algorithm options.

        Options:

          ``FastSolve`` : Flag determining whether non-essential
          computation is skipped. When ``FastSolve`` is ``True`` and
          ``Verbose`` is ``False``, the functional value and related
          iteration statistics are not computed. If ``FastSolve`` is
          ``True`` residuals are also not calculated, in which case the
          residual-based stopping method is also disabled, with the
          number of iterations determined only by ``MaxMainIter``.

          ``Verbose`` : Flag determining whether iteration status is
          displayed.

          ``StatusHeader`` : Flag determining whether status header and
          separator are displayed.

          ``DataType`` : Specify data type for solution variables,
          e.g. ``np.float32``.

          ``X0`` : Initial value for X variable.

          ``Callback`` : Callback function to be called at the end of
          every iteration.

          ``MaxMainIter`` : Maximum main iterations.

          ``IterTimer`` : Label of the timer to use for iteration times.

          ``RelStopTol`` : Relative convergence tolerance for fixed point
          residual (see Sec. 4.3 of :cite:`liu-2018-first`).

          ``L`` : Inverse of gradient step parameter :math:`L`.

          ``AutoStop`` : Options for adaptive stoping strategy (fixed
          point residual, see Sec. 4.3 of :cite:`liu-2018-first`).

            ``Enabled`` : Flag determining whether the adaptive stopping
            relative parameter strategy is enabled.

            ``Tau0`` : numerator in adaptive criterion
            (:math:`\tau_0` in :cite:`liu-2018-first`).

          ``BackTrack`` : Options for adaptive L strategy (backtracking,
          see Sec. 4 of :cite:`beck-2009-fast`).

            ``Enabled`` : Flag determining whether adaptive inverse step
            size parameter strategy is enabled.

            ``Eta`` : Multiplier applied to L when updated
            (:math:`L` in :cite:`beck-2009-fast`).

            ``MaxIter`` : Maximum iterations of updating L when
            backtracking.
        """

        defaults = {'FastSolve': False, 'Verbose': False,
                    'StatusHeader': True, 'DataType': None,
                    'X0': None, 'Callback': None,
                    'MaxMainIter': 1000, 'IterTimer': 'solve',
                    'RelStopTol': 1e-3, 'L': None,
                    'BackTrack':
                    {'Enabled': False, 'Eta': 1.2, 'MaxIter': 100},
                    'AutoStop': {'Enabled': False, 'Tau0': 1e-2}}

        def __init__(self, opt=None):
            """
            Parameters
            ----------
            opt : dict or None, optional (default None)
              FISTA algorithm options
            """

            if opt is None:
                opt = {}
            cdict.ConstrainedDict.__init__(self, opt)



    fwiter = 4
    """Field width for iteration count display column"""
    fpothr = 2
    """Field precision for other display columns"""

    itstat_fields_objfn = ('ObjFun', 'FVal', 'GVal')
    """Fields in IterationStats associated with the objective function;
    see :meth:`eval_objfun`"""
    itstat_fields_alg = ('Rsdl', 'F_Btrack', 'Q_Btrack', 'IterBTrack', 'L')
    """Fields in IterationStats associated with the specific solver
    algorithm"""
    itstat_fields_extra = ()
    """Non-standard fields in IterationStats; see :meth:`itstat_extra`"""

    hdrtxt_objfn = ('Fnc', 'f', 'g')
    """Display column headers associated with the objective function;
    see :meth:`eval_objfun`"""
    hdrval_objfun = {'Fnc': 'ObjFun', 'f': 'FVal', 'g': 'GVal'}
    """Dictionary mapping display column headers in :attr:`hdrtxt_objfn`
    to IterationStats entries"""



    def __new__(cls, *args, **kwargs):
        """Create a FISTA object and start its initialisation timer."""

        instance = super(FISTA, cls).__new__(cls)
        instance.timer = util.Timer(['init', 'solve', 'solve_wo_func',
                                     'solve_wo_rsdl', 'solve_wo_btrack'])
        instance.timer.start('init')
        return instance



    def __init__(self, Nx, xshape, dtype, opt=None):
        r"""
        Parameters
        ----------
        Nx : int
          Size of variable :math:`\mathbf{x}` in objective function
        xshape : tuple of ints
          Shape of working variable X
        dtype : data-type
          Data type for working variables (overridden by 'DataType' option)
        opt : :class:`FISTA.Options` object
          Algorithm options
        """

        if opt is None:
            opt = FISTA.Options()
        if not isinstance(opt, FISTA.Options):
            raise TypeError("Parameter opt must be an instance of "
                            "FISTA.Options")

        self.opt = opt
        self.Nx = Nx

        # DataType option overrides data type inferred from __init__
        # parameters of derived class
        self.set_dtype(opt, dtype)

        # Initialise attributes representing step parameter and other
        # parameters
        self.set_attr('L', opt['L'], dval=1.0, dtype=self.dtype)
        self.set_attr('L_eta', opt['BackTrack', 'Eta'], dval=1.2,
                      dtype=self.dtype)
        self.set_attr('L_maxiter', opt['BackTrack', 'MaxIter'], dval=1.0,
                      dtype=self.dtype)
        self.t = 1.

        # If using adaptative stop criterion, set tau0 parameter
        if self.opt['AutoStop', 'Enabled']:
            self.tau0 = self.opt['AutoStop', 'Tau0']

        # Initialise working variable X
        if self.opt['X0'] is None:
            self.X = self.xinit(xshape)
        else:
            self.X = self.opt['X0'].astype(self.dtype, copy=True)

        # Default values for variables created only if BackTrack is enabled
        if self.opt['BackTrack', 'Enabled']:
            self.F = 0.
            self.Q = 0.
            self.iterBTrack = 0
        else:
            self.F = None
            self.Q = None
            self.iterBTrack = None

        self.Y = None

        self.itstat = []
        self.k = 0
        self.last_Lchange = self.k
        self.FBtprev = 1e15



    def xinit(self, xshape):
        """Return initialiser for working variable X."""

        return np.zeros(xshape, dtype=self.dtype)



    def solve(self):
        """Start (or re-start) optimisation. This method implements the
        framework for the iterations of a FISTA algorithm. There is
        sufficient flexibility in overriding the component methods that
        it calls that it is usually not necessary to override this method
        in derived clases.

        If option ``Verbose`` is ``True``, the progress of the
        optimisation is displayed at every iteration. At termination
        of this method, attribute :attr:`itstat` is a list of tuples
        representing statistics of each iteration, unless option
        ``FastSolve`` is ``True`` and option ``Verbose`` is ``False``.

        Attribute :attr:`timer` is an instance of :class:`.util.Timer`
        that provides the following labelled timers:

          ``init``: Time taken for object initialisation by
          :meth:`__init__`

          ``solve``: Total time taken by call(s) to :meth:`solve`

          ``solve_wo_func``: Total time taken by call(s) to
          :meth:`solve`, excluding time taken to compute functional
          value and related iteration statistics

          ``solve_wo_rsdl`` : Total time taken by call(s) to
          :meth:`solve`, excluding time taken to compute functional
          value and related iteration statistics as well as time take
          to compute residuals

          ``solve_wo_btrack`` : Total time taken by call(s) to
          :meth:`solve`, excluding time taken to compute functional
          value and related iteration statistics as well as time take
          to compute residuals and implemented ``BackTrack`` mechanism
        """

        # Open status display
        fmtstr, nsep = self.display_start()


        # Start solve timer
        self.timer.start(['solve', 'solve_wo_func', 'solve_wo_rsdl',
                          'solve_wo_btrack'])

        # Main optimisation iterations
        for self.k in range(self.k, self.k + self.opt['MaxMainIter']):

            # Update record of X from previous iteration
            self.store_prev()

            # Compute backtracking
            if self.opt['BackTrack', 'Enabled'] and self.k >= 0:
                self.timer.stop('solve_wo_btrack')
                # Computes proximal step and backtracking
                self.compute_backtracking()
                self.timer.start('solve_wo_btrack')
            else:
                # Compute just proximal step
                self.proximal_step()

            # Update by combining previous iterates
            self.combination_step()

            # Compute residuals and stopping thresholds
            self.timer.stop(['solve_wo_rsdl', 'solve_wo_btrack'])
            if not self.opt['FastSolve']:
                frcxd, adapt_tol = self.compute_residuals()
            self.timer.start('solve_wo_rsdl')

            # Compute and record other iteration statistics and
            # display iteration stats if Verbose option enabled
            self.timer.stop(['solve_wo_func', 'solve_wo_rsdl',
                             'solve_wo_btrack'])
            if not self.opt['FastSolve']:
                itst = self.iteration_stats(self.k, frcxd)
                self.itstat.append(itst)
                self.display_status(fmtstr, itst)
            self.timer.start(['solve_wo_func', 'solve_wo_rsdl',
                              'solve_wo_btrack'])


            # Call callback function if defined
            if self.opt['Callback'] is not None:
                if self.opt['Callback'](self):
                    break

            # Stop if residual-based stopping tolerances reached
            if not self.opt['FastSolve']:
                if frcxd < adapt_tol:
                    break


        # Increment iteration count
        self.k += 1

        # Record solve time
        self.timer.stop(['solve', 'solve_wo_func', 'solve_wo_rsdl',
                         'solve_wo_btrack'])

        # Print final separator string if Verbose option enabled
        self.display_end(nsep)

        return self.getmin()



    def getmin(self):
        """Get minimiser after optimisation."""

        return self.X



    def proximal_step(self, grad=None):
        """Compute proximal update (gradient descent + regularization)."""

        if grad is None:
            grad = self.eval_grad()

        V = self.Y - (1. / self.L) * grad

        self.X = self.eval_proxop(V)



    def combination_step(self):
        """Build next update by a smart combination of previous updates.
        """

        # Update t step
        tprv = self.t
        self.t = 0.5 * float(1. + np.sqrt(1. + 4. * tprv**2))

        # Update Y
        if not self.opt['FastSolve']:
            self.Yprv = self.Y.copy()
        self.Y = self.X + ((tprv - 1.) / self.t) * (self.X - self.Xprv)



    def compute_backtracking(self):
        """Estimate step size L by computing a linesearch that
        guarantees that F <= Q.
        """

        gradY = self.eval_grad()
        Ry = self.eval_R(self.Y)

        eta = self.L_eta
        maxiter = self.L_maxiter

        iterBTrack = 0
        linesearch = 1
        while linesearch and iterBTrack < maxiter:

            self.proximal_step(gradY)
            Rx = self.eval_Rx()

            F = 0.5 * np.linalg.norm(Rx.flatten(), 2)**2
            Dxy = self.eval_Dxy()
            Q = 0.5 * np.linalg.norm(Ry.flatten(), 2)**2 + \
                np.sum(Dxy * gradY) + \
                (self.L/2.) * np.linalg.norm(Dxy.flatten(), 2)**2

            if F <= Q:
                linesearch = 0
            else:
                self.L *= eta
                self.Lchange()
                iterBTrack += 1

        self.F = F
        self.Q = Q
        self.iterBTrack = iterBTrack



    def eval_grad(self):
        """Compute gradient.

        Overriding this method is required.
        """

        raise NotImplementedError()



    def eval_proxop(self, V):
        """Compute proximal operator of :math:`g`.

        Overriding this method is required.
        """

        raise NotImplementedError()



    def eval_R(self, V):
        """Evaluate smooth function :math:`f` in V.

        Overriding this method is required.
        """

        raise NotImplementedError()



    def eval_Rx(self):
        """Evaluate smooth function :math:`f` in X."""

        return self.eval_R(self.X)



    def store_prev(self):
        """Store previous X state."""

        self.Xprv = self.X.copy()



    def eval_Dxy(self):
        """Evaluate difference of state and auxiliary state updates."""

        return self.X - self.Y



    def compute_residuals(self):
        """Compute residuals and stopping thresholds."""

        r = self.rsdl()
        adapt_tol = self.opt['RelStopTol']

        if self.opt['AutoStop', 'Enabled']:
            adapt_tol = self.tau0 / (1. + self.k)

        return r, adapt_tol



    @classmethod
    def hdrtxt(cls):
        """Construct tuple of status display column title."""

        return ('Itn',) + cls.hdrtxt_objfn + ('Rsdl', 'F', 'Q', 'It_Bt', 'L')




    @classmethod
    def hdrval(cls):
        """Construct dictionary mapping display column title to
        IterationStats entries.
        """

        hdrmap = {'Itn': 'Iter'}
        hdrmap.update(cls.hdrval_objfun)
        hdrmap.update({'Rsdl': 'Rsdl', 'F': 'F_Btrack', 'Q': 'Q_Btrack',
                       'It_Bt': 'IterBTrack', 'L': 'L'})

        return hdrmap



    def iteration_stats(self, k, frcxd):
        """Construct iteration stats record tuple."""

        tk = self.timer.elapsed(self.opt['IterTimer'])
        tpl = (k,) + self.eval_objfn() + \
              (frcxd, self.F, self.Q, self.iterBTrack, self.L) + \
              self.itstat_extra() + (tk,)
        return type(self).IterationStats(*tpl)



    def eval_objfn(self):
        """Compute components of objective function as well as total
        contribution to objective function.
        """

        fval = self.obfn_f(self.X)
        gval = self.obfn_g(self.X)
        obj = fval + gval
        return (obj, fval, gval)



    def itstat_extra(self):
        """Non-standard entries for the iteration stats record tuple."""

        return ()



    def getitstat(self):
        """Get iteration stats as named tuple of arrays instead of
        array of named tuples.
        """

        return util.transpose_ntpl_list(self.itstat)



    def display_start(self):
        """Set up status display if option selected. NB: this method
        assumes that the first entry is the iteration count and the
        last is the L value.
        """

        if self.opt['Verbose']:
            # If backtracking option enabled F, Q, itBT, L are
            # included in iteration status
            if self.opt['BackTrack', 'Enabled']:
                hdrtxt = type(self).hdrtxt()
            else:
                hdrtxt = type(self).hdrtxt()[0:-4]
            # Call utility function to construct status display formatting
            hdrstr, fmtstr, nsep = common.solve_status_str(
                hdrtxt, fmtmap={'It_Bt': '%5d'}, fwdth0=type(self).fwiter,
                fprec=type(self).fpothr)
            # Print header and separator strings
            if self.opt['StatusHeader']:
                print(hdrstr)
                print("-" * nsep)
        else:
            fmtstr, nsep = '', 0

        return fmtstr, nsep



    def display_status(self, fmtstr, itst):
        """Display current iteration status as selection of fields from
        iteration stats tuple.
        """

        if self.opt['Verbose']:
            hdrtxt = type(self).hdrtxt()
            hdrval = type(self).hdrval()
            itdsp = tuple([getattr(itst, hdrval[col]) for col in hdrtxt])
            if not self.opt['BackTrack', 'Enabled']:
                itdsp = itdsp[0:-4]

            print(fmtstr % itdsp)



    def display_end(self, nsep):
        """Terminate status display if option selected."""

        if self.opt['Verbose'] and self.opt['StatusHeader']:
            print("-" * nsep)



    def var_x(self):
        r"""Get :math:`\mathbf{x}` variable."""

        return self.X



    def obfn_f(self, X):
        r"""Compute :math:`f(\mathbf{x})` component of FISTA objective
        function.

        Overriding this method is required if :meth:`eval_objfun`
        is not overridden.
        """

        raise NotImplementedError()



    def obfn_g(self, X):
        r"""Compute :math:`g(\mathbf{x})` component of FISTA objective
        function.

        Overriding this method is required if :meth:`eval_objfun`
        is not overridden.
        """

        raise NotImplementedError()



    def rsdl(self):
        """Compute fixed point residual.

        Overriding this method is required.
        """

        raise NotImplementedError()



    def Lchange(self):
        """Action to be taken, if any, when L parameter is changed.

        Overriding this method is optional.
        """

        self.last_Lchange = self.k




class FISTADFT(FISTA):
    r"""
    Base class for FISTA algorithms with gradients and updates computed
    in the frequency domain.

    |

    .. inheritance-diagram:: FISTADFT
       :parts: 2

    |

    Solve optimisation problems of the form

    .. math::
       \mathrm{argmin}_{\mathbf{x}} \;
       f(\mathbf{x}) + g(\mathbf{x}) \;\;,

    where :math:`f, g` are convex functions and :math:`f` is smooth.

    This class specialises class FISTA, but remains a base class for
    other classes that specialise to specific optimisation problems.
    """


    class Options(FISTA.Options):
        """FISTADFT algorithm options.

        Options include all of those defined in :class:`FISTA.Options`.
        """

        defaults = copy.deepcopy(FISTA.Options.defaults)

        def __init__(self, opt=None):
            """
            Parameters
            ----------
            opt : dict or None, optional (default None)
              FISTADFT algorithm options
            """

            if opt is None:
                opt = {}
            FISTA.Options.__init__(self, opt)




    def __init__(self, xshape, dtype, opt=None):
        """
        Parameters
        ----------
        xshape : tuple of ints
          Shape of working variable X (the primary variable)
        dtype : data-type
          Data type for working variables
        opt : :class:`FISTADFT.Options` object
          Algorithm options
        """

        if opt is None:
            opt = FISTADFT.Options()
        Nx = np.product(np.array(xshape))
        super(FISTADFT, self).__init__(Nx, xshape, dtype, opt)



    def proximal_step(self, gradf=None):
        """Compute proximal update (gradient descent + constraint)."""

        if gradf is None:
            gradf = self.eval_gradf()


        self.Vf[:] = self.Yf - (1. / self.L) * gradf
        V = sl.irfftn(self.Vf, self.cri.Nv, self.cri.axisN)

        self.X[:] = self.eval_proxop(V)
        self.Xf = sl.rfftn(self.X, None, self.cri.axisN)



    def combination_step(self):
        """Update auxiliary state by a smart combination of previous
        updates in the frequency domain.
        """

        # Update t step
        tprv = self.t
        self.t = 0.5 * float(1. + np.sqrt(1. + 4. * tprv**2))

        # Update Y
        if not self.opt['FastSolve']:
            self.Yfprv = self.Yf.copy()
        self.Yf = self.Xf + ((tprv - 1.) / self.t) * (self.Xf - self.Xfprv)



    def compute_backtracking(self):
        """Estimate step size L by computing a linesearch that
        guarantees that F <= Q.
        """

        gradfYf = self.eval_gradf()

        eta = self.L_eta
        maxiter = self.L_maxiter
        self.FBtprev = self.F

        iterBTrack = 0
        linesearch = 1
        while linesearch and iterBTrack < maxiter:

            self.proximal_step(gradfYf)
            Rxf = self.eval_Rxf()

            F = 0.5 * np.linalg.norm(Rxf.flatten(), 2)**2
            Dxyf = self.eval_Dxyf()
            Q = 0.5 * np.linalg.norm(self.Ryf.flatten(), 2)**2 + \
                np.sum(np.real(Dxyf * gradfYf)) + \
                (self.L/2.) * np.linalg.norm(Dxyf.flatten(), 2)**2

            if F <= Q:
                linesearch = 0
            else:
                self.L *= eta
                self.Lchange()
                iterBTrack += 1

        self.F = F
        self.Q = Q
        self.iterBTrack = iterBTrack
        if ((self.k > 100) and (self.k - self.last_Lchange) > 50) \
                           and (self.FBtprev <= self.F):
            self.L /= 1.01
            self.Lchange()



    def store_prev(self):
        """Store previous X in frequency domain."""

        self.Xfprv = self.Xf.copy()



    def eval_Dxyf(self):
        """Evaluate difference of state and auxiliary state."""

        return self.Xf - self.Yf



    def eval_Rxf(self):
        """Evaluate smooth term in X."""

        return self.eval_Rf(self.Xf)



    def eval_gradf(self):
        """Compute gradient in Fourier domain. Also computes argument
        of smooth function :math:`f`.

        Overriding this method is required.
        """

        raise NotImplementedError()



    def eval_proxop(self, V):
        """Compute proximal operator of :math:`g`.

        Overriding this method is required.
        """

        raise NotImplementedError()
