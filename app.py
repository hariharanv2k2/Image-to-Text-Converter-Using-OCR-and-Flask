from flask import Flask, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from importlib import reload

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/', methods=['POST'])
def submitImage():
    image = request.files['ocrImage']
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)
    
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    
    text_file_path = image_path + '.txt'
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return render_template('textFile.html', text=text, filename=text_file_path)

if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)

