from flask import Flask, render_template, redirect, request, session, url_for
app=Flask(__name__)
@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        return
    return render_template("mecqphome.html")
@app.route("/search")
def search():
    return "<p>Work in progress</p>"
@app.route("/submit")
def submit():
    return "<p>Work in progress</p>"
@app.route("/status")
def status():
    return "<p>Work in progress</p>"
@app.route("/about")
def about():
    return "<p>Work in progress</p>"
@app.route("/admin")
def admin():
    return "<p>Work in progress</p>"
