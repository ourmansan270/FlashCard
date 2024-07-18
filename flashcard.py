import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox

def read_document(filename):
    """Read and return the content of the specified text document."""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def generate_mcq_quiz(content):
    """Generate a simple MCQ quiz based on the content of the text document."""
    questions = content.strip().split('\n\n')
    score = 0

    for q in questions:
        lines = q.strip().split('\n')
        
        if len(lines) < 6:
            print("Error: Invalid question format. Each question must have a question, 4 options, and a correct answer.")
            continue

        question = lines[0]
        options = lines[1:5]
        correct_answer_line = lines[5].split(': ')

        if len(correct_answer_line) != 2:
            print("Error: Invalid correct answer format.")
            continue

        correct_answer = correct_answer_line[1].strip()

        print(f"\n{question}")
        for i, option in enumerate(options):
            print(option)
        
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {correct_answer}")

    print(f"\nQuiz completed! Your score: {score}/{len(questions)}")

def upload_document():
    """Upload a document using file dialog and return its content."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a Text Document",
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        print("No file selected.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as src_file:
            content = src_file.read()
        messagebox.showinfo("Success", f"Document '{os.path.basename(file_path)}' uploaded successfully!")
        return content
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload document: {e}")
        return None

def main():
    print("Welcome to the Exam Helper!")
    
    content = upload_document()
    if content:
        generate_mcq_quiz(content)

if __name__ == "__main__":
    main()
