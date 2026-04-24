from bottle import post, request
from datetime import date
import re
import json
import myform_mail

# Загружаем существующие вопросы пользователей из JSON-файла
with open(r'static\questions.json', 'r') as questions_data:
    questions = json.load(questions_data)


@post('/home', method='post')
def my_form():
    """
    Обработчик POST-запроса формы на маршруте /home.

    Выполняет:
    1. Получение данных формы:
       - email пользователя
       - имя пользователя
       - вопрос

    2. Проверку корректности введённых данных:
       - email через функцию check_email()
       - имя (3–100 символов, латиница/цифры)
       - вопрос (должен содержать латинские символы и не содержать кириллицу)

    3. Нормализацию текста вопроса:
       - удаление лишних пробелов

    4. Сохранение данных в JSON:
       - если пользователь уже существует — обновляется имя при необходимости
       - новый вопрос добавляется в список вопросов
       - повторный вопрос не добавляется

    5. Возвращает текстовый ответ пользователю.
    """

    # Регулярные выражения для проверки имени и вопроса
    pattern_name = r'^[A-Za-z0-9]{3,100}$'
    pattern_question = r'^[^А-Яа-яЁё]*[A-Za-z][^А-Яа-яЁё]*$'

    # Получение данных формы
    mail = request.forms.getunicode('ADRESS').strip().lower()
    question = request.forms.getunicode('QUEST').strip().lower()
    name = request.forms.getunicode('USERNAME').strip()

    i = 0

    # Проверка email
    if not myform_mail.check_email(mail):
        return "Error: Invalid email format"

    # Проверка имени:
    # только латиница/цифры, длина 3-100, имя не должно состоять только из цифр
    if not re.match(pattern_name, name) or name == "" or name.isdigit():
        return "Error: Invalid username format"

    # Проверка вопроса
    if not re.match(pattern_question, question):
        return "Error: Invalid question format"

    # Удаление лишних пробелов между словами
    words = question.split(" ")
    while i < len(words):
        if words[i] == '':
            words.remove(words[i])
            continue
        i += 1

    question = " ".join(words)

    # Текущая дата
    today = date.today().strftime("%Y-%m-%d")

    # Флаг повторного вопроса
    already_question = True

    # Поиск пользователя по email
    user_entry = next((item for item in questions if item["mail"] == mail), None)

    if user_entry:
        # Если имя изменилось — обновляем
        if user_entry["name"] != name:
            user_entry["name"] = name

        # Добавляем новый вопрос, если его ещё не было
        if question not in user_entry["questions"]:
            user_entry["questions"].append(question)
            already_question = False
    else:
        # Создание новой записи пользователя
        new_entry = {
            "mail": mail,
            "name": name,
            "questions": [question]
        }

        questions.append(new_entry)
        already_question = False

    # Сохраняем обновлённые данные в файл
    with open(r'static\questions.json', 'w') as questions_data:
        json.dump(questions, questions_data, indent=4)

    # Ответ пользователю
    if already_question:
        return "This question has already been asked, %s. Please wait for a response" % name

    return "Thanks, %s! The answer will be sent to the mail %s. Access Date: %s" % (
        name, mail, today
    )