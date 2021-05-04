#
# PyEqn.py
# Jeremy Turpin, Isotropic Systems, jeremy@isotropicsystems.compile
# April 23, 2020
#
# Provides the Eqn class that represents an symbolic equation (i.e., two expressions separated by an equality)
# that can be manipulated as a single object. 
# This allows the algebra to be handled by Sympy, while the decision for which step to take 
# is provided by the human in the loop. 
# When equations are added to an EqnSet, then the EqnSet allows for pretty-printing, equation numbering, and 
# number- or name-based references to previous equations. 
#

import sympy as sym
from enum import Enum
from IPython.display import display
sym.init_printing()


class EqnSet:
    def __init__(self):
        self.eqns = []
        self.namemap = {}
    def __ior__(self,eqn):
        self.eqns.append(eqn)
        eqn.set_number(len(self.eqns)-1)
        if (len(eqn.name())>0):
            self.namemap[eqn.name()] = eqn.number()
        display(eqn)
        return self
    def __len__(self):
        return len(self.eqns)
    def __getitem__(self, key):
        try:
            return self.eqns[int(key)]
        except ValueError:
            return self.eqns[self.namemap[key]]        
    def _repr_latex_(self):        
        s = ''
        for item in self:
            s += item._repr_latex_() + '\\\\'
        return s   
    def __iter__(self):
        return self.eqns.__iter__()
    
class EqnType(Enum):
    Inter = 1 #Intermediate expression; Should not be used when evaluating code    
    Eval = 2 #Evaluation expression; Should be used for evaluation; The LHS should be a single symbol; all items on the RHS are well-defined and can be evaluted. 

class Eqn:
    """Defines an Equation that includes an equality, with a left and right side.
        Operations done to the expression are performed on both sides of the expression. 
        This is something that should be built in to every CAS! Seriously...Am 
        I just not using the right search terms? """
    def __init__(self,lhs,rhs,name='',flag=EqnType.Inter):
        self.lhs = lhs
        self.rhs = rhs
        self._num = None
        self._name = name
        self._flag = flag
    def name(self):
        return self._name
    def set_name(self,value):
        self._name = value
        return self
    def flag(self):
        return self._flag
    def set_number(self,value):
        self._num = value
    def number(self):
        return self._num
    def _repr_latex_(self):        
        from sympy.printing.latex import latex
        s1 = latex(self.lhs, mode='plain')
        s2 = latex(self.rhs, mode='plain')
        if not self._num is None:
            return "(Eq. %i)$\\qquad\\displaystyle %s = %s$" % (self._num,s1,s2)
        else:
            return "$\\displaystyle %s = %s$" % (s1,s2)
    def __add__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(self.lhs+other.lhs,self.rhs+other.rhs)
        else:
            return self.__class__(self.lhs+other,self.rhs+other)        
    def __sub__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(self.lhs-other.lhs,self.rhs-other.rhs)
        else:
            return self.__class__(self.lhs-other,self.rhs-other)
    def __mul__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(self.lhs*other.lhs,self.rhs*other.rhs)
        else:
            return self.__class__(self.lhs*other,self.rhs*other)
    def __truediv__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(self.lhs/other.lhs,self.rhs/other.rhs)
        else:
            return self.__class__(self.lhs/other,self.rhs/other)        
    def __radd__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(other.lhs+self.lhs,other.rhs+self.rhs)
        else:
            return self.__class__(other+self.lhs,other+self.rhs)        
    def __rsub__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(other.lhs-self.lhs,other.rhs-self.rhs)
        else:
            return self.__class__(other-self.lhs,other-self.rhs)
    def __rmul__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(other.lhs*self.lhs,other.rhs*self.rhs)
        else:
            return self.__class__(other*self.lhs,other*self.rhs)
    def __rtruediv__(self,other):
        if (isinstance(other,self.__class__)):
            return self.__class__(other.lhs/self.lhs,other.rhs/self.rhs)
        else:
            return self.__class__(other/self.lhs,other/self.rhs)
    def __pow__(self,other):
        return self.__class__(self.lhs**other,self.rhs**other)
    def swap(self):
        return self.__class__(self.rhs,self.lhs)
    def subs(self,*args):
        if len(args) == 1 and isinstance(args[0],self.__class__):
            return self.__class__(self.lhs.subs(args[0].lhs,args[0].rhs),self.rhs.subs(args[0].lhs,args[0].rhs))
        else:
            return self.__class__(self.lhs.subs(*args),self.rhs.subs(*args))
    def factor(self):
        return self.__class__(self.lhs.factor(),self.rhs.factor())
    def expand(self):
        return self.__class__(self.lhs.expand(),self.rhs.expand())
    def collect(self,*args):
        return self.__class__(self.lhs.collect(*args),self.rhs.collect(*args))
    def diff(self,*args):
        return self.__class__(sym.diff(self.lhs,*args),sym.diff(self.rhs,*args))
    def to_octave(self):        
        l=sym.octave_code(self.lhs)
        r=sym.octave_code(self.rhs)
        return '%s = %s'%(l,r)
		
		
		
def Eqn_example():
	pi,lam = sym.symbols('pi lambda_0')

	x,y,z = sym.symbols('x y z')

	xi,yi,zi,di,thetai,phii = sym.symbols('x_i y_i z_i d_i theta_i phi_i')
	delta, psii, li = sym.symbols('delta psi_i l_i')

	# Identifiers x, y, z, delta are the variables to be solved - the location of the phase center, 
	#    and the offset distance delta (not directly useful)
	# Identifiers phii, thetai, psii are direct observables (from the measured/simulated data) for each observation
	# Identifiers xi, yi, zi, di are derived observables (computed from the direct observations)

	es = EqnSet()
	es |= Eqn(di, sym.sqrt((x-xi)**2+(y-yi)**2+(z-zi)**2),name='start')
	es |= Eqn(di, delta + (lam/(2*pi))*psii,name='di')

	#Substitution values for xi, yi, zi
	es |= Eqn(xi , sym.cos(phii)*sym.sin(thetai),flag=EqnType.Eval)
	es |= Eqn(yi , sym.sin(phii)*sym.sin(thetai),flag=EqnType.Eval)
	es |= Eqn(zi , sym.cos(thetai),flag=EqnType.Eval)

	es |= es['start'].subs(es['di']).set_name('start2')

	es |= (es[5] ** 2).set_name('start3')
	es |= (es['start3'] - es['start3'].lhs).set_name('start4')
	es |= Eqn(li,psii*lam/(2*pi),name='li',flag=EqnType.Eval)
	es |= es['start4'].subs(es['li'].swap())
	