from tools import get_repository_file_code
from tools import israw_py
from tools import find_all_py


file_url = 'https://raw.githubusercontent.com/Electrotubbie/UrFU_python_course/main/task1_num2text/num_to_text.py'


def test_get_repository_file_code():
    with open('./test_directory/code_file.py', 'r', encoding='UTF-8') as file:
        code = file.read()
    assert get_repository_file_code(file_url) == code


def test_israw():
    only_raw_s = 'https://raw.githubusercontent.com/'
    only_raw = 'http://raw.githubusercontent.com/'
    raw_py_s = 'https://raw.githubusercontent.com/.py'
    raw_py = 'http://raw.githubusercontent.com/.py'
    not_raw_s = 'https://www.google.com/'
    not_raw = 'http://www.google.com/'
    not_raw_py_withot_http = 'www.google.com/.py'
    assert not israw_py(only_raw_s)
    assert not israw_py(only_raw)
    assert not israw_py(raw_py_s)
    assert not israw_py(raw_py)
    assert not israw_py(not_raw_s)
    assert not israw_py(not_raw)
    assert not israw_py(not_raw_py_withot_http)
    assert not israw_py(file_url[:-2] + 'sh')
    assert israw_py(file_url)


def test_find_all_py():
    dir = './test_directory'
    result = {
        'test_directory': {
            'py': ['code_file.py'],
            'dir': [{
                'empty_but_with_pydir': {
                    'py': [],
                    'dir': [{
                        'pydir': {
                            'py': ['file1.py', 'file2.py'],
                            'dir': []
                        }
                    }]
                }
            }]
        }
    }
    assert find_all_py(dir) == result
