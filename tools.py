import re
import requests
import git
import os
from model import get_model_result
from yandex_gpt_api import get_ya_gpt_result


REPO_TO_SUM_PATH = './repo2sum'


def get_repository_files(repo_url, branch=None, path_to_save=REPO_TO_SUM_PATH):
    # в процессе создания web и api нужно проработать более корректно эту функцию
    '''
    Функция для парсинга всех файлов и директорий с python кодом в репозитории.

    repo_url: https адрес для клонирования репозитория
    '''
    if os.path.exists(path_to_save):
        os.system(f'rm -rf {path_to_save}')
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
            if code != '404: Not Found':
                return code
            else:
                return None
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
        #TODO
    '''
    # создаём словарь, в который будем копить все наши директории и .py файлы
    py_files = dict()
    # определяем формат словаря
    py_files = list()
    # ищем директории и .py файлы на текущем пути
    dir_list = sorted(os.listdir(path))
    for d in dir_list:
        # извлекаем полный путь до рассматриваемого файла/папки
        full_path = os.path.join(path, d)
        # если это .py файл, то записываем его в список
        if os.path.isfile(full_path) and d.endswith('.py'):
            py_files.append(full_path)
        # если это директория, то вновь вызываем текущую функцию и проверяем директорию
        elif os.path.isdir(full_path):
            check_dir = find_all_py(full_path)
            if check_dir:
                py_files.extend(check_dir)
    # если совсем ничего не нашли (ни .py файлы, ни директории с ними), то возвращаем None,
    # иначе словарь с директориями и .py файлами
    if len(py_files) != 0:
        return py_files
    else:
        return None


def get_summary_from_filelist(filelist, gpt=False):
    if gpt:
        assistent = get_ya_gpt_result
    else:
        assistent = get_model_result

    summary = str()
    for file in filelist:
        with open(file, 'r', encoding='UTF-8') as f:
            result = assistent(f.read())
            summary += f'# {file.split("/")[-1]}\n\n{result}'
    return summary
