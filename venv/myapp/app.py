from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route('/test')
def test():
    return "Hi Raja"

@app.route('/')
def index():
    name = "Guhan Ganesan"
    return render_template('index.html', user=name)
 
	
if __name__=="__main__":
  app.run(debug = True)
