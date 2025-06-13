from flask import Flask, request, jsonify
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return [m.to_dict() for m in messages], 200

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    new_message = Message(
        body=data['body'],
        username=data['username'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return message.to_dict(), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)