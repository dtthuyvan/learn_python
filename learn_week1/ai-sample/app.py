from flask import Flask, render_template, request
import my_request_gemini
import my_request_openai
import sumary_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    answer = ""
    question = ""
    if request.method == 'POST':
        question = request.form['question']
        
        if question:
            try:
                answer = my_request_gemini.make_request(question)
            except Exception as e:
                answer = f"An error corrupted: {e}"

    return render_template('question.html', answer=answer, question=question, model_name="Google Gemini", action="gemini")

@app.route('/openai', methods=['GET', 'POST'])
def openai():
    answer = ""
    question = ""
    if request.method == 'POST':
        question = request.form['question']
        
        if question:
            try:
                answer = my_request_openai.make_request(question)
            except Exception as e:
                answer = f"An error corrupted: {e}"

    return render_template('question.html', answer=answer, question=question, model_name="OpenAI", action="openai")

@app.route('/summarize-pdf')
def summarize_pdf_page():
    pdf_filename = 'sample.pdf'
    pdf_folder = app.static_folder
    content = sumary_file.read_file(pdf_folder, pdf_filename)
    print("Content is: " + content)
    summary = ""
    error = ""

    if content:
        prompt = f"Please provide a detailed summary of the following document:\n\n---\n\n{content}"
        
        response = my_request_gemini.make_request(prompt)
        print("Response is: " + response)
        summary = response
    else:
        error = "Could not extract any text from the PDF file. It might be an image-based PDF."

    return render_template('summarize_pdf.html', summary=summary, pdf_filename=pdf_filename, error=error, model_name="Gemini")

if __name__ == '__main__':
    app.run(debug=True)