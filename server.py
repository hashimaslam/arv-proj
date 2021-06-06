import os
import urllib.request
from flask import Flask  # include the flask library
from flask import render_template,  flash, request, redirect, url_for
from werkzeug.utils import secure_filename
# from Generate import *


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    name = 'Rosalia'
    modelList = ["Inceptionv3","Vgg16","Xception"]
    return render_template('index.html', title='Welcome', username=name, modelList=modelList)


@app.route('/', methods=['POST'])
def upload_image():
    select = request.form.get('model')
    print(select)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print(request.files)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        result =  execute(select,filename)
        return render_template('index.html', filename=filename, result= result)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/submit-form',methods=['POST'])
def submitForm():
    select = request.form.get('model')
    return select

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

def execute(selected,image_name):
    # model_name = selected
    # load_tokanizer = 'D:\\Projects\\test\\arv-proj\\Tokenizers\\'+model_name+'_tokanizer.pkl'
    # tokenizer = load(open(load_tokanizer, 'rb'))
    # max_length = 57
    # model = load_model('D:\\Projects\\test\\arv-proj\\Models\\'+model_name+'_model.h5')
    # photo = extract_features('D:\\Projects\\test\\arv-proj\\static\\uploads\\'+image_name , model_name)
    # description = generate_desc(model, tokenizer, photo, max_length)
    # print(description)
    # description = description.replace('startseq', '')
    # description = description.replace('endseq', '')
    description = "Success"
    return description


if __name__ == '__main__':
    app.run(port=5000, debug=True)
