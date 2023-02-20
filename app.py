from flask import Flask,render_template,flash, redirect,url_for,json,request
from forms import RegistrationForm,LoginForm,QuestionForm
from flask_mysqldb import MySQL
app = Flask(__name__)
from mysql.connector import connect

app.config['SECRET_KEY']='46fcbed91dbb'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='Bharath@2002'
app.config['MYSQL_DB']='users'
mysql = MySQL(app)


user=""


posts =[
    {
        'author':"someone",
        'title':'someone',
        'content':'someone',
        'date':'12th feb 2023'
    },
     {
        'author':"someone",
        'title':'someone',
        'content':'someone',
        'date':'12th feb 2023'
    },
     {
        'author':"someone",
        'title':'someone',
        'content':'someone',
        'date':'12th feb 2023'
    },
     {
        'author':"someone",
        'title':'someone',
        'content':'someone',
        'date':'12th feb 2023'
    }
]

questions_data=""
user_data=""

@app.route("/answer/<int:id>",methods=['POST','GET'])
def answer(id):
    global user
    if(user == ""):
        return redirect("/login")
    else:
        print(id)
        answer = request.form.get("answer")
        print(user_data)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO answers(answer,userid,questionid) values(%s,%s,%s)",(answer,user_data[0][0],id,))
        mysql.connection.commit()
        return answer

@app.route("/home",methods=['POST','GET'])
def hello():
    global user
    if(user == ""):
        return redirect("/register")
    else:
        form = QuestionForm()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM flask WHERE email=%s",(user,))
        data = cur.fetchall()
        global user_data
        user_data = data
        cur.execute("SELECT * FROM questions")
        question_data = cur.fetchall()
        cur.execute("SELECT * FROM answers")
        answer_data = cur.fetchall()
        mysql.connection.commit()
        question = form.question.data
        cur.execute("SELECT * FROM questions WHERE question=%s",(question,))
        data_1 = cur.fetchall()
        global questions_data
        questoins_data = data_1
        mysql.connection.commit()
        if(data_1):
            return "<h1>Already Question Exists</h1>"
        else:
            if(question):
                 cur.execute("INSERT INTO questions(question,userid) values(%s,%s)",(question,data[0][0],))
                 mysql.connection.commit()
                 return redirect('/home')
        
        return render_template("home.html",posts=posts,data=data,form=form,question_data=question_data,answer_data=answer_data)


@app.route("/")
@app.route("/register",methods=['POST','GET'])
def register():
    form = RegistrationForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM flask WHERE email=%s",(form.email.data,))
    data = cur.fetchall()
    mysql.connection.commit()
    if(data):
        return "user already exists please login!!"
    if form.validate_on_submit():
         Username = "uxumaki"
         email="bharath"
         password="syesojf"
         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO flask(Username,email,password)  VALUES(%s,%s,%s)",(form.username.data,form.email.data,form.password.data))
         mysql.connection.commit()
         global user
         user=form.email.data
         return redirect("/home")
    return render_template('register.html', title='Register', form=form)

print(user)
@app.route("/login",methods=['POST','GET'])
def login():
     form = LoginForm()
     cur = mysql.connection.cursor()
     cur.execute("SELECT * FROM flask WHERE email=%s and password=%s",(form.email.data,form.password.data,))
     data = cur.fetchall()
     mysql.connection.commit()
     if form.validate_on_submit():
        if(data):
            global user
            user=form.email.data
            print(data)
            return redirect("/home")
        else:
            return "<h1>please Register</h1>"   
     return render_template('login.html', title='Login', form=form)


@app.route("/about")
def about():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM flask WHERE email=%s",(user,))
    data = cur.fetchall()
    global user_data
    user_data = data
    print(user_data)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM questions WHERE userid=%s",(user_data[0][0],))
    data = cur.fetchall()  
    return render_template('about.html',data=data)

if (__name__ == '__main__'):
    app.run(debug=True)