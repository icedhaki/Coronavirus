import os
import fetch_data
import findplace
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route('/')
def index():
    fetch_data.fetchdata()
    findplace.findplace()
    return render_template('map.html')

@app.route('/thank')
def thank():
    return render_template('thankyou.html')

if __name__ == "__main__":
    app.run(debug=True)

