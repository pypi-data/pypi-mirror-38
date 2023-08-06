from array import array
from .cfile import cfile, c_double, c_double_p, c_long, c_long_p, c_int_p, c_int


class libglpk(object):
    GLP_MIN = 1
    GLP_MAX = 2
    
    GLP_CV = 1
    GLP_IV = 2
    GLP_BV = 3

    GLP_FR = 1
    GLP_LO = 2
    GLP_UP = 3
    GLP_DB = 4
    GLP_FX = 5

    so = cfile('call_glpk.c', cflags='-O3 -march=native', ldflags='-lglpk')
    call_glpk = so.call_glpk
    call_glpk.argtypes = [c_long, c_double_p, c_double_p, c_long, 
                          c_long, c_long_p, c_double_p, c_double_p,
                          c_long, c_long_p, c_double_p, c_double_p,
                          c_long, c_int_p, c_int_p, c_double_p,
                          c_long, c_long_p, c_int, c_int
                          ]
    
    call_glpk.restype = c_double


class AutoArray(array):
    def __setitem__(self, idx, val):
        if idx >= len(self):
            self.extend(array(self.typecode, (0,)) * (idx - len(self) + 1))
        return array.__setitem__(self, idx, val)

    def __getitem__(self, idx):
        if idx >= len(self):
            self.extend(array(self.typecode, (0,)) * (idx - len(self) + 1))
        return array.__getitem__(self, idx)

class Objective(object):
    def __init__(self, lp, expr=None):
        self.lp = lp
        self.coefficients = AutoArray('d', [0.0])
        if expr:
            for t in expr._term_list:
                self.coefficients[t.var.index] += t.coefficient

    def __iadd__(self, expr):
        for t in expr._term_list:
            self.coefficients[t.var.index] += t.coefficient
        return self

    def __isub__(self, expr):
        for t in expr._term_list:
            self.coefficients[t.var.index] -= t.coefficient
        return self

        

class LinearProgram(object):
    def __init__(self, verbose=0):
        self.vars = 0
        self.var_bound = AutoArray('l')
        self.var_lower = AutoArray('d')
        self.var_upper = AutoArray('d')
        self.var_kind = AutoArray('l')

        self.auxvars = 0
        self.auxvar_bound = AutoArray('l')
        self.auxvar_lower = AutoArray('d')
        self.auxvar_upper = AutoArray('d')

        self.amatrix_i = AutoArray('i', (-1,))
        self.amatrix_j = AutoArray('i', (-1,))
        self.amatrix_r = AutoArray('d', (-1,))

        self._objective = Objective(self)
        self.verbose = verbose


    def Var(self):
        self.vars += 1
        return Var(self, self.vars)

    def IntVar(self):
        self.vars += 1        
        v = IntVar(self, self.vars)
        self.var_kind[v.index] = libglpk.GLP_IV
        return v

    def BoolVar(self):
        v = self.IntVar()
        self.var_kind[v.index] = libglpk.GLP_BV
        return v

    def _set_objective(self, value):
        if not isinstance(value, Objective):
            value = Objective(self, value)
        self._objective = value
    
    def _get_objective(self):
        return self._objective
    
    objective = property(_get_objective, _set_objective)

    def add_constraint(self, bound):
        if bound is True:
            return
        (t, l ,u) = bound.glpk_bound()
        if isinstance(bound.expr, Var):
            assert bound.expr.index <= self.vars
            self.var_bound[bound.expr.index] = t
            self.var_lower[bound.expr.index] = l
            self.var_upper[bound.expr.index] = u
        else:
            self.auxvars += 1
            self.auxvar_bound[self.auxvars] = t
            self.auxvar_lower[self.auxvars] = l
            self.auxvar_upper[self.auxvars] = u
            for t in bound.expr._term_list:
                self.amatrix_i.append(self.auxvars)
                self.amatrix_j.append(t.var.index)
                self.amatrix_r.append(t.coefficient)

            

    def maximize(self):
        return self.optimize(libglpk.GLP_MAX)

    def minimize(self):
        return self.optimize(libglpk.GLP_MIN)

    def optimize(self, direction):
        self.var_value = array('d', [0.0]) * (self.vars + 1)
        assert len(self.var_bound) == len(self.var_upper) == len(self.var_lower)
        assert len(self.auxvar_bound) == len(self.auxvar_upper) == len(self.auxvar_lower)
        assert len(self.amatrix_i) == len(self.amatrix_j) == len(self.amatrix_r)
        assert len(self._objective.coefficients) == self.vars + 1
        v = libglpk.call_glpk(self.vars, self._objective.coefficients, self.var_value,
                              direction,
                              len(self.var_bound),
                              self.var_bound, self.var_lower, self.var_upper,
                              len(self.auxvar_bound),
                              self.auxvar_bound, self.auxvar_lower, self.auxvar_upper,
                              len(self.amatrix_i),
                              self.amatrix_i, self.amatrix_j, self.amatrix_r,
                              len(self.var_kind), self.var_kind,
                              1, self.verbose)
        return v
        

