# Validate-it

[![Build Status](https://travis-ci.org/ruslux/accordion.svg?branch=master)](https://travis-ci.org/ruslux/accordion) 
[![Coverage Status](https://coveralls.io/repos/github/ruslux/accordion/badge.svg?branch=master)](https://coveralls.io/github/ruslux/accordion)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ruslux/accordion/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ruslux/accordion)
[![PyPI version](https://badge.fury.io/py/accordion.svg)](https://badge.fury.io/py/accordion)

- [About](#about)
- [Installation](#installation)
- [Example](#example)
- [Requirements](#requirements)
- [Contribution how-to](#contribution)

### <a name="about"/>About</a>
Make flat dict and back from `dict`


### <a name="installation"/>Installation</a>
With pip:
```bash
pip install accordion
```

### <a name="example"/>Example</a>
```python
from accordion import compress, expand

data = {
    "a": [1, 2, 3],
    "b": {
        "c": "d"
    }
}

expected = {
    "a/0": 1,
    "a/1": 2,
    "a/2": 3,
    "b.c": "d"
}

assert compress(data) == expected
assert expand(compress(data)) == data
```
### <a name="requirements"/>Requirements</a>
Tested with `python3.6`

### <a name="contribution"/>Contribution how-to</a>
###### Run tests:
* clone repo: `git clone <your-fork>`
* create and activate your virtualenv
* `pip install -r requirements.txt && pip install -r dev-requirements`
* `./run_tests.sh`
