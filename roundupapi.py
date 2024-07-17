from functools import wraps
import hashlib
import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import json
from datetime import datetime, timedelta
from bsedata.bse import BSE
from nsetools import Nse
import jwt

b = BSE();
b = BSE(update_codes = True);

ns = Nse()

# stData = {
#         "uid": "vj1",
#         "cmt": "Stock not good",
#         "lang": "Tamil1",
#         "dt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")      
#     }

ResploginStatus = {
       "loginstatus": "Failed",
       "name":"",
       "token": ""    
    }

# addUserData = {
#         "uid": "vj1",
#         "pwd": "erthfngngjgjfj$#@jjjdfjsdfdsjf",
#         "email": "test@test.com",
#         "signupdt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")        
#     }

@app.route('/')
def index():
    return 'Hello StockRoundup12'

# @app.route('/stocks')
# def getStocks():
#     return stData


#Common Methods
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        secret_key = "SRa1b2c3d4A1B2C3D4Roundup"
        # Check if token is passed in the headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]  # Extract the token part
                print(token);

        if not token:
            return "Token is missing!";
            # return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_iat":False})
            
        except Exception as e:
            print(str(e));
            return str(e), 403

        return f(*args, **kwargs)
    return decorated

# Insert Stock, Indices and Channel Feed data
@app.route('/stockfeeddetails/<string:stquoteId>', methods=['POST'])
def stockfeeddetails(stquoteId):
    data = request.get_data()
    json_object = json.loads(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return stockfeeddetail("STKFD", stquoteId, json_object)

@app.route('/indicesfeeddetails/<string:stquoteId>', methods=['POST'])
def indicesfeeddetails(stquoteId):
    data = request.get_data()
    json_object = json.loads(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return stockfeeddetail("INDSFD", stquoteId, json_object)

@app.route('/channelfeeddetails/<string:chquoteId>', methods=['POST'])
def channelfeeddetails(chquoteId):
    data = request.get_data()
    json_object = json.loads(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return stockfeeddetail("CHFD", chquoteId, json_object)
    

def stockfeeddetail(folderID, stquoteId, reqData):
    if not os.path.exists(""+folderID+"/"+stquoteId+".txt"):
        string_list = []
        string_list.append(reqData)
        with open(""+folderID+"/"+stquoteId+".txt", 'w') as file:
            file.write(json.dumps(string_list))
        return string_list
    else:
        with open(r""+folderID+"/"+stquoteId+".txt", 'r+') as f:
            dataObj = json.load(f, strict=False)
            dataObj.append(reqData) 
            dataObj = sorted(dataObj, key=lambda rd: datetime.strptime(rd['dt'], "%d/%m/%Y %H:%M:%S"), reverse=True)
            f.seek(0)       
            json.dump(dataObj, f, indent=4)
            f.truncate() 
        return dataObj

#User Signup, User details method
@app.route('/userSignUp', methods=['POST'])
def userSignUp():
    data = request.get_data();
    headerToken = request.authorization;
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return addUser(json_object)

def addUser(userData):
    with open(r"COMDATA/Users.txt", 'r+') as u:
        userDataObj = json.load(u, strict=False)
        userData["pwd"] = hashlib.sha384(str(userData["uid"] + userData["pwd"]).encode()).hexdigest()
        userData["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        userDataObj.append(userData)
        u.seek(0)    
        json.dump(userDataObj, u, indent=4)    
    return "success"


@app.route('/validateUserLogin', methods=['POST'])
def validateUserLogin():
    data = request.get_data();
    userLoginData = json.loads(data); 
    return validateUserLoginDetails(userLoginData)

def validateUserLoginDetails(userLoginData):
    # userLoginStatus = json.loads(ResploginStatus)
    with open(r"COMDATA/Users.txt", 'r+') as f:
        loginStatus = "Failed";
        userListObj = json.load(f, strict=False)
        userPwd = hashlib.sha384(str(userLoginData["uid"] + userLoginData["pwd"]).encode()).hexdigest()
        for user in userListObj:
            if (user["uid"] == userLoginData["uid"]) and (user["pwd"] == userPwd):
                ResploginStatus["loginstatus"] = "Success";
                ResploginStatus["token"] = generate_auth_token(user["uid"]);
                ResploginStatus["name"] = user["uid"];
                break;
    
    print(ResploginStatus);
    return ResploginStatus;

def generate_auth_token(userID):
    secret_key = "SRa1b2c3d4A1B2C3D4Roundup"
   
    payload = {
        "user_id": userID,
        "exp": datetime.now() + timedelta(seconds=30),
        "iat": datetime.now()
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256");
    return token

def getUsers():
    with open(r"COMDATA/Users.txt", 'r+') as f:
        userListObj = json.load(f, strict=False)
    return userListObj


#Add Channel Details
@app.route('/addChannel', methods=['POST'])
@token_required
def addChannel():
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return createChannel(json_object, json_object["name"])

def createChannel(channelData, chName):
    
    with open(r"COMDATA/Channels.txt", 'r+') as ch:
        channelDataObj = json.load(ch, strict=False)
        channelDataObj.append(channelData)
        ch.seek(0)    
        json.dump(channelDataObj, ch, indent=4)    
        ch.truncate() 

    channelData["cmt"] = "Channel Created"
    channelData["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    stockfeeddetail("CHFD", chName, channelData);
    return channelDataObj

@app.route('/addChannelmembers/<string:channelId>', methods=['POST'])
def addChannelMembers(channelId):
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return addChannelMember(channelId,json_object)

def addChannelMember(channelId, channelData):
    with open(r"COMDATA/"+channelId+".txt", 'r+') as cm:
        channelDataObj = json.load(cm, strict=False)
        channelDataObj.append(channelData)
        cm.seek(0)    
        json.dump(channelDataObj, cm, indent=4)    
        cm.truncate() 
    return channelDataObj

@app.route('/removeChannelmembers/<string:channelId>', methods=['POST'])
def removeChannelmembers(channelId):
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return removeChannelmember(channelId,json_object)

def removeChannelmember(channelId, channelData):
    with open(r"COMDATA/"+channelId+".txt", 'r+') as cr:
        channelDataObj = []
        channelDataObj = json.dumps(cr, strict=False)
        ind = channelDataObj.rfind(channelData)
        channelDataObj = channelDataObj.replace(channelDataObj,1,ind)
        cr.seek(0)    
        json.dump(channelDataObj, cr, indent=4)    
        cr.truncate() 
    return channelDataObj

#Get Stock feed
@app.route('/stockfeed/<string:stquoteId>', methods = ['GET'])
def getStockFeedbyId(stquoteId):
    with open(r"STKFD/"+stquoteId+".txt", 'r+') as f:
        stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/indicesfeed/<string:IndicesId>', methods = ['GET'])
def getIndicesFeedbyId(IndicesId):
    with open(r"INDSFD/"+IndicesId+".txt", 'r+') as f:
        stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/channelfeed/<string:chennalId>', methods = ['GET'])
def getChannelFeedbyId(chennalId):
    with open(r"CHFD/"+chennalId+".txt", 'r+') as f:
        stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/checksite', methods = ['GET'])
def checkSitefortesting():
    return "API Test is Valid"

@app.route('/bsestocklist')
def getBSEStockList():
    print(b.getScripCodes())
    with open(r"BSEStockListDetails.txt", 'r+') as ubse:
        ubse.seek(0)    
        json.dump(b.getScripCodes(), ubse, indent=4)    
        ubse.truncate() 
    return (b.getScripCodes())


#Get Stock List from NSE and BSE
@app.route('/nsestocklist')
def getNSEStockList():
    print(ns.get_index_list('self'));
    print(ns.get_stock_codes())
    with open(r"NSEStockListDetails.txt", 'r+') as unse:
        unse.seek(0)    
        json.dump(ns.get_index_list(), unse, indent=4)    
        unse.truncate();
    with open(r"NSEStockCodeList.txt", 'r+') as unse1:
        unse1.seek(0)    
        json.dump(ns.get_stock_codes(), unse1, indent=4)    
        unse1.truncate() 
    return (ns.get_stock_codes())


#Get Live Stock Data




