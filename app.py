from flask import Flask, request, render_template, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environmental variables from .env
load_dotenv()


app = Flask(__name__)


username = os.getenv('MONGODB_USER')
password = os.getenv('MONGODB_PASSWORD')
server = os.getenv('SERVER')
client = MongoClient()
client = MongoClient(f"mongodb://{username}:{password}@{server}:32788/")
db = client.note_app
collection = db["notes"]



@app.route("/create", methods=['POST']) # Respond to POST request
def create_note():

    """Receive POST request containing new note, and load it to MongoDB collection."""

    # Get json data sent by POST request
    title = request.form.get('new_memo_title')
    memo = request.form.get('new_memo_contents')
    # Add created date to the data
    date = datetime.now().strftime('%Y-%m-%d')
    # Load a new memo to MongoDB collection
    collection.insert_one({'date' : date, 'title' : title, 'memo' : memo})

    # Redirect to '/home'
    return redirect(url_for('show_notes'))


@app.route('/delete/<string:row_id>')
def delete_row(row_id):

    """Delete a memo."""

    # Delete a document from MongoDB collection 
    object_id = ObjectId(row_id)
    collection.delete_one({ "_id" : object_id })
    # Redirect to /home
    return redirect(url_for('show_notes'))


@app.route("/home")
def show_notes():

    """Get all the memos from MongoDB, and display in web server."""
    
    # Get all the memo stored in MongoDB
    memos = collection.find()

    return render_template('note_app.html', memos = memos)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    
