from flask import Flask, render_template, redirect, request, session, url_for, send_from_directory
import sqlite3
app=Flask(__name__)
@app.route("/")
def home():    
    return render_template("mecqphome.html")
@app.route("/search", methods=['GET','POST'])
def search():
    if request.method=='POST':
        with sqlite3.connect("test.db") as conn:
            query="SELECT * FROM papers"
            parameterlist=[request.form["scheme"],request.form["branch"],request.form["semester"],request.form["exam_type"],request.form["month"],request.form["year"],request.form["subject_code"],request.form["subject"]]
            p6=f"%{parameterlist[6]}%"
            p7=f"%{parameterlist[7]}%"
            pm=[]
            ifall=1
            ifpriorqueryadded=False
            for i in parameterlist:
                if i!='All' and i!="":
                    ifall=0
                    break
                else:
                    ifall=1
            if ifall!=1:
                query=query+" "+"WHERE"
            if parameterlist[0]!='All':
                ifpriorqueryadded=True
                query=query+" "+"scheme=?"
                pm.append(parameterlist[0])
            if parameterlist[1]!='All':
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"branch=?"
                    pm.append(parameterlist[1])
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"branch=?"
                    pm.append(parameterlist[1])
            if parameterlist[2]!='All':
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"semester=?"
                    pm.append(parameterlist[2])
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"semester=?"
                    pm.append(parameterlist[2])
            if parameterlist[3]!='All':
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"exam_type=?"
                    pm.append(parameterlist[3])
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"exam_type=?"
                    pm.append(parameterlist[3])
            if parameterlist[4]!='All':
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"month=?"
                    pm.append(parameterlist[4])
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"month=?"
                    pm.append(parameterlist[4])
            if parameterlist[5]!='All':
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"year=?"
                    pm.append(parameterlist[5])
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"year=?"
                    pm.append(parameterlist[5])
            if parameterlist[6]!="":
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"subject_code"+" "+"LIKE"+" "+"?"
                    pm.append(p6)
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"subject_code"+" "+"LIKE"+" "+"?"
                    pm.append(p6)
            if parameterlist[7]!="":
                if ifpriorqueryadded:
                    ifpriorqueryadded=True
                    query=query+" "+"AND"+" "+"subject"+" "+"LIKE"+" "+"?"
                    pm.append(p7)
                else:
                    ifpriorqueryadded=True
                    query=query+" "+"subject"+" "+"LIKE"+" "+"?"
                    pm.append(p7)
            cur=conn.cursor()
            cur.execute(query, pm)
            results=cur.fetchall()
            return render_template("mecqpsearch.html", results=results)
    return render_template("mecqpsearch.html")
@app.route("/papers/<name>")
def download(name):
    return send_from_directory('papers',name)
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