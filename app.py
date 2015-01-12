from flask import Flask, render_template, request, url_for, redirect, session, json, g
import sqlite3

app = Flask(__name__)

app.secret_key = "my key"
#for db
app.database = "sample.db"

@app.route('/')
def home():
	return "Hola amigo!"

@app.route('/posts')
def get_posts():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], description = row[1]) for row in cur.fetchall()]
	g.db.close()
	return json.dumps({'posts':posts}), 200, {'Content-Type':'application/json'}


@app.route('/createpost', methods = ['POST'])
def post_new():
	title = request.form['post_title']
	description = request.form['post_desc']
	row = [title,description]
	g.db = connect_db()
	g.db.execute("insert into posts values(?,?)",row)
	g.db.commit()
	g.db.close()
	return redirect(url_for('get_posts'))

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))


def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug=True)