# code_summarizer
Project on the UrFU software engineering course

# Команда
- Сорокин Андрей Дмитриевич (РИМ-130907)
- Земов Василий Александрович (РИМ-130908)

# Описание проекта
В данном проекте опробована реализация проложения для формирования summary по коду, написанному на языке python.

Summary генерируют 2 модели:
- Модель, найденная на просторах huggingface [SEBIS/code_trans_t5_base_code_documentation_generation_python](https://huggingface.co/SEBIS/code_trans_t5_base_code_documentation_generation_python). Генерирует она крайне плохо, но для отладки web-приложения и API было решено оставить её в качестве заглушки, можно попробовать реализацию другой в файле [model.py](./model.py);
- [Yandex GPT Pro](https://yandex.cloud/ru/docs/foundation-models/concepts/yandexgpt/), которая выдаёт более читаемый результат на русском языке.

# Web-приложение
Поддерживает следующие форматы считывания кода:
- из файла;
- по raw ссылке на файл из github (например: https://raw.githubusercontent.com/ ... /file.py)
- по ссылке на репозиторий github (выполняется клонирование репозитория и поиск всех .py файлов). При этом предоставляется выбор файлов для выполнения их summary.

# API
Для работы api реализованы следующие методы:
1. POST /summarize - принимает на вход code - непосредственно сам код для summary, gpt - флаг для переключения на YandexGPT (True/False). Возвращает summary по переданному методу коду.
2. POST /summarize/raw_url - принимает на вход url - ссылку на код файла из github (например: https://raw.githubusercontent.com/ ... /file.py), gpt - флаг для переключения на YandexGPT (True/False). Возвращает summary по коду из ссылки.
3. POST /summarize/repository - принимает на вход url - ссылка на репозиторий из github, gpt - флаг для переключения на YandexGPT (True/False). Возвращает summary по всем python файлам репозитория. 

# Инструкция по развёртыванию приложения и API
## Устновка необходимых пакетов
```bash
pip install -r requirements.txt
```
## Запуск web-приложения
```bash
streamlit run ./web.py
```
## Использование Yandex GPT
Для того, чтобы использовать приложение с Yandex GPT, необходимо получить token и folder_id. Инструкцию по получению данных переменных можно найти в [документации](https://yandex.cloud/ru/docs/foundation-models/api-ref/authentication) к Yandex GPT.

Для работы приложения token и folder_id необходимо передать в переменные окружения ОС командами:
```bash
export IAM_TOKEN=<ваш токен>
export FOLDER_ID=<id каталога>
```
