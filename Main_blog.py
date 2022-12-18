from flask import Flask,render_template,url_for,redirect,flash,request,jsonify,send_file
from sqlalchemy import create_engine,asc,and_,func,extract
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from Blog_database import Base,Admin,Blog_data,Response
from flask import session as login_session
import string
import datetime
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory


from flask import make_response
import requests

engine = create_engine('sqlite:///Blog_database.db',connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/Blog_Images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def main_page():
	user=session.query(Admin).first()
	blogmeta=session.query(Blog_data).all()
	return render_template('index.html',user=user,meta=blogmeta) 
@app.route('/aboutme')
def about_me():
	return(render_template('about.html'))

@app.route('/blogposts/<int:blog_id>',methods=['GET','POST'])
def blog_post(blog_id):
	postdata=session.query(Blog_data).filter_by(Id=blog_id).first()
	return render_template('post.html',postdata=postdata)
@app.route('/postedit/<int:postid>',methods=['GET','POST'])
def editpost(postid):
	if 'username' not in login_session:
		return redirect('/login')
	postmeta=session.query(Blog_data).filter_by(Id=postid).first()
	return render_template('postedit.html',postmeta=postmeta)

@app.route('/contactme')
def contact_me():
	return(render_template('contact.html'))

@app.route('/sample/<int:id>',methods=['GET','POST'])
def sample(id):
	if 'username' not in login_session:
		return redirect('/login')
	admin=session.query(Admin).filter_by(Id=id).first()
	if(admin.Name != login_session['username']):
		return "<script>function myFunction() {window.location='/login'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	return render_template('blog.html',id=admin.Id)

@app.route('/postsubmit/<int:id>/<int:blog_id>',methods=['POST','GET'])
def postsubmit(id):
	if 'username' not in login_session:
		return redirect('/login')
	admin=session.query(Admin).filter_by(Id=id).first()
	if(admin.Name != login_session['username']):
		return "<script>function myFunction() {window.location='/login'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	if request.method == 'POST':
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
			Mainhead=request.form['Mainhead']
			Headtag=request.form['Headtag']
			Sidehead=request.form['Sidehead']
			imagedescription=request.form['imagedescription']
			quotation=request.form['quotation']
			links=request.form['links']
			Para1=request.form['Para1']
			Para2=request.form['Para2']
			Para3=request.form['Para3']
			blog_data=Blog_data(head=Mainhead,headtag=Headtag,Sideheads=Sidehead,filedescription=imagedescription,quote=quotation,links=links,
									Para1=Para1,Para2=Para2,Para3=Para3,Para4=Para4,Para5=Para5,Para6=Para6,Para7=Para7,Para8=Para8,file=filename)
			session.add(blog_data)
			session.commit()
			flash("Finally! We have done it.")
			return redirect(url_for('main_page'))
	else:
		return "<script> alert('Methods is not posting into the database')</script>"

@app.route('/login',methods=['POST','GET'])
def login():	
	return render_template('login.html')

@app.route('/authorising',methods=['POST','GET'])
def authorize():
	if request.method=='POST':
			username=request.form['username']
			password=request.form['pass']
			route=request.form['route']
			if(session.query(Admin).filter_by(Name=username).first() is not None):
				user=session.query(Admin).filter_by(Name=username).first()
				if(user.verify_password(password)):
					login_session['username']=user.Name
					flash('Welcome %s'%(user.Name))
					if(route=='1'):
						return redirect(url_for('sample',id=user.Id))
					else:
						return redirect(url_for('responses'))

			else:
				flash('Oops!! Your password or usernamer is not matching')
				return redirect('/login')

@app.route('/messagesubmit',methods=['POST','GET'])
def messagesubmit():
	if request.method=='POST':
		name=request.form['name']
		email=request.form['email']
		phone=request.form['phonenumber']
		message=request.form['message']

		message=Response(name=name,email=email,phone=phone,message=message)
		session.add(message)
		session.commit()
		flash("Your message submitted sucessfully!")

		return redirect(url_for('main_page'))
	else:
		return "<script> alert('Methods is not posting into the database')</script>"
@app.route('/responses',methods=['POST','GET'])
def responses():
	if 'username' not in login_session:
		flash("Prove that you're the admin")
		return redirect('/login')
	admin=session.query(Admin).first()
	if(admin.Name != login_session['username']):
		return "<script>function myFunction() {window.location='/login'}alert('Dont Try to manipulate bro!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"
	response=session.query(Response).all()
	return render_template('response.html',responses=response)

@app.route('/logout')
def logout():
	del login_session['username']
	flash('Deleted the session of this user')
	return redirect(url_for('main_page'))

if __name__=='__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)