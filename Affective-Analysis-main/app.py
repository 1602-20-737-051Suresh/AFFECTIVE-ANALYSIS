from flask import Flask, render_template,url_for#,Response

app = Flask(__name__) 

@app.route("/")
def home():
    return render_template("Start.html", url_for=url_for)

@app.route("/main")
def main():
    return render_template("index.html", url_for=url_for)

@app.route("/HELP")
def help():
    return render_template("HELP.html", url_for=url_for)

@app.route("/about")
def about():
    return render_template("ABOUT.html", url_for=url_for)
import video,audio