import datetime
import os
from flask import Flask, render_template, request
app = Flask(__name__)


people = [	{'name':'Billy Andrews', 'email':'scripture187@gmail.com','dob':'1984-10-10'},
			{'name':'Whitney Esposito', 'email':'wespo796@gmail.com','dob':'1990-02-12'},
			{'name':'Justina Andrews', 'email':'salsajustini@gmail.com','dob':'1980-02-11'}]


@app.route('/')
def mainIndex():
	d = datetime.datetime.now().strftime('%A, %B %e, %Y')
	t = datetime.datetime.now().strftime('%R')
	dt = {'date': d, 'time': t}
	day = datetime.datetime.now().strftime('%A')
	return render_template('index.html', dt=dt, day=day)
	
@app.route('/about')
def showAbout():
	return render_template('about.html')
	
@app.route('/contact')
def showContact():
	return render_template('contact.html')
	
@app.route('/form', methods=['GET','POST'])
def showForm():
	return render_template('form.html')
	
@app.route('/form2', methods=['GET','POST'])
def showForm2():
	if request.method == 'POST':
		if request.form['fname'] != "":
			if request.form['lname'] != "":
				if request.form['email'] != "":
					if request.form['pw1'] == request.form['pw2']:
						people.append({
						'name': request.form['fname']+" "+request.form['lname'],
						'email': request.form['email'],
						'dob': request.form['dob'],
						'pw1': request.form['pw1'],
						'pw2': request.form['pw2']
						})
					else:
						return render_template('badform.html')
				else:
					return render_template('noemail.html')
			else:
				return render_template('noname.html')
		else:
			return render_template('noname.html')
		fname=request.form['fname']
		lname=request.form['lname']
		return render_template('form2.html', fname=fname, lname=lname, people=people)
	else:
		return render_template('form3.html', people=people)

@app.route('/form3', methods=['GET','POST'])
def showForm3():
	return render_template('form3.html', people=people)

@app.route('/gallery')
def showGallery():
	p1 = '/static/faceboard/1.jpg'
	p2 = '/static/faceboard/2.jpg'
	p3 = '/static/faceboard/3.jpg'
	p4 = '/static/faceboard/4.jpg'
	p5 = '/static/faceboard/5.jpg'
	p6 = '/static/faceboard/6.jpg'
	p7 = '/static/faceboard/Thor.jpg'
	photos = {p7, p1, p2, p3, p4, p5, p6}
	return render_template('gallery.html', photos=photos)

	
# Start the server
if __name__ == '__main__':
	app.run(host=os.getenv('IP', "0.0.0.0"), port =int(os.getenv('PORT', 8080)), debug=True)