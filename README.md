Keys in commit history are deprecated and deauthorized. Generate new keys.

# Python dependencies:

64bit Python 3.5 or newer

### Packages:

1. [pyrebase](https://github.com/thisbejim/Pyrebase)

2. [pyqt5](https://pypi.org/project/PyQt5/) < install this one before pyforms

3. [pyforms](https://github.com/UmSenhorQualquer/pyforms)  -GUI package

4. [pysettings](https://github.com/UmSenhorQualquer/pysettings) - modular settings for Python apps

5. [keyboard](https://pypi.org/project/keyboard/) - detect keyboard events

**All can be installed via pip**, which is the python package handler. Should get installed alongside python. Otherwise, rerun the installer in Windows or get it with ```apt-get install``` on Ubuntu.
```
pip install <package>
```
**pysetting's current pip package is out of date. update from git
using**
```
pip install git+https://github.com/UmSenhorQualquer/pysettings.git --upgrade
```
DB_Actions.py can be run as a commandline program on its own if you just want to push notifications out.

In Linux, mark it as executable, then run it like any other program in CLI.

In Windows, double click on the file, or run it with ```python DB_Actions.py``` in cmd.exe

You'll need to add a user account to the database to login.
