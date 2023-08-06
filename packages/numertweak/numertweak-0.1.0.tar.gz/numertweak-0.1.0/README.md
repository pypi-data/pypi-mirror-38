[![Build Status](https://travis-ci.org/kmedian/numertweak.svg?branch=master)](https://travis-ci.org/kmedian/numertweak)
<!-- 
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/numertweak/master?urlpath=lab)
-->

# numertweak
Some utility function for the [numer.ai](https://numer.ai/rounds) competition.

This for my personal usage so far. 
If you have any questions then send me an Email.

## Table of Contents
* [Installation](#installation)
* [Commands](#commands)
* [Support](#support)
* [Contributing](#contributing)


## Installation
The `numertweak` [git repo](http://github.com/kmedian/numertweak) is available as [PyPi package](https://pypi.org/project/numertweak)

```
pip install numertweak
```

In notebooks use this

```
%%capture
!pip install "numertweak>=0.1.0"
from numertweak import *
```


## Commands
* Check syntax: `flake8 --ignore=F401`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`


## Debugging
* Notebooks to profile python code are in the [profile](profile) folder


## Support
Please [open an issue](https://github.com/kmedian/numertweak/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/numertweak/compare/).
