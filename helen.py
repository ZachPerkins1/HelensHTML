from flask import Flask, render_template, redirect, url_for, request

from random import randrange

app = Flask(__name__)

current_question = 0
score = 0
num_questions = 0
diff = 0

answer = 0

num_amount_ranges = [
    [2, 3],
    [2, 4],
    [3, 5]
]

number_ranges = [
    20,
    40,
    60
]

valid_operations = ['+', '-']

def process_answer(user_answer):
    global score
    if user_answer == answer:
        score += 1


def gen_question():
    max_number = number_ranges[diff] + 1
    max_amount = num_amount_ranges[diff]
    amount = randrange(max_amount[0], max_amount[1]+1)
    eq = []
    for i in range(amount):
        eq.append(str(randrange(1, max_number)))
        eq.append(valid_operations[randrange(0, len(valid_operations))])

    global answer
    answer = solve(eq)
    print answer

    del eq[-1]
    return ' '.join(eq)

def solve(eq):
    total = 0
    operation = "+"
    for item in eq:
        if item in valid_operations:
            operation = item
        else:
            num = int(item)
            total = total + num if operation == '+' else total - num

    return total


@app.route("/")
def home():
    return redirect(url_for("restart"))


@app.route("/start")
def restart():
    return render_template("intro.html")


@app.route("/run", methods=['GET', 'POST'])
def start():
    global diff
    global num_questions
    global current_question

    diff = int(request.form['difficulty'])
    num_questions = int(request.form['number'])
    current_question = 0
    return redirect(url_for('play'))

@app.route("/game", methods=['GET', 'POST'])
def play():
    global current_question
    if request.method == 'GET':
        return render_template('question.html', question_number=current_question+1, problem=gen_question())
    else:
        current_question += 1
        process_answer(int(request.form['answer']))
        if current_question < num_questions:
            return render_template('question.html', question_number=current_question+1, problem=gen_question())
        else:
            formatted_score = str(score) + '/' + str(num_questions)
            return render_template('endscreen.html', score=formatted_score)



app.run()
