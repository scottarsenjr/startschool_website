from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/videos')
def videos():
    return render_template("videos.html")


@app.route('/game')
def game():
    return render_template("game.html")


@app.route('/home')
def literature():
    return render_template("literature.html")


if __name__ == '__main__':
    app.run(debug=True)
