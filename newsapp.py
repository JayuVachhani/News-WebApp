import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash,session
from datetime import datetime
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, validators, StringField, PasswordField, BooleanField, form


# create instance of the Flask class
# here parameter of Flask constructor is give current module's name
app = Flask(__name__)

# display current time
today = datetime.now()
print (today.strftime("%Y - %m - %d  %H : %M : %S"))

#here decorator is used to navigate the URL
# whenever user go to the home page route function fire the home function and return the data
@app.route("/")
def reg_mand():
    # passing reference of date variable
    return render_template("register.html",today=today)

class RegistrationForm(Form):
    username  = StringField("Username",[validators.length(min=4,max=20),validators.DataRequired()])
    email =  StringField("Email",[validators.length(min=6,max=30),validators.DataRequired()])
    password = PasswordField("Password",[validators.DataRequired()])


# register page
@app.route("/register/",methods=['GET','POST'])
def register():
    # passing reference of date variable
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            username = form.username.data
            email  = form.email.data
            password = form.password.data

            with sqlite3.connect("news.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into users(username,email,password) VALUES (?, ?, ?)", (username, email, password))

                con.commit()
                print(cur.fetchall())
                cur.close()

                return redirect(url_for('login'))
        except:
            con.rollback()



    return render_template("register.html", today=today,form=form)


# Login page
@app.route("/login/",methods=['GET','POST'])
def login():
    msg = 'msg'
    if request.method == 'POST':

            username = request.form['username']
            password = request.form['password']
            with sqlite3.connect("news.db") as con:
                cur = con.cursor()
                sqlselct = "SELECT * FROM users WHERE username = ? and password = ?"
                print('username : {0} :::: password : {1}'.format(username, password))
                cur.execute(sqlselct, (username, password,))
                data = cur.fetchone()
                # print('12312312313123123123123123')
                # print(data)
                # print(data[1])
            # data = cur.fetchall()
                if data:
                    print("Welcome" + data[1])
                    id_num = data[0]
                    session['logged_in'] = True
                    session['admin'] = False
                    session['username'] = username
                    session['id'] = id_num
                    flash('Logged In Successfully!!!')
                    return redirect(url_for('home'))
            # else:
            #     flash('Invalid Login', 'danger')
            #     return redirect(url_for('login'))
                else:
                    flash('User not found', 'danger')
                    return redirect(url_for('login'))

    return render_template('login.html',today=today)



@app.route("/home/")
def home():
    return render_template("index.html",today=today)


# news page
@app.route("/news/",methods = ['GET','POST'])
def news():

    if request.method == 'POST':
            headlines  = request.form['headlines']
            description = request.form['description']
            author = request.form['author']
            category = request.form['category']
            with sqlite3.connect("news.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into news(headlines,description,author,category) VALUES (?, ?, ?, ?)", (headlines,description,author,category))
                print('headlines : {0} :::: description : {1} :::: author : {2} :::: category : {3}'.format(headlines,description,author,category))
                con.commit()
                print(cur.fetchall())
                cur.close()
                return redirect(url_for('shownews'))
    return render_template("news.html",today=today,form=form)

# show news
@app.route("/shownews/")
def shownews():
    con = sqlite3.connect("news.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from news")

    rows = cur.fetchall()
    return render_template("shownews.html", rows=rows,today=today)


# contact page
@app.route("/contact/",methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
            name  = request.form['fullname']
            email = request.form['email']
            heading = request.form['heading']
            subject = request.form['subject']
            with sqlite3.connect("news.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into contact(name,email,heading,subject) VALUES (?, ?, ?, ?)", (name,email,heading,subject))
                print('name : {0} :::: email : {1} :::: heading : {2} :::: subject : {3}'.format(name,email,heading,subject))
                con.commit()
                flash("Contact successfully added")
                print(cur.fetchall())
                cur.close()

    return render_template("contact.html",today=today)


# logout
@app.route('/logout/')
def logout():
	session.pop('username', None)
	return redirect('/')



if __name__ == "__main__":
    #we need to run our flask app using .run funtion
    #if we don't want run everytime pass the debug = True
    # it will refresh everytime whenever changes is done
    app.secret_key = 'SECRET KEY'
    
    app.run(debug=True)


