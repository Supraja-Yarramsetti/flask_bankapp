
from flask import Flask, request,jsonify
from pymongo import MongoClient


class BankAccount:

    def __init__(self, accountNumber: int, name: str, balance: float):
        self.accountNumber = accountNumber
        self.name = name
        self.balance = balance
    # class method is invoked directly without creating instence of the class
    @classmethod
    def addUser(cls, accountNumber, name, balance):
        return cls(accountNumber, name, balance)



app = Flask(__name__)
@app.route('/', methods=["GET"])
def welcome():
    return 'Welcome Our Bank !'


client = MongoClient('mongodb://localhost:27017/')
db = client['bank']
collection = db['users']


def get_db_collection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bank']
    collection = db['users']
    return collection


# creating new user
@app.route("/BankAccount/adduser", methods=["POST"])
def addUser():
    data = request.get_json()
    accountNumber = data.get("accountNumber")
    name = data.get("name")
    balance = data.get("balance")
    # validate input data
    if not accountNumber or not name or not balance:
        return jsonify({"error": "Insufficient data"}), 400
    try:
        accountNumber = int(accountNumber)
        balance = float(balance)
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400

    # create new account and update database
    collection = get_db_collection()
    new_user = {"accountNumber": accountNumber, "name": name, "balance": balance}
    result = collection.insert_one(new_user)
    return jsonify({"message": "New user added successfully"})



if __name__ == '__main__':
    app.run(debug=True)