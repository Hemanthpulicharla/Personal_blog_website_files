from flask import Flask,render_template,url_for,redirect,flash,request,jsonify,send_file
from sqlalchemy import create_engine,asc,and_,func,extract
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from OLMS import Base,Overview,Wardens,Superwarden,Security,Students,Pending,Complaints,Outpass,Results
from flask import session as login_session
import string
import datetime
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory


from flask import make_response
import requests

engine = create_engine('sqlite:///OLMS.db',connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

use_date=datetime.datetime.now()
UPLOAD_FOLDER = 'Images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


P1=['Maths','Physics','Chemistry','Biology']

#Complaints section rendering for showin on the student page and super warden page as well


#Branch wise analysis of the Leave share to show on the super warden page and wraden page


#Graph data for drawing the leave v/s time graph on a monthly basis



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def showLogin():
	return render_template('login.html')
@app.route('/Authorization',methods=['GET','POST'])
def Authorize():
	if request.method=='POST':
		username=request.form['username']
		password=request.form['pass']
		if(session.query(Wardens).filter_by(email=username).first() is not None):
			user=session.query(Wardens).filter_by(email=username).first()
			if(user.verify_password(password)):
				login_session['username']=user.name
				login_session['email']=user.email
				flash('Welcome %s'%(user.name))
				return redirect(url_for('Wardenpage',warden_id=user.id))
			else:
				flash('Oops!! Your password doesnot matching')
				return redirect('/')
		if(session.query(Students).filter_by(email=username).first() is not None):
			user=session.query(Students).filter_by(email=username).first()
			if(user.verify_password(password)):
				login_session['username']=user.name
				login_session['email']=user.email
				flash('Welcome %s'%(user.name))
				return redirect(url_for('studentpage',student_id=user.id))
			else:
				flash('Oops!!Your password doesnot matching')
				return redirect('/')
		if(session.query(Superwarden).filter_by(email=username).first() is not None):
			user=session.query(Superwarden).filter_by(email=username).first()
			if(user.verify_password(password)):
				login_session['username']=user.name
				login_session['email']=user.email
				flash('Welcome %s'%(user.name))
				return redirect(url_for('Superwardenpage',superwarden_id=user.id))
			else:
				flash('Oops!! Your password is doesnot matching')
				return redirect('/')
		if(session.query(Security).filter_by(email=username).first() is not None):
			user=session.query(Security).filter_by(email=username).first()
			if(user.verify_password(password)):
				login_session['username']=user.name
				login_session['email']=user.email
				flash('Welcome %s'%(user.name))
				return redirect(url_for('Securitypage',security_id=user.id))
			else:
				flash('Oops!! Your password doesnot matching')
				return redirect('/')
		else:
			flash('Oops!! Looks like you username doesnot exist')
			return redirect('/')
	else:
		flash('Sorry!! for the inconvinience.. Try again later')
		return redirect('/')


@app.route('/wardens/<int:warden_id>',methods=['GET','POST'])
def Wardenpage(warden_id):
	if 'username' not in login_session:
		return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).first()
	if(warden.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	pending=session.query(Pending).filter_by(warden=warden.name).all()
	overview=session.query(Overview).filter_by(warden=warden.name).all()
	month=session.query(Overview).filter_by(month=use_date.month).count()
	year=session.query(Overview).filter_by(year=use_date.year).count()
	pendings=len(pending)
	outpercents=len(overview)
	incamp=100-(pendings+outpercents)
	incampperc=(float(incamp/100))*100
	graphdata=[1]*12
	jan=session.query(Overview).filter_by(month=1).count()
	graphdata[0]=jan
	feb=session.query(Overview).filter_by(month=2).count()
	graphdata[1]=feb
	mar=session.query(Overview).filter_by(month=3).count()
	graphdata[2]=mar
	apr=session.query(Overview).filter_by(month=4).count()
	graphdata[3]=apr
	may=session.query(Overview).filter_by(month=5).count()
	graphdata[4]=may
	jun=session.query(Overview).filter_by(month=6).count()
	graphdata[5]=jun
	jul=session.query(Overview).filter_by(month=7).count()
	graphdata[6]=jul
	aug=session.query(Overview).filter_by(month=8).count()
	graphdata[7]=aug
	sep=session.query(Overview).filter_by(month=9).count()
	graphdata[8]=sep
	octo=session.query(Overview).filter_by(month=10).count()
	graphdata[9]=octo
	nov=session.query(Overview).filter_by(month=11).count()
	graphdata[10]=nov
	dec=session.query(Overview).filter_by(month=12).count()
	graphdata[11]=dec

	branch=[1.1]*8
	totalb=session.query(Outpass).count()
	if(totalb==0):
		totalb=1
	cse=session.query(Outpass).filter_by(branch='cse').count()
	cseper=(float(cse)/totalb)*100
	branch[0]=cseper
	mech=session.query(Outpass).filter_by(branch='mech').count()
	mechper=(float(mech)/totalb)*100
	branch[1]=mechper
	ece=session.query(Outpass).filter_by(branch='Ece').count()
	eceper=(float(ece)/totalb)*100
	branch[2]=eceper
	civil=session.query(Outpass).filter_by(branch='civil').count()
	civilper=(float(civil)/totalb)*100
	branch[3]=civilper
	mme=session.query(Outpass).filter_by(branch='mme').count()
	mmeper=(float(mme)/totalb)*100
	branch[4]=mmeper
	chem=session.query(Outpass).filter_by(branch='chem').count()
	chemper=(float(chem)/totalb)*100
	branch[5]=chemper

	return render_template('index.html',warden=warden,pendingper=pendings,outpercent=outpercents,overview=overview,month=month,incamp=incamp,year=year,incampus=incampperc,graphdata=graphdata,branch=branch)

@app.route('/student/<int:student_id>',methods=['GET','POST'])
def studentpage(student_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	if(student.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	warden=session.query(Wardens).filter_by(id=student.warden_id).first()
	leave=session.query(Overview).filter_by(id_num=student.id_num).count()
	month=session.query(Overview).filter_by(id_num=student.id_num,month=use_date.month).count()
	year=session.query(Overview).filter_by(id_num=student.id_num,year=use_date.year).count()
	status='Rejected'
	if(session.query(Pending).filter_by(id_num=student.id_num).first()):
		status='Pending'
	if(session.query(Outpass).filter_by(id_num=student.id_num).first()):
		status='Approved'
	#This is data for graph used inside the student view frontend pages 
	studentgraphdata=[1]*12
	jan=session.query(Overview).filter_by(month=1,id_num=student.id_num).count()
	studentgraphdata[0]=jan
	feb=session.query(Overview).filter_by(month=2,id_num=student.id_num).count()
	studentgraphdata[1]=feb
	mar=session.query(Overview).filter_by(month=3,id_num=student.id_num).count()
	studentgraphdata[2]=mar
	apr=session.query(Overview).filter_by(month=4,id_num=student.id_num).count()
	studentgraphdata[3]=apr
	may=session.query(Overview).filter_by(month=5,id_num=student.id_num).count()
	studentgraphdata[4]=may
	jun=session.query(Overview).filter_by(month=6,id_num=student.id_num).count()
	studentgraphdata[5]=jun
	jul=session.query(Overview).filter_by(month=7,id_num=student.id_num).count()
	studentgraphdata[6]=jul
	aug=session.query(Overview).filter_by(month=8,id_num=student.id_num).count()
	studentgraphdata[7]=aug
	sep=session.query(Overview).filter_by(month=9,id_num=student.id_num).count()
	studentgraphdata[8]=sep
	octo=session.query(Overview).filter_by(month=10,id_num=student.id_num).count()
	studentgraphdata[9]=octo
	nov=session.query(Overview).filter_by(month=11,id_num=student.id_num).count()
	studentgraphdata[10]=nov
	dec=session.query(Overview).filter_by(month=12,id_num=student.id_num).count()
	studentgraphdata[11]=dec

	complaint=[1]*8
	total=session.query(Complaints).count()
	if(total==0):
		total=1
	mess=session.query(Complaints).filter_by(category='Mess').count()
	messper=(float(mess)/total)*100
	complaint[0]=messper
	elec=session.query(Complaints).filter_by(category='Electricity').count()
	elecper=(float(elec)/total)*100
	complaint[1]=elecper
	water=session.query(Complaints).filter_by(category='Water').count()
	waterper=(float(water)/total)*100
	complaint[2]=waterper
	Hk=session.query(Complaints).filter_by(category='HouseKeep').count()
	Hkper=(float(Hk)/total)*100
	complaint[3]=Hkper
	sec=session.query(Complaints).filter_by(category='Security').count()
	secper=(float(sec)/total)*100
	complaint[4]=secper
	dorm=session.query(Complaints).filter_by(category='Dorm').count()
	dormper=(float(dorm)/total)*100
	complaint[5]=dormper
	lib=session.query(Complaints).filter_by(category='Library').count()
	libper=(float(lib)/total)*100
	complaint[6]=libper
	clsinfra=session.query(Complaints).filter_by(category='ClassInfra').count()
	clsper=(float(clsinfra)/total)*100
	complaint[7]=clsper
	
	return render_template('student.html',status=status,warden=warden,student=student,month=month,year=year,graphdata=studentgraphdata,outpass=leave,complaint=complaint)

@app.route('/superwarden/<int:superwarden_id>',methods=['GET','POST'])
def Superwardenpage(superwarden_id):
	if 'username' not in login_session:
    	   return redirect('/login')
   	superwarden=session.query(Superwarden).filter_by(id=superwarden_id).first()
   	if(superwarden.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	student=session.query(Pending).count()
	warden=session.query(Wardens).all()
	approve=session.query(Overview).count()
	pending=session.query(Pending).count()
	incamp=100-(approve+pending)
	month=session.query(Overview).filter_by(month=datetime.datetime.utcnow().month).count()
	year=session.query(Overview).filter_by(year=datetime.datetime.utcnow().year).count()
	graphdataf=[1]*12
	jan=session.query(Overview).filter_by(month=1).count()
	graphdataf[0]=jan
	feb=session.query(Overview).filter_by(month=2).count()
	graphdataf[1]=feb
	mar=session.query(Overview).filter_by(month=3).count()
	graphdataf[2]=mar
	apr=session.query(Overview).filter_by(month=4).count()
	graphdataf[3]=apr
	may=session.query(Overview).filter_by(month=5).count()
	graphdataf[4]=may
	jun=session.query(Overview).filter_by(month=6).count()
	graphdataf[5]=jun
	jul=session.query(Overview).filter_by(month=7).count()
	graphdataf[6]=jul
	aug=session.query(Overview).filter_by(month=8).count()
	graphdataf[7]=aug
	sep=session.query(Overview).filter_by(month=9).count()
	graphdataf[8]=sep
	octo=session.query(Overview).filter_by(month=10).count()
	graphdataf[9]=octo
	nov=session.query(Overview).filter_by(month=11).count()
	graphdataf[10]=nov
	dec=session.query(Overview).filter_by(month=12).count()
	graphdataf[11]=dec

	branch=list(range(8))
	totalb=session.query(Outpass).count()
	if(totalb==0):
		totalb=1
	cse=session.query(Outpass).filter_by(branch='cse').count()
	branch[0]=(float(cse)/totalb)*100
	mech=session.query(Outpass).filter_by(branch='mech').count()
	branch[1]=(float(mech)/totalb)*100
	ece=session.query(Outpass).filter_by(branch='Ece').count()
	branch[2]=(float(ece)/totalb)*100
	civil=session.query(Outpass).filter_by(branch='civil').count()
	branch[3]=(float(civil)/totalb)*100
	mme=session.query(Outpass).filter_by(branch='mme').count()
	branch[4]=(float(mme)/totalb)*100
	chem=session.query(Outpass).filter_by(branch='chem').count()
	branch[5]=(float(chem)/totalb)*100

	return render_template('superwarden.html',warden=warden,student=student,superwarden=superwarden,month=month,year=year,approve=approve,pending=pending,incamp=incamp,branch=branch,graphdata=graphdataf)
@app.route('/security/<int:security_id>',methods=['GET','POST'])
def Securitypage(security_id):
 	if 'username' not in login_session:
    	    return redirect('/login')
   	security=session.query(Security).filter_by(id=security_id).first()
   	if(security.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	student=session.query(Outpass).all()
	warden=session.query(Wardens).all()
	superwarden=session.query(Superwarden).all()
	return render_template('security.html',student=student,warden=warden,superwarden=superwarden,security=security)

@app.route('/leave/applying/<int:student_id>',methods=['GET','POST'])
def applyleave(student_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	if(student.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	warden=session.query(Wardens).filter_by(id=student.warden_id).first()
	if(session.query(Outpass).filter_by(id_num=student.id_num).first()):
		flash('You already had a leave granted')
		return redirect(url_for('studentpage',student_id=student_id))
	if(session.query(Pending).filter_by(id_num=student.id_num).first()):
		flash('Your leave request is pending..')
		return redirect(url_for('studentpage',student_id=student_id))
	else:
		return render_template('leave_application.html',student=student,warden=warden)
@app.route('/leave/pending/<int:student_id>',methods=['GET','POST'])
def leavesubmit(student_id):
	if 'username' not in login_session:
        	return redirect('/login')
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			return "<script> alert('File not selected')</script>"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            reason=request.form['reason']
            fromdate=request.form['fromdate']
            todate=request.form['todate']
            contact=request.form['contact']
            student=session.query(Students).filter_by(id=student_id).first()
            warden=session.query(Wardens).filter_by(id=student.warden_id).first()
            pending=Pending(name=student.name,id_num=student.id_num,email=student.email,branch=student.branch,warden=warden.name,contact=contact,reason=reason,fromdate=fromdate,todate=todate,file=filename)
            session.add(pending)
            session.commit()
            flash("Whoa!! Your request submitted")
            return	redirect(url_for('studentpage',student_id=student_id))
        else:
        	flash('Problem in submitting')
        	return	"<script>function myFunction() {window.location='/student/%s'} alert('Problem in submitting please try again...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%student_id


@app.route('/pending/<int:warden_id>/table',methods=['GET','POST'])
def pending(warden_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).first()
	if(warden.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	pending=session.query(Pending).filter_by(warden=warden.name).all()
	return render_template('tablesnew.html',pending=pending,warden=warden)
@app.route('/leaveapprove/<student_id>/<int:warden_id>',methods=['GET','POST'])
def leaveapprove(warden_id,student_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Pending).filter_by(id_num=student_id).first()
	warden=session.query(Wardens).filter_by(id=warden_id).first()
	if(warden.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	leave=Overview(name=student.name,fromdate=student.fromdate,todate=student.todate,id_num=student.id_num,email=student.email,branch=student.branch,warden=warden.name,reason=student.reason,contact=student.contact)
	session.add(leave)
	session.commit()
	outpass=Outpass(name=student.name,fromdate=student.fromdate,todate=student.todate,id_num=student.id_num,email=student.email,branch=student.branch,warden=warden.name,reason=student.reason,contact=student.contact)
	session.add(outpass)
	session.commit()
	session.delete(student)
	session.commit()
	warden.leaves_granted+=1
	flash('Leave approved succesfully!!')
	return redirect(url_for('pending',warden_id=warden_id))
	#else:
	#	return "<script>function myFunction() {window.location='/pending/%s/table'} alert('Problem in submitting...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
@app.route('/leavereject/<student_id>/<int:warden_id>')
def leavereject(student_id,warden_id):
	if 'username' not in login_session:
    	    return redirect('/login')
 	warden=session.query(Wardens).filter_by(id=warden_id).first()
 	if(warden.email != login_session['email']):
			return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	pendingdown=session.query(Pending).filter_by(id_num=student_id).first()
	student=session.query(Students).filter_by(id_num=student_id).first()
	student.rejected+=1
	session.delete(pendingdown)
	session.commit()
	flash('Leave rejected for %s'%student.name)
	return redirect(url_for('pending',warden_id=warden_id))
@app.route('/approved/<int:warden_id>',methods=['POST','GET'])
def Approved(warden_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).first()
	if(warden.email != login_session['email']):
			return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	approved=session.query(Outpass).filter_by(warden=warden.name).all()
	return render_template('approvedleaves.html',approved=approved,warden=warden)
@app.route('/depreciate/<student_id>/<int:warden_id>')
def depreciate(warden_id,student_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	student=session.query(Overview).filter_by(id_num=student_id).first()
	outpassdip=session.query(Outpass).filter_by(id_num=student_id).first()
	session.delete(outpassdip)
	session.commit()
	flash('Leave depreciated succesfully for %s'%student.name)
	return redirect(url_for('Approved',warden_id=warden_id))
		#return "<script>function myFunction() {window.location='/approved/%i'} alert('Sorry Couldnt depreciate...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
@app.route('/superwarden/<int:sup_id>/table')
def superview(sup_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	pending=session.query(Pending).all()
	requests=len(pending)
	return render_template('supertable.html',pending=pending,superwarden=superwarden,requests=requests)
@app.route('/superapprove/<int:sup_id>')
def superapprove(sup_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	approved=session.query(Outpass).all()
	return render_template('superapprove.html',approved=approved,superwarden=superwarden)
@app.route('/outpassview/<int:sup_id>')
def outpassview(sup_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	approved=session.query(Outpass).all()
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	return render_template('outpassview.html',approved=approved,superwarden=superwarden)
@app.route('/depreciated/<student_id>/<int:sup_id>')
def superdepreciate(student_id,sup_id):
	outpass=session.query(Outpass).filter_by(id_num=student_id).first()
	session.delete(outpass)
	session.commit()
	flash('Leave depreciated succesfully for %s'%student.name)
	return redirect(url_for('outpassview',sup_id=sup_id))
@app.route('/complaint/<int:student_id>/<category>',methods=['GET','POST'])
def complain(student_id,category):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	if(student.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	return render_template('complain_form.html',student=student,category=category)
@app.route('/results/<student_id>',methods=['GET','POST'])
def getresults(student_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id_num=student_id).first()
	if(student.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	results=session.query(Results).filter_by(id_num=student_id).all()
	return render_template('results.html',results=results,student=student)

@app.route('/complainsubmit/<int:student_id>/<category>',methods=['GET','POST'])
def complainsubmit(student_id,category):
	if 'username' not in login_session:
    	    return redirect('/login')
   	student=session.query(Students).filter_by(id=student_id).first()
   	if(student.email != login_session['email']):
		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
   	if request.method == 'POST':
   		complaint=Complaints(stud_name=student.name,id_num=student.id_num,branch=student.branch,email=request.form['email'],category=category,description=request.form['message'],oneline=request.form['oneline'])
   		session.add(complaint)
   		session.commit()
   		flash("Complaint succesfully submitted!")
   		return redirect(url_for('studentpage',student_id=student.id))
   	else:
   		return	"<script>function myFunction() {window.location='/student/%s'} alert('Problem in submitting please try again.Redirecting..........');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%student_id
@app.route('/complainview/<int:sup_id>')
def complaintview(sup_id):
	if 'username' not in login_session:
    	    return redirect('/login')
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	if(superwarden.email != login_session['email']):
			return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	complaint=session.query(Complaints).all()
	return render_template('complaintview.html',superwarden=superwarden,complaint=complaint)
@app.route('/facultyreview/<id_num>',methods=['GET','POST'])
def facultyreview(id_num):
	sub=[]
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id_num=id_num).first()
	if(student.email != login_session['email']):
    		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');</script><body onload='myFunction()'>"
	if 'o17' in login_session['email']:
			sub=P1
	return render_template('faaculyreview.html',student=student,sub=sub)

@app.route('/messreview/<id_num>',methods=['GET','POST'])
def messreview(id_num):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Students).filter_by(id_num=id_num).first()
	if(student.email != login_session['email']):
    		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');</script><body onload='myFunction()'>"
	return render_template('messreview.html',student=student)

@app.route('/facultyreviewsubmit/<id_num>',methods=['GET','POST'])
def reviewsubmit(id_num):
   	if 'username' not in login_session:
			return redirect('/login')
	student=session.query(Students).filter_by(id_num=id_num).first()
	if student.email != login_session['email']:
    		return "<script>function myFunction() {window.location='/'}alert('Dont Try to manipulate bro!! Redirecting.....');</script><body onload='myFunction()'>"
	if request.method == 'POST':
		rating=Ratings(faculty_id=request.form['faculty_id'],Section=request.form['section'],
    			faculty_name=request.form['faculty_name'],Timeliness=request.form['Timeliness'],
    			Concept_depth=request.form['Concept'],Doubts=request.form['Doubts'],Availability=request.form['Availability'],
    			Preparedness=request.form['Preparedness'],Temparement=request.form['Temparement'])
    	session.add(rating)
    	session.commit()
    	flash(' Faculty review submitted succesfully')
    	return redirect('facultyreview',id_num=student.id_num)
    #else:
    #	return	"<script>function myFunction() {window.location='/student/%s'} alert('Problem in submitting please try again.Redirecting..........');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%student_id

@app.route('/download/<int:id>')
def downloadfile(id):
	if 'username' not in login_session:
    	    return redirect('/login')
	student=session.query(Pending).filter_by(id=id).first()
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               student.file,as_attachment=True)
@app.route('/logout')
def logout():
	del login_session['username']
	del login_session['email']
	return redirect(url_for('showLogin'))
if __name__=='__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)





