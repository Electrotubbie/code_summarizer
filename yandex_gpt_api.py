import requests
import json
import os

TOKEN = os.getenv('IAM_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')

def get_ya_gpt_result(code):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(TOKEN)
    }

    body = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": "0.1",
            "maxTokens": "10000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Создай summary по написанному python коду по каждой функции и объекту отдельно. "
                        "Верни результат в формате markdown, где имена файлов это заголовки 1 уровня обозначаются #, "
                        "имена функций это заголовки 2 уровня и обозначаются они через ## в markdown, "
                        "а внутри функций summary по ним. Для каждого описания ограничься 10 предложениями. "
                        "Указывай названия функций в файле через заголовки второго уровня ##"
            },
            {
                "role": "user",
                "text": f"{code}"
            }
        ]
    }

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    resp = requests.post(url, json=body, headers=header)
    answer = json.loads(resp.text)
    result = answer['result']['alternatives'][0]['message']['text']
    return result
