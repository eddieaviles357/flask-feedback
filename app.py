
from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.config.update(

)


@app.route('/')
def home():
    """ Home route """
    return render_template("index.html")