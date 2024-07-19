from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        questions = parse_file(file)
        if not questions:
            return "No valid questions found in the file.", 400
        return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form
    correct_answers = request.form.getlist('correct_answers')
    if not correct_answers:
        return "No questions were found to check the answers against.", 400
    score = calculate_score(answers, correct_answers)
    return render_template('result.html', score=score, total=len(correct_answers))

def parse_file(file):
    questions = []
    try:
        lines = file.readlines()
        if len(lines) % 7 != 0:
            raise ValueError("File content is not formatted correctly.")

        for i in range(0, len(lines), 7):
            question = {
                'text': lines[i].decode('utf-8').strip(),
                'options': [lines[i+1].decode('utf-8').strip(), lines[i+2].decode('utf-8').strip(),
                            lines[i+3].decode('utf-8').strip(), lines[i+4].decode('utf-8').strip()],
                'answer': lines[i+5].decode('utf-8').strip().split(": ")[1]
            }
            questions.append(question)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []
    return questions

def calculate_score(answers, correct_answers):
    score = 0
    for i, correct_answer in enumerate(correct_answers):
        if answers.get(f'question_{i+1}') == correct_answer:
            score += 1
    return score

if __name__ == '__main__':
    app.run(debug=True)
