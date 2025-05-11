from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

def generate_pdf(csv_file):
    df = pd.read_csv(csv_file)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)

    for index, row in df.iterrows():
        line = ' | '.join(str(val) for val in row)
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'Empty file', 400

    pdf = generate_pdf(file)
    return send_file(pdf, as_attachment=True, download_name="output.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
