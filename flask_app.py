import os
import fetch_data
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route('/')
def index():
    fetch_data.fetchdata()
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)

