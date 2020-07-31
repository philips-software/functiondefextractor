# INSTALL

Requirements are added in requirement.txt file

Python 3.8

python: install python for the respective OS at
"https://www.python.org/downloads/" Make sure to update the
path variable to point to the python installation folder.

pip: (only if pip is not present by default) get get-pip.py
from below link to your folder "https://bootstrap.pypa.io/get-pip.py"
Open a command prompt and navigate to the folder containing get-pip.py.

Run the following command:

functiondefextractor:

pip install functiondefextractor

## Other tools

### Ctags: "https://en.wikipedia.org/wiki/Ctags"

- Windows:

1.Download Ctags from "http://ctags.sourceforge.net/"

2.Select the right package(based on OS & architecture) and

extract the zip file to a folder

3.Update the system 'path' environment variable with the path to ctags executable

- Linux:

`apt-get install ctags`

- OS X:

`brew install ctags`

### grep

1.Download grep `"binaries and Dependencies"`

from `http://gnuwin32.sourceforge.net/packages/grep.htm`

2.Extract the content to a folder

3.Copy and paste contents from `\bin` folder of Dependencies

to `\bin` folder of Binaries

4.Update the system `'path'` environment variable with the path to "grep" executable
