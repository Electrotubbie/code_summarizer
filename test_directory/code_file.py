"""
Модуль для преобразования числа в его прописное выражение.
Используйте модуль следующим образом:

from num_to_text import num_to_text

num_to_text(101) # example
# returns 'сто один'

Для получения помощи напишите: 
help(num_to_text)
"""

t1 = ['один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять']
tsuf = ['дцать', 'надцать', 'ста', 'сот', 'тысяч', #основные литералы
        'миллион', 'миллиард', 'сорок', 'девяносто', 'одна'] # доп литералы

def num_to_text(number: int):
    """
    Parameters: 
        number (int) - исходное число;
    Returns: 
        text_number (str) - прописное выражение исходного числа;
    Функция, получающая на вход число и возвращающая его прописное выражение.
    Выполняется анализ числа путём разложения его на тройки цифр.
    Каждая тройка преобразовывается в прописное выражение через функцию num_part_to_text
    в зависимости от требуемого рода.
    """
    text_number = str()
    iterations = (len(str(number))-1) // 3 # анализ числа на количество троек цифр
    for count in range(iterations, -1, -1):
        num_part = (number % 1000**(count+1)) // 1000**count # извлечение соответсвующей тройки цифр
        thousand_flag = (count == 1)
        mille_flag = (count not in (1, 0))
        if num_part != 0:
            text_num_part = num_part_to_text(num_part, thousand_flag) + ' '
            if mille_flag or thousand_flag:
                if text_num_part[-2] == 'ь' or num_part % 10 == 0: # ... тысяч, ^иллион^ов, ^иллиард^ов
                    text_num_part += tsuf[count+3] + 'ов'*mille_flag
                elif num_part//10 % 10 != 1: # исключение 10, 11, ... , 19
                    if num_part%10 == 1: # ... 1 тысяч^a, ^иллион, ^иллиард
                        text_num_part += tsuf[count+3] + 'а'*thousand_flag
                    elif num_part%10 in (2, 3, 4): # ... 2, 3, 4 тысяч^и, ^иллион^а, ^иллиард^а
                        text_num_part += tsuf[count+3] + 'а'*mille_flag + 'и'*thousand_flag 
            text_number += text_num_part + ' '
    return text_number.rstrip()

def num_part_to_text(number: int, thousand: bool == False):
    """
    Parameters: 
        number (int) - число от 1 до 999 включительно;
        thousand (bool) - признак формирования прописного выражения для тысячного порядка;
    Returns: 
        text_part (str) - прописное выражение исходного числа от 1 до 999 включительно;
    Функция, получающая на вход тройку цифр от 1 до 999 включительно и возвращающая его прописное выражение.
    """
    text_part = str()
    hundred_part = number // 100
    ten_part = number//10 % 10
    one_part = number % 10
    # сотни
    if hundred_part in range(1,10):
        if hundred_part == 1: # сто
            text_part += tsuf[2][:2] + 'о'
        elif hundred_part == 2: # двести
            text_part += t1[hundred_part-1][:2] + 'е' + tsuf[2][:2] + 'и'
        elif hundred_part in (3, 4): # триста, четыреста
            text_part += t1[hundred_part-1] + tsuf[2]
        elif hundred_part in (5, 6, 7, 8, 9): # пятьсот, шестьсот, семьсот, восемьсот, девятьсот
            text_part += t1[hundred_part-1] + tsuf[3]
        text_part += ' '
    # десятки
    if ten_part in range(1,10):
        if ten_part == 1: # числа от 10, 11, ..., 19 включительно
            if one_part == 0: # десять
                text_part += t1[-1]
            elif one_part in (1, 3): # один^надцать, три^надцать
                text_part += t1[one_part-1] + tsuf[1]
            elif one_part == 2: # дв^е^надцать
                text_part += t1[one_part-1][:2] + 'е' + tsuf[1]
            elif one_part in (4, 5, 6, 7, 8, 9): # четыр^надцать, ..., девят^надцать
                text_part += t1[one_part-1][:-1] + tsuf[1]
        elif ten_part in (2, 3): # два^дцать, три^дцать
            text_part += t1[ten_part-1] + tsuf[0]
        elif ten_part == 4: # сорок
            text_part += tsuf[7]
        elif ten_part == 9: # девяносто
            text_part += tsuf[8]
        elif ten_part in (5, 6, 7, 8): # пять^десят, шесть^десят, семь^десят, восемь^десят
            text_part += t1[ten_part-1] + t1[-1][:-1]
        text_part += ' '
    # единицы
    if ten_part != 1 and one_part != 0: # добавляем t1 ко всем числам, кроме 10, 11, ..., 19 включительно
        if thousand and one_part == 1: # одна тысяч^а
            text_part += tsuf[9]
        elif thousand and one_part == 2: # две тысяч^и
            text_part += t1[one_part-1][:-1] + 'е'
        else:
            text_part += t1[one_part-1] # всё остальное 
    return text_part.rstrip()