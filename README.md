# pynamestats
Functions for getting naming statistics in python projects at given path

**get_all_names(**_path_**)** - get all names in python files in a path
**get_top_names(**_path_**,** _top_size=10_**)** - get top names in python files in a path
**get_all_function_names(**_path_**)** - get all function names in python files in a path
**get_top_function_names(**_path_**,** _top_size=10_**)** - get top function names in python files in a path
**get_top_function_verbs(**_path_**,** _top_size=10_**)** - get top verbs in function names in python files in a path

### Code example

```python
import os, collections
from pynamestats import get_top_function_verbs

words = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]

for project in projects:
    path = os.path.join('.', project)
    words += get_top_function_verbs(path)

top_size = 200
print('total %s words, %s unique' % (len(words), len(set(words))))
for word, occurence in collections.Counter(words).most_common(top_size):
    print(word, occurence)
```
