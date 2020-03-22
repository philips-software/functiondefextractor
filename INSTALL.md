# INSTALL

Requirements are added in requirement.txt file

python & packages
----------------

`Python 3.7.3 - 64 bit`

python:
install python for the respective OS at `https://www.python.org/downloads/` Make sure to update the path variable to point to the python installation folder.

pip:
get `get-pip.py` from below link to your folder `https://bootstrap.pypa.io/get-pip.py` Open a command prompt and navigate to the folder containing `get-pip.py`. Run the following command:

pandas:
`python -m pip install pandas`

pylint:
`python -m pip install -U pylint`

mutmut:
`python -m pip install mutmut`

pytest:
`python -m pip install pytest`

unittest:
`python -m pip install unittest`

codecov:
`python -m pip install codecov`

pytest-cov:
`python -m pip install pytest-cov`

Other tools
-----------
Ctags: `https://en.wikipedia.org/wiki/Ctags`
***********************

Windows:
1. Download Ctags from `https://sourceforge.net/projects/ctags/files/ctags/5.8/ctags58.zip/download?use_mirror
=excellmedia` 

   or 

     `http://ctags.sourceforge.net/`
2. select the right package(based on the Operating system and architecture) and extract the zip file to a folder
3. Update the system 'path' environment variable with the path to ctags executable

Linux: 

`apt-get install ctags`

OS X: 

`brew install ctags`
grep
***********************
1. Download grep `"binaries and Dependencies"` from `http://gnuwin32.sourceforge.net/packages/grep.htm` 
2. extract the content to a folder
3. Copy and paste contents from `\bin` folder of Dependencies to `\bin` folder of Binaries
4. Update the system `'path'` environment variable with the path to "grep" executable


