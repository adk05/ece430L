from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Anthony:anthonysql2004!@localhost:3306/exchange'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float, nullable=False)
    lbp_amount = db.Column(db.Float, nullable=False)
    usd_to_lbp = db.Column(db.Boolean, nullable=False)

#@app.route('/hello', methods=['GET'])

#def hello_world():
#    return "Hello World!"


@app.route('/transaction', methods=['POST'])
def add_transaction():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]

    new_txn = Transaction(usd_amount=usd_amount, lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp)

    db.session.add(new_txn)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully!"})


@app.route('/exchangeRate', methods=['GET'])
def get_exchange_rate():
    transactions = Transaction.query.all()

    usd_to_lbp_rates = []
    lbp_to_usd_rates = []

    for txn in transactions:
        if txn.usd_to_lbp:
            rate = txn.lbp_amount / txn.usd_amount
            usd_to_lbp_rates.append(rate)
        else:
            rate = txn.usd_amount / txn.lbp_amount
            lbp_to_usd_rates.append(rate)

    avg_usd_to_lbp = (sum(usd_to_lbp_rates) / len(usd_to_lbp_rates) if usd_to_lbp_rates else 0)
    avg_lbp_to_usd = (sum(lbp_to_usd_rates) / len(lbp_to_usd_rates) if lbp_to_usd_rates else 0)

    return jsonify({"usd_to_lbp": avg_usd_to_lbp, "lbp_to_usd": avg_lbp_to_usd})
