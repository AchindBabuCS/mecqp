from flask import Flask, render_template, redirect, request, session, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
ALLOWED_EXTENSIONS={'pdf'}
app=Flask(__name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
@app.route("/submit", methods=['GET','POST'])
def submit():
    if request.method=='POST':
        if 'file' not in request.files:
            return redirect(url_for("submit"))
        file=request.files["file"]
        if file.filename=="":
            return redirect(url_for("submit"))
        if file and allowed_file(file.filename):
            with sqlite3.connect("test.db") as conn:
                cur=conn.cursor()
                submission_date=datetime.today().strftime('%d.%m.%y')
                sublimitstatement='SELECT * FROM submissions WHERE submission_date=?'
                cur.execute(sublimitstatement, (submission_date,))
                no_of_submissions=cur.fetchall()
                if len(no_of_submissions)>9:
                    return redirect(url_for("uploadclosed"))
                else:
                    filename=secure_filename(file.filename)
                    submitstatement='''INSERT INTO submissions(filename,description,status,reason,submission_date)
                                        VALUES (?,?,?,?,?)'''
                    values=[filename,request.form["description"],1,"Pending",submission_date]
                    cur.execute(submitstatement, values)
                    cur.execute("SELECT submission_id FROM submissions WHERE filename=?", (filename,))
                    submission_id=cur.fetchone()[0]
                    conn.commit()
                    file.save(f"submissions/{filename}")
                    return redirect(url_for("aftersubmission", submission_id=submission_id))
        else:
            return redirect(url_for("submit"))    
    return render_template("mecqpsubmit.html")
@app.route("/aftersubmission/<int:submission_id>")
def aftersubmission(submission_id):
    return render_template("mecqpaftersubmissionpage.html", submission_id=submission_id)
@app.route("/uploadclosed")
def uploadclosed():
    return render_template("mecqpuploadclosed.html")
@app.route("/status")
def status():
    with sqlite3.connect("test.db") as conn:
        cur=conn.cursor()
        query="SELECT submission_id, status, reason FROM submissions ORDER BY submission_id DESC LIMIT 20"
        cur.execute(query)
        results=cur.fetchall()
        return render_template("mecqpstatus.html", results=results)
@app.route("/about")
def about():
    return "<p>Work in progress</p>"
@app.route("/admin")
def admin():
    return "<p>Work in progress</p>"