from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.eyphci3.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/board', methods=['GET'])
def test_get():
    title = request.args['title']
    board = db.board.find_one({'title': title})

    board['_id'] = str(board['_id'])
    return jsonify({'id': board['_id']})


@app.route('/comment', methods=['POST'])
def comment_post():
    id_receive = request.form['board_id']
    star_receive = request.form['board_star']
    comment_receive = request.form['board_comment']

    doc = {'star': star_receive, 'comment': comment_receive, 'id': id_receive}
    db.comment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글등록완료!'})


@app.route('/comments', methods=['GET'])
def comment_get():
    id = request.args['id']
    all_comments = list(db.comment.find({'id': id}, {'_id': False}))
    return jsonify({'comments': all_comments})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
