from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')

@app.route('/credits/')
def credits():
    return render_template('credits.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/howitworks/')
def howitworks():
    return render_template('howitworks.html')

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
