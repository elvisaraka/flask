import mysql.connector
from flask import *
app = Flask(__name__)
app.secret_key = "abc"  

mycon=mysql.connector.connect(host="localhost",user="root",password="",database="student_portal")
cur=mycon.cursor()
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/registration')
def registration():
	return render_template('register.html')
@app.route('/registration_action',methods=['POST'])
def registration_action():
	if request.method == "POST":
		registration_number=request.form['registration_number']
		student_names=request.form['student_names']
		school=request.form['school']
		program=request.form['program']
		#stage=request.form['program']
		nationalIdNumber=request.form['nationalIdNumber']
		#validate the data



		#query from database where registrationNumber
		tup=[]
		tup.append(registration_number)

		sql="SELECT * FROM studentinfo WHERE registrationNumber =%s"
		cur.execute(sql,tup)
		print(cur)
		result=cur.fetchone()
		if result:
			error="registration number already exists"
			return render_template('register.html',error=error)
		else:
			sql1 = "insert into studentinfo(registrationNumber,studentName,school,programe,stage,nationalIdNumber) values (%s, %s, %s, %s, %s,%s)" 
			val = (registration_number,student_names,school,program,"y1s1",nationalIdNumber) 
			try:
				cur.execute(sql1,val)

				print(cur)
				mycon.commit()
				session['username']=registration_number
				flash("student registered successfully")
				return redirect(url_for("home"))
			except:
				mycon.rollback()
				error="something went wrong"
				return render_template('register.html',error=error)
			
	else:
		@app.errorhandler(404)
		def not_found(error):
			return render_template('error.html'), 404


@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/login_action',methods=['POST'])
def login_action():
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		#validate the data

		#query from database where username and password are the same
		tup2=[]
		tup2.append(username)
		tup2.append(password)
		sql3="SELECT * FROM studentinfo WHERE registrationNumber =%s AND nationalIdNumber =%s "
		cur.execute(sql3,tup2)
		print(cur)
		result2=cur.fetchone()
		if result2:
			#set the value of username to a session
			flash("valid details")
			session['username']=username
			#redirect to home page
			return redirect(url_for('home'))
		else:
			error="incorrect user name or password"
			return render_template("login.html",error=error)

		
		
	else:
		@app.errorhandler(404)
		def not_found(error):
			return render_template('error.html'), 404
@app.route('/home')
def home():
	if 'username' in session:
		tup3=[]
		tup3.append(session['username'])
		sql4="SELECT * FROM studentinfo WHERE registrationNumber =%s"
		cur.execute(sql4,tup3)
		print(cur)
		result4=cur.fetchone()
		if result4:
			return render_template("home.html",result=result4)
	else:
		error="something went wrong"
		return render_template("login.html")
		
	
	
		
		
		


	
if __name__ == "__main__":
	app.run(debug=True)


