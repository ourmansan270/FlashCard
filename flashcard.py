# app.py

import os
import random
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pypdf
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download NLTK data (run this once)
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def read_document(filename):
    """Read and return the content of the specified document."""
    content = ""
    if filename.lower().endswith('.txt'):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    elif filename.lower().endswith('.pdf'):
        reader = pypdf.PdfReader(filename)
        for page in reader.pages:
            content += page.extract_text()
    else:
        raise ValueError("Unsupported file format. Please upload a .txt or .pdf file.")
    return content

def extract_keywords(text, num_keywords=5):
    """Extract keywords from the text."""
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    keywords = [word for word, count in word_counts.most_common(num_keywords)]
    return keywords

def generate_mcq_from_paragraphs(content):
    """Generate MCQs based on paragraphs in the document."""
    paragraphs = content.strip().split('\n\n')
    questions = []

    for para in paragraphs:
        sentences = sent_tokenize(para)
        if not sentences:
            continue

        for sentence in sentences:
            keywords = extract_keywords(sentence, num_keywords=4)
            if not keywords:
                continue

            question = f"What is a key concept from the following sentence: \"{sentence}\""
            correct_answer = random.choice(keywords)

            # Ensure we have enough keywords to sample from
            num_options = min(len(keywords), 4)
            options = [correct_answer] + random.sample(keywords, num_options - 1)
            random.shuffle(options)

            questions.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer
            })

    return questions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Read and process the document
            content = read_document(file_path)
            questions = generate_mcq_from_paragraphs(content)

            return render_template('quiz.html', questions=questions)
    
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
