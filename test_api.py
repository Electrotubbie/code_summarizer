from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["description"] == ("API для генерации summary на python код. "
    "Возможности: простое summary методом summarize, по ссылке на файл в github, по python коду в репозитории.")

# def test_summarize():
#     response = client.post("/summarize")
#     assert response == {'error': 'Пожалуйста, передайте в API '
#                 '{\'code\': \'Ваш код\', \'gpt\': \'True/False\''}

