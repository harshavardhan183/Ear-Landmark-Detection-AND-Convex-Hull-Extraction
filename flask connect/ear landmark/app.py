from flask import Flask,render_template,flash,request,redirect,url_for, session,jsonify
from keras.models import load_model
import cv2
import keras.utils as image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

import matplotlib.pyplot as plt

def put_landmarks1(pred,img_path,img_result_path):
    
    img_original = plt.imread(img_path)

    for k in range(0,55):  # drop the landmark points on the image
        plt.scatter([pred[k]], [pred[k+55]])

    plt.imshow(img_original)
    plt.savefig(img_result_path)
    plt.close()
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method=='POST':
        im=request.files['ip']
        path = 'static/images/'+im.filename
        im.save(path)
        model1 = load_model('my_model.h5')
        img = cv2.imread(path)
        img = cv2.resize(img, (224, 224)) # first resize the original single image
        cv2.imwrite(path,img)       # save the resized original single image
        img = image.load_img(path)      # load the resized original single image
        X = image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        X = preprocess_input(X)
        for i in range(0,len(X)):

            temp = X[i]
            temp = temp[None,:] # adjust the dimensions for the model
            prediction1 = model1.predict(temp)

        for p in range(len(prediction1[0])):     # adjust the landmark points for 224x224 image (they were normalized in range 0 to 1)

            prediction1[0][p] = int(prediction1[0][p] * 224)
        model2 = load_model('my_model1.h5')
        for i in range(0,len(X)):

            temp = X[i]
            temp = temp[None,:] # adjust the dimensions for the model
            prediction2 = model2.predict(temp)

        for p in range(len(prediction2[0])):     # adjust the landmark points for 224x224 image (they were normalized in range 0 to 1)

            prediction2[0][p] = int(prediction2[0][p] * 224)
        result_path1 = 'static/results1/'+im.filename
        result_path2 = 'static/results2/'+im.filename
        put_landmarks1(prediction1[0],path,result_path1)
        put_landmarks1(prediction2[0],path,result_path2)        # the function to drop landmark points on the image
    return render_template('home.html',filename=im.filename,flag=1)

@app.route('/display_op1/<filename>')
def display_op1(filename):
    return redirect(url_for('static',filename='results1/'+filename))

@app.route('/display_op2/<filename>')
def display_op2(filename):
    return redirect(url_for('static',filename='results2/'+filename))


if __name__=='__main__':
    app.run(debug=True)