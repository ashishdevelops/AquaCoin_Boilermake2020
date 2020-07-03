from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pyrebase
import uuid
import requests

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyAVKhVQUmUeoS3Vj5pVjzm-tHi2XjUEYtk",
  "authDomain": "aquacoin-a0002.firebaseapp.com",
  "databaseURL": "https://aquacoin-a0002.firebaseio.com",
  "storageBucket": "aquacoin-a0002.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
logged_in = 0
user_id = 0
user_data = {}
tokenAddress = "0xab0ed64d89446981b2a07e9789e9520e46a5e01a"

@app.route("/")
def home():
	global logged_in
	if logged_in == 0:
		return redirect("/login/")
	else:
		transaction_list = db.child("MARKET").get()
		print(transaction_list)
		return render_template('index.html', username = user_data["name"],\
			balance = user_data["balance"], transactions = transaction_list,\
			database = db, fromAddress =  user_data["walletAddress"])

@app.route("/login/")
def login():
	return render_template('login.html')

@app.route("/logout/")
def logout():
	global logged_in
	global user_id
	global user_data
	logged_in = 0
	user_id = 0
	user_data = {}
	return redirect("/login/")

@app.route("/attempt-login/", methods=['POST'])
def attemptLogin():
	global logged_in
	global user_id
	global user_data
	if request.method == "POST":
		result = request.form
		username = result["user"]
		password = result["pass"]
		users = db.child("USERS").get()
		authenticated = 0
		for user in users.each():
			if user.val()["name"] == username:
				if user.val()["password"] == password:
					authenticated = 1
					logged_in = 1
					user_id = user.key()
					user_data = user.val()
					break
			#Redirect to welcome page
		if authenticated == 1:
			return redirect(url_for('home'))
		else:
			return redirect(url_for('login'))

	else:
	    if logged_in == 1:
	        return redirect(url_for('welcome'))
	    else:
	        return redirect(url_for('login'))

@app.route("/firebase/")
def debug():
	db = firebase.database()
	return db.get().val()

@app.route("/adduser/")
def add_user():
	userID = str(uuid.uuid4())[:6]
	balance = int(request.args.get('balance'))
	name = request.args.get('name')
	walletAddress = request.args.get('pay')
	password = request.args.get('pass')
	user = {"name": name,"balance": balance,"walletAddress": walletAddress, "password": password}
	db.child("USERS").child(userID).set(user)
	return "success"
	#balnce, id, name, payment info

@app.route("/trans/")
def transactions():
	transID = str(uuid.uuid4())
	sender = request.args.get('i')
	reciever = request.args.get('f')
	amount = int(request.args.get('amt'))
	data = {"initial": sender, "final": reciever,"amount": amount}
	db.child("TRANSACTIONS").child(transID).set(data)
	#i_balance = db.child("USERS").child(initial)
	#db.child("USERS").child(initial).set({"balance": name}).get
	return "success"
	#balnce, id, name, payment info

@app.route("/removeuser/")
def remove_user():
	u = request.args.get('u')
	db.child("USERS").child(u).remove()
	return "removed " + u

@app.route("/market/")
def addmarket():
	transID = str(uuid.uuid4())
	seller = request.args.get('sell')
	amount = int(request.args.get('amt'))
	price = int(request.args.get('price'))
	data = {"seller": seller, "count": amount,"price": price}
	db.child("MARKET").child(transID).set(data)
	return "success"

@app.route("/sell/", methods=['POST'])
def sell():
	global user_id
	if request.method == "POST":
		transID = str(uuid.uuid4())
		result = request.form
		count = int(result["count"])
		price = int(result["price"])
		data = {"seller": user_id, "count": count,"price": price}
		db.child("MARKET").child(transID).set(data)
		return redirect(url_for('home'))

@app.route("/settings/", methods = ["POST"])
def addWalletAddress():
	global user_id
	if request.method == "POST":
		result = request.form
		walletAddress = result["address"]
		db.child("USERS").child(user_id).update({"walletAddress": walletAddress})
		return redirect(url_for('home'))

@app.route("/success/", methods = ["POST"])
def successTrans():
    global user_id
    if request.method == "POST":
        result = request.form
        marketID = result["marketID"]
        print(marketID)
        db.child("MARKET").child(marketID).remove()
        return redirect(url_for('home'))

# @app.route("/purchase/", methods = ["POST"])
# def confirmPurchase():
#     global user_id
#     global user_data
#     if request.method == "POST":
#         result = request.form
#         marketID = result["data"]
#         sellerID = db.child("MARKET").child(marketID).get().val()["seller"]
#         sellerWallet = db.child("USERS").child(sellerID).get().val()["walletAddress"]
#         buyerWallet = user_data["walletAddress"]
#         aqua = db.child("MARKET").child(marketID).get().val()["count"]
#         data = {"toAddress": sellerWallet, "fromAddress": buyerWallet, "money": aqua}
#         return render_template('purchase.html', data=data)


if __name__ == "__main__":
    app.run()
