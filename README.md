# pyeqn

Provides the Eqn class that represents an symbolic equation (i.e., two expressions separated by an equality) that can be manipulated as a single object using sympy

This allows the algebra to be handled by Sympy, while the decision for which step to take is provided by the human in the loop. 

When equations are added to an EqnSet, then the EqnSet allows for pretty-printing, equation numbering, and number- or name-based references to previous equations. 

Install as:
```bash
pip install git+ssh://git@github.com/jeremy-isl/pyeqn.git#egg=pyeqn
```

Import as:
```python
from pyeqn.pyeqn import Eqn, EqnSet, EqnType
```


```python
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
```
