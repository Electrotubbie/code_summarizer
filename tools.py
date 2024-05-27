import re
import requests
import git
import os


REPO_TO_SUM_PATH = './repo2sum'


def get_repository_files(repo_url, branch=None, path_to_save=REPO_TO_SUM_PATH):
    # в процессе создания web и api нужно проработать более корректно эту функцию
    '''
    Функция для парсинга всех файлов и директорий с python кодом в репозитории.

    repo_url: https адрес для клонирования репозитория
    '''
    git.Repo.clone_from(repo_url, path_to_save)
    repo = git.Repo(path_to_save)
    if branch:
        repo.git.checkout(branch)
    py_files = find_all_py(path_to_save)
    return py_files


def get_repository_file_code(file_url):
    '''
    Функция для парсинга кода из .py файлов в репозитории.

    file_url: raw ссылка на файл
    '''
    if israw_py(file_url):  # проверка корректности ссылки
        try:
            code = requests.get(file_url).text
            return code
        except Exception as e:
            print(e)
            return None
    else:
        return None


def israw_py(url):
    '''
    Функция для проверки правильности ссылки на файл в github.
    '''
    http_pattern = r"http(s)?:\/\/"
    raw_pattern = r"^((http(s)?:\/\/)?raw.githubusercontent.com\/){1}[A-z\S]+(\.py)$"
    if len(re.findall(http_pattern, url)) == 1:  # проверка на повторение https:// только однажды
        if re.match(raw_pattern, url):  # проверка на корректность ссылки на .py файл
            return True
    # assert ValueError('Адрес для чтения файла из github не подходит. '
    #                   '\nНеобходимо, чтоб он начинался с https://raw.githubusercontent.com/. '
    #                   f'\nАдрес: {url} ')
    return False


def find_all_py(path):
    '''
    Функция для рекурсивного поиска всех .py файлов в директории.

    path: путь к директории (например '.' или './dir').

    Returns:
    {
        'dirname1_1': {
            'dir': [
                {
                    'dirname1_2': {
                        'dir': [{}, {}, ... directory list with py files]
                        'py': [py files from dirname1_2]
                    }
                },
                {
                    'dirname1_3': {
                        'dir': [{}, {}, ... directory list with py files]
                        'py': [py files from dirname1_3]
                    }
                }
            ]
            'py': [py files from dirname1_1]
        }
    }
    '''
    # создаём словарь, в который будем копить все наши директории и .py файлы
    py_files = dict()
    # достаём из пути к директории её имя для удобного сохранения в словарь
    dir_name = os.path.basename(path)
    # определяем формат словаря
    py_files[dir_name] = {'py': [], 'dir': []}
    # ищем директории и .py файлы на текущем пути
    for d in os.listdir(path):
        # извлекаем полный путь до рассматриваемого файла/папки
        full_path = os.path.join(path, d)
        # если это .py файл, то записываем его в список
        if os.path.isfile(full_path) and d.endswith('.py'):
            py_files[dir_name]['py'].append(d)
        # если это директория, то вновь вызываем текущую функцию и проверяем директорию
        elif os.path.isdir(full_path):
            check_dir = find_all_py(full_path)
            if check_dir:
                py_files[dir_name]['dir'].append(check_dir)
    # если совсем ничего не нашли (ни .py файлы, ни директории с ними), то возвращаем None,
    # иначе словарь с директориями и .py файлами
    if len(py_files[dir_name]['dir']) != 0 or len(py_files[dir_name]['py']) != 0:
        return py_files
    else:
        return None
