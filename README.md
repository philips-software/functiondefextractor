# Function Extractor

[![Build Status](https://travis-ci.com/philips-software/functiondefextractor.svg?branch=master)](https://travis-ci.com/philips-software/functiondefextractor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/philips-software/functiondefextractor/branch/master/graph/badge.svg)](https://codecov.io/gh/philips-software/functiondefextractor)

Tool to extract the function definitions from the source code

It can be used to extract functions from,

- C  

- C++

- C#  

- Java  

- Python

- TypeScript

- JavaScript

Advantage of using such function extractions are,

- Resolving technical debt  

- Identify function similarity  

- Identify pattern check (Supress warnings, Asset, etc...)
  
## Dependencies

- python 3.8 : 64 bit  

- python packages (xlrd, xlsxwriter, pandas)  

- third party packages [Ctags, grep]

## Installation
  
[INSTALL.md](INSTALL.md)

```sh
pip install functiondefextractor
```

## Usage & Configuration

### Code

- General usage with out options.

```sh
from functiondefextractor import core_extractor
out_put = core_extractor.extractor (r"path_to_repo/code")
print(out_put)
```

- To extract functions based on annotation.

```sh
from functiondefextractor import core_extractor
out_put = core_extractor.extractor (r"path_to_repo/code", annot="@Test")
print(out_put)
```

- To extract delta lines(+/-) from code based on annotation/key word.

```sh
from functiondefextractor import core_extractor
out_put = core_extractor.extractor
          (r"path_to_repo/code", annot="@SupressWarning", delta="5")
print(out_put)
```

- To analyse various patterns in the code based on given condition.

```sh
from functiondefextractor import core_extractor
out_put = core_extractor.check_condition
          ("@SupressWarning", r"path_to_excelfile/dataframe", "(")
print(out_put)
```

### Commandline

- General usage with out options to extract functions from repo.

```sh
>>>python -m functiondefextractor.extractor_cmd --p path/to/repo
```

- To analyse various patterns in the code based on given condition.

```sh
>>>python -m functiondefextractor.extractor_cmd
             --c "@Assert" --e path/to/excel/dataframe --s "("
```

- Help option can be found at,  

```sh
>>>python -m functiondefextractor.extractor_cmd -h
```

### Output
  
- Executing functiondefextractor to extract functions from
 command line would generate an output excel file which contains
 FileName_FunctionName in Unique ID column and extracted functions in Code column

- Using functiondefextractor to extract functions from code would return
 a dataframe with same content as excel file.

- when functiondefextractor is executed to analyse patterns in code, an excel file
 with multiple sheets would be generated which contains the requested patterns and
 top 10 patterns. Also an html file with pivot table of top 10 patterns
 would be generated.

## Contact

[MAINTAINERS.md](MAINTAINERS.md)  

## License

[License.md](LICENSE.md)
