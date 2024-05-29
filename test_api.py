from fastapi.testclient import TestClient
from model import get_model_result
from tools import get_repository_files
from tools import get_repository_file_code
from tools import get_summary_from_filelist
from api import app


raw_url = 'https://raw.githubusercontent.com/Electrotubbie/UrFU_python_course/main/task1_num2text/num_to_text.py'
repo_url = 'https://github.com/Electrotubbie/UrFU_python_course'
with open('./test_directory/code_file.py', 'r', encoding='UTF-8') as f:
    code = f.read()
no_data_error = {'detail': [{'type': 'missing', 'loc': ['body'], 'msg': 'Field required', 'input': None}]}
none_data_error = {'detail': [{'type': 'string_type', 'loc': ['body', 'url'], 'msg': 'Input should be a valid string', 'input': None}]}
none_code_error = {'detail': [{'type': 'missing', 'loc': ['body', 'url'], 'msg': 'Field required', 'input': {'code': None}}]}

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["description"] == ('API для генерации summary на python код. '
                                              'Возможности: простое summary методом summarize, '
                                              'по ссылке на файл в github, по python коду в репозитории.')


def test_summarize():
    response_good = client.post("/summarize", json={'code': code})
    assert response_good.status_code == 200
    assert response_good.json() == {'summary': get_model_result(code)}

    response_good = client.post("/summarize")
    assert response_good.status_code == 422
    assert response_good.json() == no_data_error

    response_no_code = client.post("/summarize/raw_url", json={'code': None})
    assert response_no_code.status_code == 422
    print(response_no_code.json())
    assert response_no_code.json() == none_code_error


def test_summarize_raw_link():
    response = client.post("/summarize/raw_url", json={'url': raw_url})
    assert response.status_code == 200
    assert response.json() == {'summary': get_model_result(get_repository_file_code(raw_url))}

    response_no_data = client.post("/summarize/raw_url")
    assert response_no_data.status_code == 422
    assert response_no_data.json() == no_data_error

    response_no_url = client.post("/summarize/raw_url", json={'url': None})
    print(response_no_url.json())
    assert response_no_url.status_code == 422
    assert response_no_url.json() == none_data_error


def test_summarize_repo():
    response = client.post("/summarize/repository", json={'url': repo_url})
    assert response.status_code == 200
    assert response.json() == {'summary': get_summary_from_filelist(get_repository_files(repo_url))}

    response_no_data = client.post("/summarize/repository")
    assert response_no_data.status_code == 422
    assert response_no_data.json() == no_data_error

    response_no_url = client.post("/summarize/repository", json={'url': None})
    print(response_no_url.json())
    assert response_no_url.status_code == 422
    assert response_no_url.json() == none_data_error
