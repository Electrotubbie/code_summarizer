from fastapi import FastAPI
from pydantic import BaseModel
from model import get_model_result
from yandex_gpt_api import get_ya_gpt_result
from tools import israw_py
from tools import get_repository_file_code
from tools import get_repository_files
from tools import get_summary_from_filelist


class Url(BaseModel):
    url: str
    gpt: bool = None


class Code(BaseModel):
    code: str
    gpt: bool = None


app = FastAPI()


@app.get("/")
def root():
    return {'description':
            'API для генерации summary на python код. '
            'Возможности: простое summary методом summarize, '
            'по ссылке на файл в github, по python коду в репозитории.'
            }


@app.post("/summarize")
def summarize(data: Code):
    if data.code:
        if data.gpt:
            assistent = get_ya_gpt_result
        else:
            assistent = get_model_result
        return {'summary': assistent(data.code)}
    else:
        return {'error': 'Пожалуйста, передайте в API '
                '{\'code\': \'Ваш код\', \'gpt\': \'True/False\''}


@app.post("/summarize/raw_url")
def summarize_raw_link(data: Url):
    if israw_py(data.url):
        code = get_repository_file_code(data.url)
        if data.gpt:
            return {'summary': get_ya_gpt_result(code)}
        else:
            return {'summary': get_model_result(code)}
    else:
        return {'error': 'Пожалуйста, передайте в API '
                'raw-ссылку на файл. '
                'Например: https://raw.githubusercontent.com/ ... /file.py'}


@app.post("/summarize/repository")
def summarize_repo(data: Url):
    try:
        files = get_repository_files(data.url)
        summary = get_summary_from_filelist(files, gpt=data.gpt)
        return {'summary': summary}
    except Exception as e:
        return {'error': f'Возникла ошибка {e}'}
