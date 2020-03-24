[![Build Status](https://travis-ci.com/bkk003/FunctionDefExtractor.svg?branch=master)](https://travis-ci.com/bkk003/FunctionDefExtractor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/bkk003/FunctionDefExtractor/branch/master/graph/badge.svg)](https://codecov.io/gh/bkk003/FunctionDefExtractor)


Function Definition Extractor
=============================

What is the project intended to solve?
-------------------------------------
Project will help to extract the function definitions from source or test code and report the extracted output
 in a data frame which can be further used for Similarity processing, Review, etc...

Dependencies
------------
`Python 3.7.3 `

[packages]
**************
```
pip

mutmut

pytest

pandas

codecov

pytest-cov

pylint
```
[Third party tools]
******************
```
Ctags

grep
```
Installation
-----------
[INSTALL.md](INSTALL.md)

Usage & Configuration
--------------------
1. Install the tool using `pip install functiondefextractor`
2. To call from script
```
from functiondefextractor import core_extractor
out_put = core_extractor.extractor (r"path_to_repo/code")
print(out_put)
```

```
from functiondefextractor import core_extractor
out_put = core_extractor.extractor (r"path_to_repo/code")
# Default value of arguments are parse_code="True", parse_test="True", annot=None, delta=None
print(out_put)
```
3. To call from commandline
```
python -m functiondefextractor.extractor_cmd -h 
```
Note: 

1.To use annotation based search feature, input annot and delta parameters (For example annot = "@Test", delta = "5") 
  which returns a data frame containing + and - delta number of lines from the given annotation
  
2.While using this feature parse_code, parse_test conditions are set to default(True).

3.An xlsx file is also generated as output in the same input location. 
```
from functiondefextractor import core_extractor
out_put = core_extractor.extractor (r"path_to_repo/code", parse_code="True", parse_test="True
", annot="@Test", delta="5")
print(out_put)
```

How to test the software
-----------------------
1. To test the tool use : navigate to `functiondefextractor` which is the root directory
2. Issue `pytest -v` to run all the tests
To report the pytest in html: issue command `pytest --html=report.html`

To run test for coverage: `pytest --cov-report html --cov="src"`

pydoc creation `python -m pydoc -w module_name`

mutation testing using mutmut `mutmut run`

pylint execution on code `pylint src test >"path_to_save_file\pylint.txt"`

jscpd execution on root folder `jscpd --min-tokens 20 --reporters "html" --mode "strict" --format "python" --output . .`

Contact / Getting help
----------------------
[MAINTAINERS.md](MAINTAINERS.md)

License
--------
[License.md](License.md)
