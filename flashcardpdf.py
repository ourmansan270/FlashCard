from pypdf import PdfReader
import random

def read_pdf(file):
    """Read the text content from a PDF file using pypdf."""
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_mcq_from_paragraphs(text):
    """Generate a list of MCQs from the text."""
    paragraphs = text.split('\n\n')
    questions = []

    for paragraph in paragraphs:
        if len(paragraph.strip()) < 100:  # Skip very short paragraphs
            continue
        words = paragraph.split()
        if len(words) < 5:
            continue
        
        # Generate a MCQ
        correct_answer = random.choice(words)
        options = [correct_answer] + random.sample([w for w in words if w != correct_answer], 3)
        random.shuffle(options)

        question = {
            'question': "What is the key concept in this paragraph?",
            'options': options,
            'correct_answer': correct_answer
        }
        questions.append(question)

        if len(questions) >= 10:
            break

    return questions
