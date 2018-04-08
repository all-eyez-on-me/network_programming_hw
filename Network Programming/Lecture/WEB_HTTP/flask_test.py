from flask import Flask
from flask import request
from flask import render_template, jsonify

app = Flask('__name__')
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/user/<username>')
def show_user_profile(username):
    message = "Hello {}!".format(username)
    return message
# Use <type:variable> to restrict the data type
@app.route('/post/<int:post_id>')
def show_post(post_id):
    message = "This is Post {:d}".format(post_id)
    return message

@app.route('/get_news', methods=['GET'])
def get_news():
    news_id = request.args.get("news_id")
    articles = get_news_from_db(news_id)
    return jsonify(status="OK", data=articles)
@app.route('/add', methods=['GET'])
def add():
# Retrieve values of a and b from query string
    a = request.args.get("a", 0, type=int)
    b = request.args.get("b", 0, type=int)
    sum = a + b
# Return a JSON response
    return jsonify(status="OK", sum=sum)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)