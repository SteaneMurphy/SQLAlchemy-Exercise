from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://james:12345@localhost:5432/trello_clone_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')

@app.cli.command('seed')
def seed_db():
    from datetime import date
    card1 = Card(
        title = 'Start the project',
        description = 'Stage 1, creating the database',
        status = 'To do',
        priority = 'High',
        date = date.today()
    )
    db.session.add(card1)

    card2 = Card(
        title = 'SQLAlchemy and Marshmallow',
        description = 'Stage 2, integrate both modules in the project',
        status = 'Ongoing',
        priority = 'High',
        date = date.today()
    )
    db.session.add(card2)

    db.session.commit()
    print('Tables seeded')

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped')

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date', 'status', 'priority')

card_schema = CardSchema()
cards_schema = CardSchema(many=True)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/cards', methods=['GET'])
def get_cards():
    stmt = db.select(Card)
    cards = db.session.scalars(stmt)
    result = cards_schema.dump(cards)
    return jsonify(result)