from flask import (Flask, render_template, request)

app = Flask(__name__)

APPLICATION_NAME = "Josh Briand's website"

@app.route('/', methods=['GET'])
def showIndexPage():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = "Don't panic!"
    app.debug = True
    app.run()
