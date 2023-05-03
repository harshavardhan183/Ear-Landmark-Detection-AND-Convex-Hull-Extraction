from flask import Flask,render_template,flash,request,redirect,url_for, session,jsonify

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

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
    return render_template('home.html')


if __name__=='__main__':
    app.run(debug=True)