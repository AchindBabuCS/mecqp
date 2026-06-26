from flask import Flask, render_template, redirect, request, session, url_for
app=Flask(__name__)
@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        return
    return render_template("mecqphome.html")