class Expr(object):
    _making_dual_bound = None # Nasty hack!!
    
    def __add__(self, other):
        if isinstance(other, int) and other == 0:
            return self
        return LinearCombination(self._term_list + other._term_list)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int) and other == 0:
            return self
        other_term_list = [Term(-t.coefficient, t.var) for t in other._term_list]
        return LinearCombination(self._term_list + other_term_list)

    def __rsub__(self, other):
        if other == 0:
            return self
        self_term_list = [Term(-t.coefficient, t.var) for t in self._term_list]
        return LinearCombination(self_term_list + other._term_list)

    def __mul__(self, other):
        if isinstance(other, Expr):
            return NotImplemented
        return LinearCombination([Term(other*t.coefficient, t.var) for t in self._term_list])
    __rmul__ = __mul__

    @property
    def _term_list(self):
        raise NotImplementedError

    def __le__(self, other):
        b = UpperBound(self, other)
        if self._making_dual_bound is not None:
            if b.bound == self._making_dual_bound.bound:
                b = FixedBound(self, other)
            else:
                b = DualBound(self._making_dual_bound, b)
            self._making_dual_bound = None
        return b

    def __ge__(self, other):
        b = LowerBound(self, other)
        if self._making_dual_bound is not None:
            b = DualBound(b, self._making_dual_bound)
            self._making_dual_bound = None
        return b

    def __eq__(self, other):
        return FixedBound(self, other)

    def __lt__(self):
        raise NotImplementedError
    __gt__ = __neq__ = __lt__
    

class Var(Expr):
    def __init__(self, lp, index):
        self.lp = lp
        self.index = index

    @property
    def _term_list(self):
        return [Term(1, self)]

    def __repr__(self):
        return 'X%d' % self.index

    @property
    def value(self):
        return self.lp.var_value[self.index]

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

class IntVar(Var):
    @property
    def value(self):
        return int(self.lp.var_value[self.index])

        
class Term(Expr):
    def __init__(self, coefficient, var):
        self.coefficient = coefficient
        self.var = var

    @property
    def _term_list(self):
        return [self]

    def __repr__(self):
        return '%5.2f %r' % (self.coefficient, self.var)


class LinearCombination(Expr):
    def __init__(self, terms):
        self.terms = terms

    @property
    def _term_list(self):
        return self.terms

    def __repr__(self):
        return ' + '.join(['%r'%t for t in self.terms])

class Bound(object):
    def __init__(self, expr, bound):
        self.expr = expr
        self.bound = bound

    def __nonzero__(self):
        self.expr._making_dual_bound = self
        return True

    __bool__ = __nonzero__

class UpperBound(Bound):
    def __repr__(self):
        return '%r <= %5.2f' % (self.expr, self.bound)

    def glpk_bound(self):
        return (libglpk.GLP_UP, 0.0, self.bound)

class LowerBound(Bound):
    def __repr__(self):
        return '%r >= %5.2f' % (self.expr, self.bound)

    def glpk_bound(self):
        return (libglpk.GLP_LO, self.bound, 0.0)

class FixedBound(Bound):
    def __repr__(self):
        return '%r == %5.2f' % (self.expr, self.bound)

    def glpk_bound(self):
        return (libglpk.GLP_FX, self.bound, self.bound)

class DualBound(object):
    def __init__(self, lower, upper):
        assert lower.expr is upper.expr
        self.lower = lower.bound
        self.expr = lower.expr
        self.upper = upper.bound
        
    def __repr__(self):
        return '%5.2f <= %r <= %5.2f' % (self.lower, self.expr, self.upper)

    def glpk_bound(self):
        return (libglpk.GLP_DB, self.lower, self.upper)
    
    
        

    
        
    


        
        
        
