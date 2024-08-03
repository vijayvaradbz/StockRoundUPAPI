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

RespsignupStatus={
    "status":"Failed"
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
@token_required
def stockfeeddetails(stquoteId):
    data = request.get_data()
    json_object = json.loads(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return stockfeeddetail("STKFD", stquoteId, json_object)

@app.route('/indicesfeeddetails/<string:stquoteId>', methods=['POST'])
@token_required
def indicesfeeddetails(stquoteId):
    data = request.get_data()
    json_object = json.loads(data)
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return stockfeeddetail("INDSFD", stquoteId, json_object)

@app.route('/channelfeeddetails/<string:chquoteId>', methods=['POST'])
@token_required
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
    if userData["uid"] != "":
        SRUsername = userData["uid"];
        SRUserFilename = SRUsername[0].upper()+SRUsername[:2].upper()+"_"+str(ord(SRUsername[0].upper()))+"_SRUPUsers.txt"
        print(SRUserFilename);
        with open(r"COMDATA/"+SRUsername[0].upper()+"_User/"+SRUserFilename, 'r+') as u:
            userDataObj = json.load(u, strict=False)
            user = next(filter(lambda row: row["uid"].upper() == userData["uid"].upper() and row["email"].upper() == userData["email"].upper(), userDataObj), None);
            if(user != None):
                RespsignupStatus["status"] = "DuplicateUserID"
            else:
                userData["pwd"] = hashlib.sha384(str(userData["uid"] + userData["pwd"]).encode()).hexdigest()
                userData["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                userData["lang"] = "English";
                userDataObj.append(userData)
                u.seek(0)    
                json.dump(userDataObj, u, indent=4)    
                RespsignupStatus["status"] =  "Success"

        return RespsignupStatus


@app.route('/validateUserLogin', methods=['POST'])
def validateUserLogin():
    data = request.get_data();
    userLoginData = json.loads(data); 
    return validateUserLoginDetails(userLoginData)

def validateUserLoginDetails(userLoginData):
    ResploginStatus["loginstatus"] = "Failed";
    ResploginStatus["token"] = "";
    ResploginStatus["name"] = userLoginData["uid"];
    ResploginStatus["watchList"] = '[]';
    ResploginStatus["channelList"] = '[]';
    if userLoginData["uid"] != "":
        SRUsername = userLoginData["uid"];
        SRUserFilename = SRUsername[0].upper()+SRUsername[:2].upper()+"_"+str(ord(SRUsername[0].upper()))+"_SRUPUsers.txt"
        with open(r"COMDATA/"+SRUsername[0].upper()+"_User/"+SRUserFilename, 'r+') as f:
            userListObj = json.load(f, strict=False)
            userPwd = hashlib.sha384(str(userLoginData["uid"] + userLoginData["pwd"]).encode()).hexdigest()
            user = next(filter(lambda row: row["uid"].upper() == userLoginData["uid"].upper() and row["pwd"] == userPwd, userListObj), None);
            if(user != None):
                ResploginStatus["loginstatus"] = "Success";
                ResploginStatus["token"] = generate_auth_token(user["uid"]);
                ResploginStatus["name"] = user["uid"];
                ResploginStatus["watchList"] = user["watchList"];
                ResploginStatus["channelList"] = user["channels"];

                
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
def addChannel():
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return createChannel(json_object, json_object["name"])

def createChannel(channelData, chName):
    with open(r"COMDATA/Channels.txt", 'r+') as h:
        channelDataObj = json.load(h, strict=False)
        channelDataObj.append(channelData)
        h.seek(0)    
        json.dump(channelDataObj, h, indent=4)    
        h.truncate() 

    print("test");
    # channelData["cmt"] = "Channel Created"
    # channelData["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    # stockfeeddetail("CHFD", chName, channelData);
    return "Channel Created"

@app.route('/addChannelmembers/<string:channelId>', methods=['POST'])
@token_required
def addChannelMembers(channelId):
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return addChannelMember(channelId,json_object)

def addChannelMember(channelId, channelData):
    if channelData["uid"] != "":
        SRUsernameWL = channelData["uid"];
        SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
        with open(r"COMDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUserFilename, 'r+') as cm:
            channelDataObj = json.load(cm, strict=False)
            for row in channelDataObj:
                if row["uid"] == channelData["uid"]:
                    row["channels"]= channelData["channelList"]
                    break;
            
            cm.seek(0)    
            json.dump(channelDataObj, cm, indent=4)    
            cm.truncate() 
        return channelDataObj
    return "{}"

@app.route('/addUserChannels', methods=['POST'])
# @token_required
def addUserChannels():
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return addUserChannel(json_object)

def addUserChannel(channelData):
    if channelData["uid"] != "":
        SRUsernameWL = channelData["uid"];
        SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
        with open(r"COMDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUserFilename, 'r+') as cm:
            channelDataObj = json.load(cm, strict=False)
            for row in channelDataObj:
                if row["uid"] == channelData["uid"]:
                    row["channels"]= channelData["channelList"]
                    break;
            
            cm.seek(0)    
            json.dump(channelDataObj, cm, indent=4)    
            cm.truncate() 
        return channelDataObj
    return "{}"


@app.route('/addUserWatchList', methods=['POST'])
# @token_required
def addUserWatchList():
    data = request.get_data();
    json_object = json.loads(data); 
    return addWatchList(json_object)

def addWatchList(wathListData):
    if wathListData["uid"] != "":
        SRUsernameWL = wathListData["uid"];
        SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
        with open(r"COMDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUserFilename, 'r+') as cm:
            wathListDataObj = json.load(cm, strict=False)
            for row in wathListDataObj:
                if row["uid"] == wathListData["uid"]:
                    print(row);
                    row["watchList"]= wathListData["watchlist"]
                    break;
            
            cm.seek(0)    
            json.dump(wathListDataObj, cm, indent=4)    
            cm.truncate() 
        return wathListDataObj
    return "{}"

@app.route('/removeChannelmembers/<string:channelId>', methods=['POST'])
@token_required
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
    stockFeedObj = [];
    if os.path.exists("STKFD/"+stquoteId+".txt"):
        with open(r"STKFD/"+stquoteId+".txt", 'r+') as f:
            stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/indicesfeed/<string:IndicesId>', methods = ['GET'])
def getIndicesFeedbyId(IndicesId):
    stockFeedObj = [];
    if os.path.exists("INDSFD/"+IndicesId+".txt"):
        with open(r"INDSFD/"+IndicesId+".txt", 'r+') as f:
            stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/channelfeed/<string:chennalId>', methods = ['GET'])
def getChannelFeedbyId(chennalId):
    stockFeedObj = [];
    if os.path.exists("CHFD/"+chennalId+".txt"):
        with open(r"CHFD/"+chennalId+".txt", 'r+') as f:
            stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/otherfeed/<string:otherId>', methods = ['GET'])
def getOtherFeedbyId(otherId):
    stockFeedObj = [];
    if os.path.exists("OTFD/"+otherId+".txt"):
        with open(r"OTFD/"+otherId+".txt", 'r+') as f:
            stockFeedObj = json.load(f, strict=False)
    return stockFeedObj

@app.route('/globalIndices', methods = ['GET'])
def globalIndices():
    globalIndicesListObj = [];
    if os.path.exists("COMDATA/GlobalIndices.txt"):
        with open(r"COMDATA/GlobalIndices.txt", 'r+') as f:
            globalIndicesListObj = json.load(f, strict=False)
    return globalIndicesListObj

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




