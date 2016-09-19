from flask import Flask
import fk

app = Flask(__name__)

@app.route("/i/<product>")
def getme(product):
    a = fk.search_for(product, 4)
    return a

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
