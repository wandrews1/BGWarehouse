import datetime
import os
from flask import Flask, render_template
app = Flask(__name__)


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

@app.route('/gallery')
def showGallery():
	p1 = '/static/faceboard/1.jpg'
	p2 = '/static/faceboard/2.jpg'
	p3 = '/static/faceboard/3.jpg'
	p4 = '/static/faceboard/4.jpg'
	p5 = '/static/faceboard/5.jpg'
	p6 = '/static/faceboard/6.jpg'
	photos = {p1, p2, p3, p4, p5, p6}
	return render_template('gallery.html', photos=photos)
	
@app.route('/rickroll')
def showRick():
	theLyrics = "Never gonna give you up."
	return render_template('rickroll.html', lyrics=theLyrics)


	
# Start the server
if __name__ == '__main__':
	app.run(host=os.getenv('IP', "0.0.0.0"), port =int(os.getenv('PORT', 8080)), debug=True)