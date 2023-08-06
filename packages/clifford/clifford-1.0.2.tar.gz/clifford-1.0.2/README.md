[clifford](http://clifford.readthedocs.org/en/latest/): Geometric Algebra for Python
=========================================================
A numerical geometric algebra module for python. BSD License. 

[![Build Status](https://travis-ci.org/pygae/clifford.svg?branch=master)](https://travis-ci.org/pygae/clifford) [![Documentation Status](https://readthedocs.org/projects/clifford/badge/?version=latest)](http://clifford.readthedocs.io/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/pygae/clifford/badge.svg?branch=master)](https://coveralls.io/github/pygae/clifford?branch=master) [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/pygae/clifford/master?filepath=examples%2Fg3c.ipynb) 

[![DOI](https://zenodo.org/badge/26588915.svg)](https://zenodo.org/badge/latestdoi/26588915)




Quickstart
--------------

Try out a notebook in [binder](https://mybinder.org/v2/gh/pygae/clifford/master?filepath=examples%2Fg3c.ipynb)

Or have a go on your own pc:

    from clifford.g3 import *  # import GA for 3D space
    from numpy import e,pi
    a = e1 + 2*e2 + 3*e3 # vector 
    R = e**(pi/4*e12)    # rotor 
    R*a*~R    # rotate the vector  

Summary
----------


This module implements Geometric Algebras (a.k.a. Clifford algebras). Geometric Algebra (GA) is a universal algebra which subsumes complex algebra, quaternions, linear algebra and several other independent mathematical systems.  Scalars, vectors, and higher-grade entities can
be mixed freely and consistently in the form of mixed-grade multivectors. Like this, 

![blades](https://github.com/arsenovic/clifford/blob/master/docs/_static/blades.png)


If you think Geometric Algebra looks interesting and want to learn more, check out the [cambridge group page]( http://geometry.mrao.cam.ac.uk/),  and here are some great introductory textbooks!

* Geometric Algebra for Physicists, by Doran and Lasenby
* Geometric Algebra for Computer Science, by Dorst, Fontijne and Mann
* New Foundations for Classical Mechanics, by David Hestenes



