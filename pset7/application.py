from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", "Go ahead")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure second password was submitted
        elif not request.form.get("password_s"):
            return apology("must provide password again")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username not exist
        if len(rows) == 1:
            return apology("username exists already")

        # ensure two password arguments agree
        if request.form.get("password") != request.form.get("password_s"):
            return apology("password does not match")
            
        # encrypy password
        hash = pwd_context.encrypt(request.form.get("password"))

        # verify a password...
        #ok = pwd_context.verify("somepass", hash)

        # register new user to database
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :pwd)", username=request.form.get("username"), pwd=hash)

        # remember the new user and keep logging in
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))[0]["id"]
        session["user_name"] = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))[0]["username"]
        
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/index", methods=["GET"])
@login_required
def index():

    # check current cash from users
    rows1 = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    cash = usd(rows1[0]["cash"])

    # collect user current stock from assets - symbol & stock_name & share
    assets = db.execute("SELECT symbol, stock_name, SUM(share) FROM assets WHERE user_id=:user_id GROUP BY stock_name", user_id=session["user_id"])

    # check current stock price 
    for i in range(int(len(assets))):
        assets[i]["cost"] = usd(lookup(assets[i]["symbol"])["price"])

    # calculate stock's value
    for i in range(int(len(assets))):
        assets[i]["value"] = usd(lookup(assets[i]["symbol"])["price"] * int(assets[i]["SUM(share)"]))
        
    # calculate stock's total stock value
    sum_value = 0
    for i in range(int(len(assets))):
        sum_value += lookup(assets[i]["symbol"])["price"] * int(assets[i]["SUM(share)"])
    total = usd(sum_value + rows1[0]["cash"])

    # feed back the query
    return render_template("index.html", assets=assets, cash=cash, total=total)

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")        
        
        # pass in symbol to lookup
        result = lookup(request.form.get("symbol"))
        
        # ensure symbol is valid
        if result == None:
            return apology("invalid symbol")        
        
        # feed back the query
        return render_template("quoted.html", name=result["name"], symbol=result["symbol"], price=result["price"])

    # else if user reached route via GET (as by clicking a link or via redirect)
    else: 
        return render_template("quote.html")   
    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")        
            
        # ensure symbol is valid
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")

        # ensure share was submitted
        if not request.form.get("share"):
            return apology("must provide share")   

        # ensure share is integer
        if not RepresentInt(request.form.get("share")):
            return apology("must be positive integer")  

        # ensure share is positive
        if int(request.form.get("share")) < 1:
            return apology("must be positive integer")  

        # pass in symbol to lookup to obtain stock info
        result = lookup(request.form.get("symbol"))

        # check user's current cash
        rows = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]
        
        # ensure user has enough money to buy 
        recount = cash - int(request.form.get("share"))*result["price"]
        if recount < 0:
            return apology("no enough cash to buy")
    
        # save transaction to database for records
        db.execute("INSERT INTO records (user, user_id, symbol, buy_or_sell, share, price) VALUES (:user, :user_id, :symbol, :bs, :share, :price)", user=session["user_name"], user_id=session["user_id"], symbol=result["symbol"], bs="BUY", share=request.form.get("share"), price=result["price"])

        assets = db.execute("SELECT symbol, share, cost FROM assets WHERE user_id=:user_id GROUP BY symbol HAVING symbol=:symbol", user_id=session["user_id"], symbol=request.form.get("symbol").upper())
        # check if user owns the stock already
        if len(assets) == 0:  
            # save new stock to assets
            db.execute("INSERT INTO assets (user, user_id, symbol, stock_name, share, cost) VALUES (:user, :user_id, :symbol, :sn, :share, :cost)", user=session["user_name"], user_id=session["user_id"], symbol=result["symbol"], sn=result["name"], share=request.form.get("share"), cost=result["price"]*int(request.form.get("share")))
        else:
            # update old stock to assets
            new_share = int(assets[0]["share"]) + int(request.form.get("share"))
            new_cost = assets[0]["cost"] + int(request.form.get("share"))*result["price"]
            db.execute("UPDATE assets SET share=:share, cost=:cost WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=request.form.get("symbol").upper(), share=new_share, cost=new_cost)

        # update user's cash    
        db.execute("UPDATE users SET cash=:recount WHERE id=:user_id", recount=recount, user_id=session["user_id"])
      
        # feed back the query
        return render_template("success.html", name=result["name"], symbol=result["symbol"], price=result["price"], share=request.form.get("share"), bs="bought")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else: 
        return render_template("buy.html")   

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")        
            
        # ensure symbol is valid
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")

        # ensure share was submitted
        if not request.form.get("share"):
            return apology("must provide share")   

        # ensure share is integer
        if not RepresentInt(request.form.get("share")):
            return apology("must be positive integer")  

        # ensure share is positive
        if int(request.form.get("share")) < 1:
            return apology("must be positive integer")   

        # check user's current assets - symbol & share & cost
        assets = db.execute("SELECT symbol, share, cost FROM assets WHERE user_id=:user_id GROUP BY symbol HAVING symbol=:symbol", user_id=session["user_id"], symbol=request.form.get("symbol").upper())

        # ensure user has this stock to sell 
        if len(assets) == 0:
            return apology("no such stock available")

        # ensure user has enough shares to sell 
        #recount = cash - int(request.form.get("share"))*result["price"]
        if int(request.form.get("share")) > int(assets[0]["share"]):
            return apology("no enough share to sell")

        # pass in symbol to lookup to obtain stock info
        result = lookup(request.form.get("symbol"))

        # save transaction to database for records
        db.execute("INSERT INTO records (user, user_id, symbol, buy_or_sell, share, price) VALUES (:user, :user_id, :symbol, :bs, :share, :price)", user=session["user_name"], user_id=session["user_id"], symbol=result["symbol"], bs="SELL", share=request.form.get("share"), price=result["price"])

        # save transaction to database for assets
        new_share = int(assets[0]["share"]) - int(request.form.get("share"))
        new_cost = assets[0]["cost"] - int(request.form.get("share"))*result["price"]
        db.execute("UPDATE assets SET share=:share, cost=:cost WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=request.form.get("symbol").upper(), share=new_share, cost=new_cost)

        # check user's current cash and update it
        cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["cash"]
        recount = cash + int(request.form.get("share"))*result["price"]
        db.execute("UPDATE users SET cash=:recount WHERE id=:user_id", recount=recount, user_id=session["user_id"])
      
        # feed back the query
        return render_template("success.html", name=result["name"], symbol=result["symbol"], price=result["price"], share=request.form.get("share"), bs="sold")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else: 
        return render_template("sell.html")   

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    # access user's transactions from records
    records = db.execute("SELECT * FROM records WHERE user_id=:user_id", user_id=session["user_id"])
    
    return render_template("history.html", records=records)
    
@app.route("/personal", methods=["GET","POST"])
@login_required
def personal():
    """Show personal management."""

    # if user reached route via POST (as by submitting a form via POST)    
    if request.method == "POST":
     
        # check if any input field are empty
        if not request.form.get("password") or not request.form.get("new_password") or not request.form.get("new_password_s"):
            return apology("must provide these three field")
        
        # check user current password
        info = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=session["user_id"])
        if not pwd_context.verify(request.form.get("password"), info[0]["hash"]):
            return apology("current password does not match")
            
        # check if two new passwords matched up
        if request.form.get("new_password") != request.form.get("new_password_s"):
            return apology("new password does not match up")
        
        # hash new password
        hash = pwd_context.encrypt(request.form.get("new_password"))
        
        # update new password at users
        db.execute("UPDATE users SET hash=:pwd WHERE id=:user_id", pwd=hash, user_id=session["user_id"])
        
        # inform user the password changed successfully
        return render_template("congrats.html")
    
    # else if user reached route via GET (as by clicking a link or via redirect)   
    else:
        return render_template("personal.html")
    
