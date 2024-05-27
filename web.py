import streamlit as st
from tools import israw_py
from tools import get_repository_file_code
from tools import get_repository_files
from model import get_model_result


st.title("Try to summarize code")

uploaded_file = st.file_uploader("или загрузите файл с python кодом")

if uploaded_file:
    url = st.text_input("Введите raw ссылку на файл из github или https ссылку для клонирования целого репозитория", disabled=True)
else:
    url = st.text_input("Введите raw ссылку на файл из github или https ссылку для клонирования целого репозитория")

if url:
    st.text(f'Введённая ссылка: {url}')

st.text('Например:\n'
        '\thttps://raw.githubusercontent.com/ ... file.py\n'
        '\thttps://github.com/ ... .git')


if st.button("Summarize!"):
    if uploaded_file:
        if uploaded_file.name.endswith('.py'):
            code = uploaded_file.read().decode()
            result = get_model_result(code)
            st.text(f'# {uploaded_file.name}\n\n{result}')
    elif url:
        if israw_py(url):
            code = get_repository_file_code(url)
            result = get_model_result(code)
            st.text(f'# {url.split("/")[-1]}\n\n{result}')
        else:
            st.text('Иерархическая структура файлов для саммаризации кода')
    else:
        st.text('Загрузите файл или введите ссылку')
