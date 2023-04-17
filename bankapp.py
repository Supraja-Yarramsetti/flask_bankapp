
from flask import Flask, request,jsonify
from pymongo import MongoClient
from bank_methods import BankAccount

class BankAccount:

    def __init__(self, accountNumber: int, name: str, balance: float):
        self.accountNumber = accountNumber
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid amount"
        else:
            self.balance += amount
            return f"New balance: {self.balance} for Account number {self.accountNumber}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount"
        elif amount > self.balance:
            return "Insufficient balance"
        else:
            self.balance -= amount
            return f"New balance: {self.balance}"

    def bankFees(self):
        fee = self.balance * 0.05
        self.balance -= fee
        return f"Bank fees of {fee} applied. New balance: {self.balance}"

    def display(self):
        return f"Account Number: {self.accountNumber}  Name: {self.name}  ,Balance: {self.balance}"

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

# depositing the amount
@app.route("/BankAccount/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    accountNumber = data.get("accountNumber")
    amount = data.get("amount")
    # validate input data
    if not accountNumber or not amount:
        return jsonify({"error": "Insufficient data"}), 400
    try:
        accountNumber = int(accountNumber)
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400
    # retrieve account from database
    collection = get_db_collection()
    account = collection.find_one({"accountNumber": accountNumber})

    if not account:
        return jsonify({"error": "Account not found"}), 404
    # make deposit and update database
    new_balance = account['balance'] + amount
    collection.update_one({"accountNumber": accountNumber}, {"$set": {"balance": new_balance}})
    return jsonify({"message": f"Deposit of {amount} successful"})

# withdrawing the amount
@app.route("/BankAccount/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    accountNumber = data.get("accountNumber")
    amount = data.get("amount")
    # validate input data
    if not accountNumber or not amount:
        return jsonify({"error": "Insufficient data"}), 400
    try:
        accountNumber = int(accountNumber)
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400
    # retrieve account from database
    collection = get_db_collection()
    account = collection.find_one({"accountNumber": accountNumber})

    if not account:
        return jsonify({"error": "Account not found"}), 404
    # make withdrawal and update database
    if account['balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    new_balance = account['balance'] - amount
    collection.update_one({"accountNumber": accountNumber}, {"$set": {"balance": new_balance}})
    return jsonify({"message": f"Withdrawal of {amount} successful"})

# deducting bank fees
@app.route("/BankAccount/bankfees", methods=["POST"])
def bankFees():
    data = request.get_json()
    accountNumber = data.get("accountNumber")
    # validate input data
    if not accountNumber:
        return jsonify({"error": "Insufficient data"}), 400
    try:
        accountNumber = int(accountNumber)
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400
    # retrieve account from database
    collection = get_db_collection()
    account = collection.find_one({"accountNumber": accountNumber})

    if not account:
        return jsonify({"error": "Account not found"}), 404
    # deduct bank fees and update database
    accountObj = BankAccount(account['accountNumber'], account['name'], account['balance'])
    bankFee = accountObj.bankFees()
    collection.update_one({"accountNumber": accountNumber}, {"$set": {"balance": accountObj.balance}})
    return jsonify({"message": bankFee})



# displaying account details
@app.route("/BankAccount/display", methods=["GET"])
def display():
    accountNumber = request.args.get("accountNumber")
    # validate input data
    if not accountNumber:
        return jsonify({"error": "Insufficient data"}), 400
    try:
        accountNumber = int(accountNumber)
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400
    # retrieve account from database
    collection = get_db_collection()
    account = collection.find_one({"accountNumber": accountNumber})
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": f"Account details: {account}"})

if __name__ == '__main__':
    app.run(debug=True)