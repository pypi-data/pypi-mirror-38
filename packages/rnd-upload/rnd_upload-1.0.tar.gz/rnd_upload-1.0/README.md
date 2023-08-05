### Livenviro LEQ rnd upload script

Installation:  
`pip install rnd_upload`

Usage:  
`python -m rnd_upload <config_name>`

Build:
`python setup.py sdist bdist_wheel`

Upload:
`twine upload --repository pypi dist/*`