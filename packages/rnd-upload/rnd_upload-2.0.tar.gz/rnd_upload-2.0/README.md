### Livenviro LEQ rnd upload script

#### Requirements:
- python 3.6 (make sure to check 'Add to PATH' option when installing)
- Windows: mysqlclient (see Windows Installation section)
- rnd_upload python module

#### Windows (64-bit):
**Installation**:  
Use the following link to install [python 3.6](https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe)  
Open PowerShell in current folder (shift + right click in folder explorer-> Open PowerShell)  
Run the commands bellow in PowerShell:    
1. `pip3.6.exe install .\requirements\mysqlclient-1.3.13-cp36-cp36m-win_amd64.whl`  
2. `pip3.6.exe install rnd_upload`

**Usage**:  
1. Open PowerShell in current folder  
2. run `.\executables\rnd_upload.exe <config_name>`


#### Linux:
**Installation**:  
`pip install rnd_upload`

**Usage**:  
`python -m rnd_upload <config_name>`  
or  
`./executables/rnd_upload <config_name>`

#### Development:
Build:
`python setup.py sdist bdist_wheel`

Upload:
`twine upload --repository pypi dist/*`