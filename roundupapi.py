from flask import Flask, request
app = Flask(__name__)
import json
from datetime import datetime
from bsedata.bse import BSE
from nsetools import Nse

b = BSE();
b = BSE(update_codes = True);

nse = Nse()

stData = {
        "uid": "vj1",
        "cmt": "Stock not good",
        "lang": "Tamil1",
        "dt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")      
    }

addUserData = {
        "uid": "vj1",
        "pwd": "erthfngngjgjfj$#@jjjdfjsdfdsjf",
        "email": "test@test.com",
        "signupdt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")        
    }

@app.route('/')
def index():
    return 'Hello StockRoundup'

@app.route('/stocks')
def getStocks():
    return stData

@app.route('/stockfeeddetails', methods=['POST'])
def stockfeeddetails():
    data = request.get_data()
    json_object = json.loads(data)
    print(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(json_object)
    return stockfeeddetail(json_object)
    

def stockfeeddetail(reqData):
    with open(r"C:\Project\StocksRoundUpAPI\TCS.txt", 'r+') as f:
        dataObj = json.load(f, strict=False)
        dataObj.append(reqData)      
        dataObj = sorted(dataObj, key=lambda r: datetime.strptime(r['dt'], '%d/%m/%Y %H:%M:%S'), reverse=True)
        print(dataObj)
        f.seek(0)       
        json.dump(dataObj, f, indent=4)
        f.truncate() 
    return dataObj

@app.route('/userSignUp', methods=['POST'])
def userSignUp():
    data = request.get_data();
    json_object = json.loads(data);
    print(data);   
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    print(json_object);
    return addUser(json_object)

def addUser(userData):
    with open(r"Users.txt", 'r+') as u:
        userDataObj = json.load(u, strict=False)
        userDataObj.append(userData)
        print(userData)
        u.seek(0)    
        json.dump(userDataObj, u, indent=4)    
        u.truncate() 
    return userDataObj


@app.route('/getUserData')
def getUserData():
    return getUsers()

def getUsers():
    with open(r"Users.txt", 'r+') as f:
        userListObj = json.load(f, strict=False)
       
    return userListObj

@app.route('/stockfeed')
def getStockFeed():
    with open(r"TCS.txt", 'r+') as f:
        userListObj = json.load(f, strict=False)
    return userListObj

@app.route('/bsestocklist')
def getBSEStockList():
    with open(r"BSEStockList..json", 'r+') as u:
        u.seek(0)    
        json.dump(b.getScripCodes(), u, indent=4)    
        u.truncate() 
    print(b.getScripCodes())


@app.route('/nsestocklist')
def getNSEStockList():
    print(nse.get_stock_codes())
    with open(r"NSEStockList.json", 'r+') as u:
        u.seek(0)    
        json.dump(nse.get_stock_codes, u, indent=4)    
        u.truncate() 
    print(nse.get_stock_codes())