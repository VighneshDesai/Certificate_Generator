from datetime import date
from flask import Flask, render_template, request, send_from_directory
import cv2
import os

app = Flask(__name__)

list_of_names = []
clg_name = []

today = date.today()
d2 = today.strftime("%B %d, %Y")



import os



def generate_certificate(name, college, certificate_type):
    if certificate_type.lower() == 'internship':
        template_path = "static/certificate1_internship.png"
    elif certificate_type.lower() == 'workshop':
        template_path = "static/certificate1_workshop.png"
    else:
        # Handle invalid certificate type
        return None

    template = cv2.imread(template_path)
    text_width, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 3, 3)[0]
    x = (template.shape[1] - text_width) // 2
    cv2.putText(template, name.center(60), (0, 560), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0, 1), 3, cv2.LINE_AA)
    cv2.putText(template, d2, (945, 815), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0, 1), 2, cv2.LINE_AA)
    cv2.putText(template, college.center(120), (0, 670), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0, 1), 2, cv2.LINE_AA)

    output_folder = 'static/generated_certificates'
    os.makedirs(output_folder, exist_ok=True)
    output_filename = f'{name}.jpg'
    output_path = f'{output_folder}/{output_filename}'
    cv2.imwrite(output_path, template)

    return output_filename



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        college = request.form['college']
        certificate_type = request.form['certificate-type']

        certificate_filename = generate_certificate(name, college, certificate_type)
        if certificate_filename:
            return render_template('preview.html', certificate_filename=certificate_filename)
        else:
            return render_template('error.html')

    return render_template('index.html', error_message='')

from flask import send_from_directory
'''
@app.route('/download_certificate/<filename>')
def download_certificate_route(filename):
    return send_from_directory('static/generated_certificates', filename, as_attachment=True)

'''
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from flask import send_file

@app.route('/download_certificate/<filename>')
def download_certificate_route(filename):
    certificate_path = f'static/generated_certificates/{filename}'
    pdf_path = f'static/generated_certificates/{filename.split(".")[0]}.pdf'
    
    # Create a PDF document using reportlab
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    c.drawImage(certificate_path, 0, 0, width=A4[1], height=A4[0])
    c.save()
    
    return send_file(pdf_path, as_attachment=True)


@app.route('/generate_certificate', methods=['POST'])
def generate_certificate_route():
    name = request.form['name']
    college = request.form['college']
    certificate_type = request.form['certificate-type']
    
    
if __name__ == '__main__':
    
    app.run(debug=True)
