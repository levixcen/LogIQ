import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.main import run_agent, call_azure_openai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'logfile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['logfile']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    try:
        report = run_agent(filepath)
        return jsonify({'report': report})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    question = data.get('question', '').strip()
    report_context = data.get('report_context', '').strip()
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    if not report_context:
        return jsonify({'error': 'No report context provided'}), 400
    
    prompt = f"""
    You are a senior digital forensic analyst. A forensic investigation report 
    has already been generated and is shown below. The analyst is asking a 
    follow-up question about this specific incident.

    FORENSIC REPORT:
    {report_context}

    ANALYST QUESTION:
    {question}

    Answer the question based strictly on the evidence in the report above.
    Be concise and specific. Do not use markdown formatting, no asterisks, 
    no hashtags. Use plain text only. If the answer requires a list, 
    use numbers like 1. 2. 3.
    If the question cannot be answered from the report, say so clearly.
    """
    
    try:
        response = call_azure_openai(prompt)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 