import ast
import os
import collections

from nltk import pos_tag

def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])

def is_verb(word):
    """return True if word is a verb, base form"""
    return word is not None and pos_tag([word])[0][1] == 'VB'

def is_special(name):
    """__some_name__ -> True"""
    return isinstance(name, str) and name.startswith('__') and name.endswith('__')

def process_files(dirname, files):
    """generate trees from files in the list"""
    processed = 0
    trees = []
    for file in files:
        if not file.endswith('.py'):
            continue

        filename = os.path.join(dirname, file)

        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            continue

        trees.append(tree)

    return trees

def get_trees(path):
    """generate trees from files in given path"""
    trees = []
    print('generating trees')
    for dirname, dirs, files in os.walk(path, topdown=True):
        dir_trees = process_files(dirname, files)
        trees += dir_trees

    print('total %s trees generated' % len(trees))
    return trees

def get_verbs_from_function_name(function_name):
    """return list of all verbs (base form) in function name"""
    return [word for word in function_name.split('_') if is_verb(word)]

def get_names(tree):
    """return list of all names in a tree"""
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]

def get_function_names(tree):
    """return list of all function names in a tree"""
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_all_names(path):
    """return list of all names in python files in specified path"""
    trees = get_trees(path)
    names = [f for f in flat([get_names(t) for t in trees]) if not is_special(f)]
    return names

def get_top_names(path, top_size=10):
    """return most common names in python files in specified path"""
    names = get_all_names(path)
    return collections.Counter(names).most_common(top_size)

def get_all_function_names(path):
    """return list of all function names inpython files in specified path"""
    trees = get_trees(path)
    function_names = [f for f in flat([get_function_names(t) for t in trees]) if not is_special(f)]
    return function_names

def get_top_function_names(path, top_size=10):
    """return most common function names in python files in specified path"""
    function_names = get_all_function_names(path)
    return collections.Counter(function_names).most_common(top_size)

def get_top_function_verbs(path, top_size=10):
    """return most common verbs in function names in python files in specified path"""
    function_names = get_all_function_names(path)
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in function_names])
    return collections.Counter(verbs).most_common(top_size)

if __name__ == '__main__':
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
