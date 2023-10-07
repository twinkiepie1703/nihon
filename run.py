from random import shuffle
from flask import Flask, render_template, request
from connector import PostgreSQLConnector

HIDDEN = "**hidden**"
app = Flask(__name__)
dbc = PostgreSQLConnector(database=HIDDEN, host=HIDDEN, port=HIDDEN, password=HIDDEN)

@app.route("/")
def app__index():
    lessons = dbc.lessons.get().exec()
    return render_template("index.html", lessons = lessons)


@app.route("/type", methods = ["POST", "GET"])
def app__type():
    lessons = dbc.lessons.get().exec()
    lesson = request.form.getlist("lesson", type = int)
    return render_template("type.html", lesson = lesson)

@app.route("/quiz", methods = ["POST", "GET"])
def app__quiz():
    questions = []
    lesson = request.form.getlist("lesson", type = int)
    words = dbc.words.any(lesson_id = lesson).exec()
    
    quiz_type = request.form.getlist("quiz_type")
    for each in quiz_type:
        if each == "kana2eng":
            for word in words:
                _quest = {
                    "type": "abcd",
                    "question": word['kana'],
                    "answers": [word['english']],
                    "right_answer": 0
                }
                _w = words[::]
                _w.remove(word)
                shuffle(_w)
                for i in range(3):
                    _quest['answers'].append(_w[i]['english'])
                shuffle(_quest['answers'])
                _quest["right_answer"] = _quest['answers'].index(word['english'])
                questions.append(_quest)

        if each == "kanji2eng":
            for word in words:
                _quest = {
                    "type": "abcd",
                    "question": word['kanji'],
                    "answers": [word['english']],
                    "right_answer": 0
                }
                _w = words[::]
                _w.remove(word)
                shuffle(_w)
                for i in range(3):
                    _quest['answers'].append(_w[i]['english'])
                shuffle(_quest['answers'])
                _quest["right_answer"] = _quest['answers'].index(word['english'])
                questions.append(_quest)

        if each == "end2kana":
            for word in words:
                _quest = {
                    "type": "abcd",
                    "question": word['english'],
                    "answers": [word['kana']],
                    "right_answer": 0
                }
                _w = words[::]
                _w.remove(word)
                shuffle(_w)
                for i in range(3):
                    _quest['answers'].append(_w[i]['kana'])
                shuffle(_quest['answers'])
                _quest["right_answer"] = _quest['answers'].index(word['kana'])
                questions.append(_quest)

        if each == "eng2kanji":
            for word in words:
                _quest = {
                    "type": "abcd",
                    "question": word['english'],
                    "answers": [word['kanji']],
                    "right_answer": 0
                }
                _w = words[::]
                _w.remove(word)
                shuffle(_w)
                for i in range(3):
                    _quest['answers'].append(_w[i]['kanji'])
                shuffle(_quest['answers'])
                _quest["right_answer"] = _quest['answers'].index(word['kanji'])
                questions.append(_quest)

        if each == "eng2kanaorder":
            for word in words:
                _quest = {
                    "type": "buttons",
                    "question": word['english'],
                    "answers": list(word['kana']) + list(word['kanji']),
                    "right_answer": [word['kana'], word['kanji']]
                }
                _quest["answers"] = list(set(_quest["answers"]))
                _quest["right_answer"] = list(set(_quest["right_answer"]))
                _w = words[::]
                _w.remove(word)
                shuffle(_w)
                for each in _w:
                    for chars in list(each['kana']) + list(each['kanji']):
                        if len(_quest["answers"]) < 18:
                            if chars not in _quest["answers"]:
                                _quest["answers"].append(chars)
                        else:
                            break
                    if len(_quest["answers"]) >= 18:
                        break
                shuffle(_quest["answers"])
                questions.append(_quest)

        if each == "eng2writing":
            for word in words:
                _quest = {
                        "type": "write",
                        "question": word['english'],
                        "right_answer": [word['kana'], word['kanji']]
                    }
                questions.append(_quest)
        if each == "selftest":
            for word in words:
                _quest = {
                        "type": "quest",
                        "question": word['english'],
                        "right_answer": [word['kana'], word['kanji']]
                    }
                questions.append(_quest)
    shuffle(questions)

    quest_time = request.form.get("quest_time", 0, int)

    quiz_base = request.form.get("quiz_base")
    is_infinite = False
    quiz_maxtime = 0
    if quiz_base == "count":
        count = request.form.get("count", 0, int)
        print(questions)
        if count > 0:
            questions = questions[:count]
        elif count == -1:
            is_infinite = True
    elif quiz_base == "time":
        quiz_maxtime = request.form.get("quiz_time", 5, int) * 60

    return render_template("quiz.html", questions = questions, quest_time = quest_time, quiz_maxtime = quiz_maxtime, is_infinite = is_infinite)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=21009, debug=True)