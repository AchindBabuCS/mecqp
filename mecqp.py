from flask import Flask, render_template, redirect, request, session, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import sqlite3
import os
ALLOWED_EXTENSIONS={'pdf'}
app=Flask(__name__)
app.secret_key=os.environ.get('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
passwordhash=os.environ.get('PASSWORD_HASH')
database=os.environ.get('DATABASE')
csrf=CSRFProtect(app)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_submission():
    with sqlite3.connect(database) as conn:
        subimssionsquery="SELECT * FROM submissions WHERE status=1"
        cur=conn.cursor()
        cur.execute(subimssionsquery)
        return cur.fetchall()
@app.route("/")
def home():    
    return render_template("mecqphome.html")
@app.route("/search", methods=['GET','POST'])
def search():
    if request.method=='POST':
        with sqlite3.connect(database) as conn:
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
            with sqlite3.connect(database) as conn:
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
                    submission_id=cur.lastrowid
                    savefilename=str(submission_id)+"_"+filename
                    cur.execute("UPDATE submissions SET filename=? WHERE submission_id=?",(savefilename,submission_id))
                    conn.commit()
                    file.save(f"submissions/{savefilename}")
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
    with sqlite3.connect(database) as conn:
        cur=conn.cursor()
        query="SELECT submission_id, status, reason FROM submissions ORDER BY submission_id DESC LIMIT 20"
        cur.execute(query)
        results=cur.fetchall()
        return render_template("mecqpstatus.html", results=results)
@app.route("/about")
def about():
    with sqlite3.connect(database) as conn:
        announcementquery="SELECT message, message_date FROM adminmessages ORDER BY message_id DESC"
        cur=conn.cursor()
        cur.execute(announcementquery)
        latestmessage=cur.fetchone()
        return render_template("mecqpabout.html", latestmessage=latestmessage)
@app.route("/adminlogin", methods=['GET','POST'])
def adminlogin():
    with sqlite3.connect(database) as conn:
        logincheckquery='SELECT * FROM loginattempts WHERE login_date=? AND ip_address=?'
        loginattemptidaddress=request.remote_addr
        loginattemptdate=datetime.today().strftime('%d.%m.%y')
        cur=conn.cursor()
        cur.execute(logincheckquery,(loginattemptdate,loginattemptidaddress))
        loginattempts=cur.fetchall()
        if len(loginattempts)>5:
            return render_template("adminlockedout.html")
        else:
            wrongpassword=False
            if request.method=='POST':
                if check_password_hash(passwordhash,request.form['adminloginpassword']):
                    session['admin']=True
                    return redirect(url_for("admin"))
                else:
                    loginattemptquery='''INSERT INTO loginattempts(login_date,ip_address) VALUES(?,?)'''
                    cur=conn.cursor()
                    cur.execute(loginattemptquery,(loginattemptdate,loginattemptidaddress))
                    conn.commit()
                    wrongpassword=True
                    return render_template("mecqpadminlogin.html", wrongpassword=wrongpassword)
            return render_template("mecqpadminlogin.html")
@app.route("/admin", methods=['GET','POST'])
def admin():
    if session.get("admin"):
        modifymode=False
        deletemode=False
        if request.method=='POST':
            submissions=get_submission()
            if 'upload' in request.form:
                if 'newfile' not in request.files:
                    return redirect(url_for("admin"))
                file=request.files["newfile"]
                fname=file.filename
                if file.filename=="":
                    return redirect(url_for("admin"))
                if file and allowed_file(fname):
                    with sqlite3.connect(database) as conn:
                        newpaperquery='''INSERT INTO papers (scheme,branch,semester,exam_type,month,year,subject_code,subject,filename) VALUES(?,?,?,?,?,?,?,?,?)'''
                        newpaperparameter=[request.form["newscheme"],request.form["newbranch"],request.form["newsemester"],request.form["newexam_type"],request.form["newmonth"],request.form["newyear"],request.form["newsubject_code"],request.form["newsubject"],fname]
                        file.save(f"papers/{fname}")
                        cur=conn.cursor()
                        cur.execute(newpaperquery, newpaperparameter)
                        conn.commit()
                        return redirect(url_for("admin"))
            if 'modifybutton' in request.form:
                modifymode=True
                return render_template("mecqpadmin.html", modifymode=modifymode, submissions=submissions)
            if 'modifysearch' in request.form:
                modifymode=True
                with sqlite3.connect(database) as conn:
                    modifysearchquery="SELECT * FROM papers"
                    modifysearchparameterlist=[request.form["modifysearchscheme"],request.form["modifysearchbranch"],request.form["modifysearchsemester"],request.form["modifysearchexam_type"],request.form["modifysearchmonth"],request.form["modifysearchyear"]]
                    modifysearchpm=[]
                    ifall=1
                    ifpriorqueryadded=False
                    for i in modifysearchparameterlist:
                        if i!='All':
                            ifall=0
                            break
                        else:
                            ifall=1
                    if ifall!=1:
                        modifysearchquery=modifysearchquery+" "+"WHERE"
                    if modifysearchparameterlist[0]!='All':
                        ifpriorqueryadded=True
                        modifysearchquery=modifysearchquery+" "+"scheme=?"
                        modifysearchpm.append(modifysearchparameterlist[0])
                    if modifysearchparameterlist[1]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"AND"+" "+"branch=?"
                            modifysearchpm.append(modifysearchparameterlist[1])
                        else:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"branch=?"
                            modifysearchpm.append(modifysearchparameterlist[1])
                    if modifysearchparameterlist[2]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"AND"+" "+"semester=?"
                            modifysearchpm.append(modifysearchparameterlist[2])
                        else:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"semester=?"
                            modifysearchpm.append(modifysearchparameterlist[2])
                    if modifysearchparameterlist[3]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"AND"+" "+"exam_type=?"
                            modifysearchpm.append(modifysearchparameterlist[3])
                        else:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"exam_type=?"
                            modifysearchpm.append(modifysearchparameterlist[3])
                    if modifysearchparameterlist[4]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"AND"+" "+"month=?"
                            modifysearchpm.append(modifysearchparameterlist[4])
                        else:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"month=?"
                            modifysearchpm.append(modifysearchparameterlist[4])
                    if modifysearchparameterlist[5]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"AND"+" "+"year=?"
                            modifysearchpm.append(modifysearchparameterlist[5])
                        else:
                            ifpriorqueryadded=True
                            modifysearchquery=modifysearchquery+" "+"year=?"
                            modifysearchpm.append(modifysearchparameterlist[5])
                    cur=conn.cursor()
                    cur.execute(modifysearchquery,modifysearchpm)
                    modifysearchresults=cur.fetchall()
                    return render_template("mecqpadmin.html", modifymode=modifymode, modifysearchresults=modifysearchresults, submissions=submissions)
            if 'updatesubmit' in request.form:
                modifymode=False
                with sqlite3.connect(database) as conn:
                    modifysubmitquery="UPDATE papers"
                    modifysubmitparameterlist=[request.form['updatescheme'],request.form['updatebranch'],request.form['updatesemester'],request.form['updateexam_type'],request.form['updatemonth'],request.form['updateyear'],request.form['updatepaperid']]
                    modifysubmitpm=[]
                    ifall=1
                    ifpriorqueryadded=False
                    for i in range(len(modifysubmitparameterlist)-1):
                        if modifysubmitparameterlist[i]!='All':
                            ifall=0
                            break
                        else:
                            ifall=1
                    if ifall==1:
                        return render_template("mecqpadmin.html", modifymode=modifymode, submissions=submissions)
                    else:
                        modifysubmitquery=modifysubmitquery+" "+"SET"
                        if modifysubmitparameterlist[0]!='All':
                            ifpriorqueryadded=True
                            modifysubmitquery=modifysubmitquery+" "+"scheme=?"
                            modifysubmitpm.append(modifysubmitparameterlist[0])
                        if modifysubmitparameterlist[1]!='All':
                            if ifpriorqueryadded:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+","+" "+"branch=?"
                                modifysubmitpm.append(modifysubmitparameterlist[1])
                            else:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+" "+"branch=?"
                                modifysubmitpm.append(modifysubmitparameterlist[1])
                        if modifysubmitparameterlist[2]!='All':
                            if ifpriorqueryadded:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+","+" "+"semester=?"
                                modifysubmitpm.append(modifysubmitparameterlist[2])
                            else:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+" "+"semester=?"
                                modifysubmitpm.append(modifysubmitparameterlist[2])
                        if modifysubmitparameterlist[3]!='All':
                            if ifpriorqueryadded:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+","+" "+"exam_type=?"
                                modifysubmitpm.append(modifysubmitparameterlist[3])
                            else:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+" "+"exam_type=?"
                                modifysubmitpm.append(modifysubmitparameterlist[3])
                        if modifysubmitparameterlist[4]!='All':
                            if ifpriorqueryadded:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+","+" "+"month=?"
                                modifysubmitpm.append(modifysubmitparameterlist[4])
                            else:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+" "+"month=?"
                                modifysubmitpm.append(modifysubmitparameterlist[4])
                        if modifysubmitparameterlist[5]!='All':
                            if ifpriorqueryadded:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+","+" "+"year=?"
                                modifysubmitpm.append(modifysubmitparameterlist[5])
                            else:
                                ifpriorqueryadded=True
                                modifysubmitquery=modifysubmitquery+" "+"year=?"
                                modifysubmitpm.append(modifysubmitparameterlist[5])
                        modifysubmitquery=modifysubmitquery+" "+"WHERE paper_id=?"
                        modifysubmitpm.append(modifysubmitparameterlist[6])
                        cur=conn.cursor()
                        cur.execute(modifysubmitquery,modifysubmitpm)
                        conn.commit()
                        return render_template("mecqpadmin.html", modifymode=modifymode, submissions=submissions)
            if 'closemodifymode' in request.form:
                modifymode=False
                return render_template("mecqpadmin.html", modifymode=modifymode, submissions=submissions)
            if 'deletebutton' in request.form:
                deletemode=True
                return render_template("mecqpadmin.html", deletemode=deletemode, submissions=submissions)
            if 'deletesearch' in request.form:
                deletemode=True
                with sqlite3.connect(database) as conn:
                    deletesearchquery="SELECT * FROM papers"
                    deletesearchparameterlist=[request.form['deletesearchscheme'],request.form['deletesearchbranch'],request.form['deletesearchsemester'],request.form['deletesearchexam_type'],request.form['deletesearchmonth'],request.form['deletesearchyear']]
                    deletesearchpm=[]
                    ifall=1
                    ifpriorqueryadded=False
                    for i in deletesearchparameterlist:
                        if i!='All':
                            ifall=0
                            break
                        else:
                            ifall=1
                    if ifall!=1:
                        deletesearchquery=deletesearchquery+" "+"WHERE"
                    if deletesearchparameterlist[0]!='All':
                        ifpriorqueryadded=True
                        deletesearchquery=deletesearchquery+" "+"scheme=?"
                        deletesearchpm.append(deletesearchparameterlist[0])
                    if deletesearchparameterlist[1]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"AND"+" "+"branch=?"
                            deletesearchpm.append(deletesearchparameterlist[1])
                        else:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"branch=?"
                            deletesearchpm.append(deletesearchparameterlist[1])
                    if deletesearchparameterlist[2]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"AND"+" "+"semester=?"
                            deletesearchpm.append(deletesearchparameterlist[2])
                        else:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"semester=?"
                            deletesearchpm.append(deletesearchparameterlist[2])
                    if deletesearchparameterlist[3]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"AND"+" "+"exam_type=?"
                            deletesearchpm.append(deletesearchparameterlist[3])
                        else:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"exam_type=?"
                            deletesearchpm.append(deletesearchparameterlist[3])
                    if deletesearchparameterlist[4]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"AND"+" "+"month=?"
                            deletesearchpm.append(deletesearchparameterlist[4])
                        else:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"month=?"
                            deletesearchpm.append(deletesearchparameterlist[4])
                    if deletesearchparameterlist[5]!='All':
                        if ifpriorqueryadded:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"AND"+" "+"year=?"
                            deletesearchpm.append(deletesearchparameterlist[5])
                        else:
                            ifpriorqueryadded=True
                            deletesearchquery=deletesearchquery+" "+"year=?"
                            deletesearchpm.append(deletesearchparameterlist[5])
                    cur=conn.cursor()
                    cur.execute(deletesearchquery,deletesearchpm)
                    deletesearchresults=cur.fetchall()
                    return render_template("mecqpadmin.html", deletemode=deletemode, deletesearchresults=deletesearchresults, submissions=submissions)
            if 'deletesubmit' in request.form:
                deletemode=False
                with sqlite3.connect(database) as conn:
                    deletefilenamequery="SELECT filename FROM papers WHERE paper_id=?"
                    deletefilenamepaperid=request.form["deletepaperid"]
                    cur=conn.cursor()
                    cur.execute(deletefilenamequery,(deletefilenamepaperid,))
                    deletefilenamerow=cur.fetchone()
                    deletefilequery="DELETE FROM papers WHERE paper_id=?"
                    os.remove(f"papers/{deletefilenamerow[0]}")
                    cur.execute(deletefilequery,(deletefilenamepaperid,))
                    conn.commit()
                    return render_template("mecqpadmin.html", deletemode=deletemode, submissions=submissions)
            if 'closedeletemode' in request.form:
                deletemode=False
                render_template("mecqpadmin.html", deletemode=deletemode, submissions=submissions)
            if 'acceptsubmission' in request.form:
                with sqlite3.connect(database) as conn:
                    acceptpaperid=request.form["acceptpaperid"]
                    acceptfilenamequery="SELECT filename FROM submissions WHERE submission_id=?"
                    acceptquery="UPDATE submissions SET status=2 WHERE submission_id=?"
                    cur=conn.cursor()
                    cur.execute(acceptfilenamequery,(acceptpaperid,))
                    acceptfilenamerow=cur.fetchone()
                    os.remove(f"submissions/{acceptfilenamerow[0]}")
                    cur.execute(acceptquery,(acceptpaperid,))
                    conn.commit()
                    return redirect(url_for("admin"))
            if 'rejectsubmission' in request.form:
                with sqlite3.connect(database) as conn:
                    rejectpaperid=request.form["rejectpaperid"]
                    rejectfilenamequery="SELECT filename FROM submissions WHERE submission_id=?"
                    rejectquery="UPDATE submissions SET status=0, reason=? WHERE submission_id=?"
                    rejectpm=[request.form["Reason"],rejectpaperid]
                    cur=conn.cursor()
                    cur.execute(rejectfilenamequery,(rejectpaperid,))
                    rejectfilenamerow=cur.fetchone()
                    os.remove(f"submissions/{rejectfilenamerow[0]}")
                    cur.execute(rejectquery,rejectpm)
                    conn.commit()
                    return redirect(url_for("admin"))
            if 'adminmessagesubmit' in request.form:
                with sqlite3.connect(database) as conn:
                    messageupdatedate=datetime.today().strftime('%d.%m.%y')
                    messageupdatequery="INSERT INTO adminmessages (message,message_date) VALUES(?,?)"
                    messageupdatepm=[request.form["adminmessage"],messageupdatedate]
                    cur=conn.cursor()
                    cur.execute(messageupdatequery,messageupdatepm)
                    conn.commit()
            if 'adminlogout' in request.form:
                return redirect(url_for("adminlogout"))
        submissions=get_submission()
        return render_template("mecqpadmin.html", submissions=submissions)
    else:
        return redirect(url_for("adminlogin"))
@app.route("/adminlogout")
def adminlogout():
    if session.get("admin"):
        session.pop("admin",None)
        return render_template("mecqpadminlogout.html")
    else:
        return redirect(url_for("adminlogin"))
@app.route("/submissions/<submissionname>")
def submissiondownload(submissionname):
    if session.get("admin"):
        return send_from_directory('submissions',submissionname)
    else:
        return redirect(url_for("adminlogin"))