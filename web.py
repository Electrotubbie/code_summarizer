import streamlit as st
from tools import israw_py
from tools import get_repository_file_code
from tools import get_repository_files
from model import get_model_result
from yandex_gpt_api import get_ya_gpt_result
import os

# TODO
# 1) Сделать кнопку загрузки в md файл
# 2) Подумать над переключателем md -> preview
# 3) протестить всё до конца 

st.title("Try to summarize code")

if st.toggle("YandexGPT"):
    os.system('. ./token.sh')
    assistent = get_ya_gpt_result
else:
    assistent = get_model_result

uploaded_file = st.file_uploader("Загрузите файл с python кодом или")

if uploaded_file:
    url = st.text_input("Введите raw ссылку на файл из github или ссылку для клонирования целого репозитория", 
                        value=None, disabled=True)
else:
    url = st.text_input("Введите raw ссылку на файл из github или ссылку для клонирования целого репозитория")

st.text('Например:\n'
        '\thttps://raw.githubusercontent.com/ ... file.py\n'
        '\thttps://github.com/...')

if url:
    # st.text(f'Введённый адрес: {url}')
    if israw_py(url):
        code = get_repository_file_code(url)
    else:
        try:
            filelist = get_repository_files(url)
        except Exception as e:
            print(f'Проверьте правильность ввода ссылки, а также рассмотрите ошибку: {e}')
        else:
            chx = [st.checkbox(file) for file in filelist]

if st.button("Summarize!"):
    if uploaded_file:
        if uploaded_file.name.endswith('.py'):
            code = uploaded_file.read().decode()
            result = assistent(code)
            st.text(f'# {uploaded_file.name}\n\n{result}')
    elif url:
        if israw_py(url):
            result = assistent(code)
            st.text(f'# {url.split("/")[-1]}\n\n{result}')
        else:
            for i, ch in enumerate(chx):
                if ch:
                    file = filelist[i]
                    with open(file, 'r', encoding='UTF-8') as f:
                        result = assistent(f.read())
                        st.text(f'# {file.split("/")[-1]}\n\n{result}')
    else:
        st.text('Загрузите файл или введите ссылку')
