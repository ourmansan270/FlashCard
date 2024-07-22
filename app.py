from flask import Flask, render_template, request, redirect, session
import secrets

app = Flask(__name__)

# Generate a secure random key
app.config['SECRET_KEY'] = secrets.token_hex(32)

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
        
        session['questions'] = questions
        session['current_question'] = 0
        session['answers'] = [None] * len(questions)
        
        return redirect('/quiz')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions')
    if not questions:
        return redirect('/')  # Redirect to home if questions are not in session
    
    current_question_index = int(session.get('current_question', 0))
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer:
            # Save the user's answer in the session
            session['answers'][current_question_index] = user_answer

        if 'next' in request.form:
            current_question_index += 1
            if current_question_index < len(questions):
                session['current_question'] = current_question_index
            else:
                # All questions have been answered, redirect to results
                return redirect('/result')

        # Always redirect to /quiz to render the current question
        return redirect('/quiz')
    
    if current_question_index >= len(questions):
        return redirect('/result')  # Redirect to results if index is out of bounds
    
    question = questions[current_question_index]
    return render_template('quiz.html', question=question, index=current_question_index, total=len(questions))


@app.route('/result')
def result():
    questions = session.get('questions')
    answers = session.get('answers')
    
    if not questions or not answers:
        return redirect('/')
    
    correct_answers = [q['answer'] for q in questions]
    score = sum(1 for i in range(len(answers)) if answers[i] == correct_answers[i])
    total_questions = len(questions)
    
    return render_template('result.html', score=score, total=total_questions)

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

if __name__ == '__main__':
    app.run(debug=True)
