from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='pyeqn',
    url='https://github.com/jeremy-isl/pyeqn.git',
    author='jeremy-isl',
    author_email='j@i.co',
    # Needed to actually package something
    packages=['pyeqn'],
    # Needed for dependencies
    install_requires=['sympy','IPython'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='proprietary',
    description='Provides the Eqn class that represents an symbolic equation (i.e., two expressions separated by an equality) that can be manipulated as a single object using sympy',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
