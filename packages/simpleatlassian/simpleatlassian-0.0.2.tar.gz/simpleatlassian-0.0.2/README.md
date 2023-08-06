# python-simpleatlassian
The most simple, and most powerful Atlassian (JIRA) Python API

## Installation
`pip install simpleatlassian`

## Usage
```python
from simpleatlassian import JIRA

# Make a connection with basic auth
j = JIRA(
    'https://myjirahost.com/jira/rest/',
    username='myuser',
    password='mypw'
)

# Search some issues (get_all collects all pages of a result)
issues = j.get_all(
    'api/2/search',
    params={
        'jql': 'issuetype = Bug'
    },
    resultfield='issues'
)

# Get a board configuration
j.get('agile/1.0/board/1/configuration')
```

Don't forget to check out Atlassian's official documentation:
https://docs.atlassian.com/jira-software/REST/latest/

## Development
### Upload to pip
1. Make sure that the version number has been updated
1. Generate dist files `python setup.py sdist bdist_wheel`
1. Upload to PyPI `twine upload dist/*`
