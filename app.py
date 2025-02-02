from flask import Flask, render_template, request, redirect, url_for, session
import ollama
from ollama import chat
from prompt_library import PROMPT_LIBRARY

import pydantic
from typing import List, Dict, Any

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production!

# Default model constant (will be overwritten by user selection)
MODEL_NAME = "qwen2.5:3b"

class QuestionSchema(pydantic.BaseModel):
    question: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str

    def __str__(self):
        return f"{self.question} \n A: {self.option_1} \n B: {self.option_2} \n C: {self.option_3} \n D: {self.option_4}"

def ask_question(model, messages):
    response_text = ollama.chat(
        model=model,
        messages=messages,
        format=QuestionSchema.model_json_schema(),
    )['message']['content']

    question_count = len(messages)  # count messages (system message + previous Q&A)
    if question_count >= 10:
        return None, []
    
    output = QuestionSchema.model_validate_json(response_text)
    
    return output.question, [output.option_1, output.option_2, output.option_3, output.option_4]

@app.route('/')
def index():
    """Landing page."""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    """Initialize the session and start the questionnaire."""
    # Retrieve model and system prompt from the form.
    model = request.form.get('model')
    system_prompt = PROMPT_LIBRARY["QUESTIONING"].format(system_prompt=request.form.get('system_prompt'))
    
    # Save the chosen model in the session.
    session['model'] = model
    
    # Initialize messages with the custom system prompt.
    session['messages'] = [{"role": "system", "content": system_prompt}]
    session['response_summary'] = []  # To store question/answer pairs.
    session['question_count'] = 0     # To count how many questions have been answered.
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        # Determine the answer from the form submission.
        answer = None
        if 'response' in request.form:
            answer = request.form['response']
        elif 'custom_response' in request.form:
            answer = request.form['custom_response']
        
        # Retrieve the current question from the session.
        current_question = session.get('current_question')
        if not current_question:
            return redirect(url_for('index'))
        
        # Update conversation history and response summary.
        messages = session.get('messages', [])
        summary = session.get('response_summary', [])
        summary.append({'question': current_question, 'answer': answer})
        messages.append({"role": "assistant", "content": current_question})
        messages.append({"role": "user", "content": answer})
        session['messages'] = messages
        session['response_summary'] = summary
        
        # Increment the question count.
        session['question_count'] = session.get('question_count', 0) + 1
        
        # After 10 questions, go to summary.
        if session['question_count'] >= 10:
            return redirect(url_for('summary'))
        
        # Redirect to GET so a new question is generated.
        return redirect(url_for('question'))
    
    # For a GET request, generate a new question based on past messages.
    messages = session.get('messages', [])
    # Use the user-selected model stored in the session.
    model = session.get('model', MODEL_NAME)
    question_text, options = ask_question(model, messages)
    if question_text is None:
        return redirect(url_for('summary'))
    
    # Store the current question in the session so that we can pair it with the response.
    session['current_question'] = question_text
    return render_template('question.html', question=question_text, options=options)

@app.route('/summary')
def summary():
    """Display the summary of all questions and responses."""
    messages = session.get('response_summary', [])
    return render_template('summary.html', messages=messages)

@app.route('/restart', methods=['POST'])
def restart():
    """Clear the session and restart the questionnaire."""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
