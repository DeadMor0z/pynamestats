# pynamestats
Function for getting naming statistics in python projects at given path


### Code example

```python
import os, collections
from pynamestats import get_top_verbs_in_path

words = []
projects = [
    'yamdb',
]

for project in projects:
    path = os.path.join('.', project)
    words += get_top_verbs_in_path(path)

top_size = 200
print('total %s words, %s unique' % (len(words), len(set(words))))
for word, occurence in collections.Counter(words).most_common(top_size):
    print(word, occurence)
```
