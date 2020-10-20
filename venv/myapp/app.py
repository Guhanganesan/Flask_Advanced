from flask import Flask, render_template, url_for, request
app = Flask(__name__)

List = ["Raja","Anbu","Ganesan","Guhan"]

@app.route('/test')
def test():
    return "Hi Raja"

@app.route('/')
def index():
    name = "Guhan Ganesan"
    return render_template('index.html',user=name)

@app.route('/concepts')
def concept():
    name = "Guhan Ganesan"
    return render_template('concepts.html', user=name, len=len(List), mylist=List)
	
if __name__=="__main__":
  app.run(debug = True)
