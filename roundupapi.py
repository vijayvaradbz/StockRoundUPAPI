from functools import wraps
import hashlib
import logging
import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import json
from datetime import datetime, timedelta
# from bsedata.bse import BSE
# from nsetools import Nse
import jwt

# b = BSE();
# b = BSE(update_codes = True);

# ns = Nse()
#logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

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

RespChannelData = {
       "members": ""
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

if __name__ == "__main__":
    app.run(host='0.0.0.0')

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
    try:
        data = request.get_data()
        json_object = json.loads(data)
        json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not os.path.exists("STKFD/"+stquoteId[0].upper()+"_Stocks"):
            os.makedirs("STKFD/"+stquoteId[0].upper()+"_Stocks");
        if not os.path.exists("STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks"):
            os.makedirs("STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks");
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath = "STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks/"+filename;
        return stockfeeddetail(filepath, stquoteId, json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"
    
@app.route('/addfeeddetails', methods=['POST'])
def addfeeddetails():
    try:
        data = request.get_data()
        json_object = json.loads(data)
        json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        stquoteId = json_object["stQuoteId"];
        if not os.path.exists("STKFD/"+stquoteId[0].upper()+"_Stocks"):
            os.makedirs("STKFD/"+stquoteId[0].upper()+"_Stocks");
        if not os.path.exists("STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks"):
            os.makedirs("STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks");
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath = "STKFD/"+stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks/"+filename;
        return stockfeeddetail(filepath, stquoteId, json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"



@app.route('/indicesfeeddetails/<string:stquoteId>', methods=['POST'])
@token_required
def indicesfeeddetails(stquoteId):
    try:
        data = request.get_data()
        json_object = json.loads(data)
        json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath = "INDSFD/"+filename;
        return stockfeeddetail(filepath, stquoteId, json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"
    
@app.route('/channelfeeddetails/<string:chquoteId>', methods=['POST'])
@token_required
def channelfeeddetails(chquoteId):
    try:
        data = request.get_data()
        json_object = json.loads(data)
        json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not os.path.exists("STKFD/"+chquoteId[0].upper()+"_Stocks"):
            os.makedirs("STKFD/"+chquoteId[0].upper()+"_Stocks");
        if not os.path.exists("STKFD/"+chquoteId[0].upper()+"_Stocks/"+chquoteId[:2].upper()+"_Stocks"):
            os.makedirs("STKFD/"+chquoteId[0].upper()+"_Stocks/"+chquoteId[:2].upper()+"_Stocks");
        filename =  chquoteId[0].upper()+chquoteId[:2].upper()+"_"+str(ord(chquoteId[0].upper()))+chquoteId+".txt";
        filepath = "STKFD/"+chquoteId[0].upper()+"_Stocks/"+chquoteId[:2].upper()+"_Stocks/"+filename;
        return stockfeeddetail(filepath, chquoteId, json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"
    
@app.route('/otherfeeddetails/<string:stquoteId>', methods=['POST'])
@token_required
def otherfeeddetails(stquoteId):
    try:
        data = request.get_data()
        json_object = json.loads(data)
        json_object["dt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath = "OTHERFD/"+filename;
        return stockfeeddetail(filepath, stquoteId, json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"


def stockfeeddetail(folderID, stquoteId, reqData):
    try:
        if not os.path.exists(folderID):
            string_list = []
            string_list.append(reqData)
            with open(folderID, 'w') as file:
                file.write(json.dumps(string_list))
            return string_list
        else:
            with open(r""+folderID, 'r+') as f:
                dataObj = json.load(f, strict=False)
                dataObj.append(reqData) 
                dataObj = sorted(dataObj, key=lambda rd: datetime.strptime(rd['dt'], "%d/%m/%Y %H:%M:%S"), reverse=True)
                f.seek(0)       
                json.dump(dataObj, f, indent=4)
                f.truncate() 
            return dataObj
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "[]"

#User Signup, User details method
@app.route('/userSignUp', methods=['POST'])
def userSignUp():
    try:
        data = request.get_data();
        headerToken = request.authorization;
        json_object = json.loads(data); 
        json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
        return addUser(json_object)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "SignUp Failed"

def addUser(userData):
    try:
        if userData["uid"] != "":
            SRUsername = userData["uid"];
        
            if not os.path.exists("USERDATA/"+SRUsername[0].upper()+"_User"):
                os.makedirs("USERDATA/"+SRUsername[0].upper()+"_User");
            if not os.path.exists("USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User"):
                os.makedirs("USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User");
            
            SRUserFilename = SRUsername[0].upper()+SRUsername[:2].upper()+"_"+str(ord(SRUsername[0].upper()))+"_SRUPUsers.txt";
            
            if not os.path.exists("USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User/"+SRUserFilename):
                string_list = []
                userData["pwd"] = hashlib.sha384(str(userData["uid"] + userData["pwd"]).encode()).hexdigest()
                userData["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                userData["lang"] = "English";
                string_list.append(userData)
                with open("USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User/"+SRUserFilename, 'w') as file:
                    file.write(json.dumps(string_list))
                RespsignupStatus["status"] =  "Success"
            else:
                with open(r"USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User/"+SRUserFilename, 'r+') as u:
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
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        RespsignupStatus["status"] =  "Failed"
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
    try:
        if userLoginData["uid"] != "":
            # SRUserToken = generate_auth_token(userLoginData["uid"]);
            SRUsername = userLoginData["uid"];
            SRUserFilename = SRUsername[0].upper()+SRUsername[:2].upper()+"_"+str(ord(SRUsername[0].upper()))+"_SRUPUsers.txt";
            with open(r"USERDATA/"+SRUsername[0].upper()+"_User/"+SRUsername[:2].upper()+"_User/"+SRUserFilename, 'r+') as f:
                userListObj = json.load(f, strict=False)
                userPwd = hashlib.sha384(str(userLoginData["uid"] + userLoginData["pwd"]).encode()).hexdigest()
                user = next(filter(lambda row: row["uid"].upper() == userLoginData["uid"].upper() and row["pwd"] == userPwd, userListObj), None);
                if(user != None):
                    ResploginStatus["loginstatus"] = "Success";
                    ResploginStatus["token"] = "SRUserToken";
                    ResploginStatus["name"] = user["uid"];
                    ResploginStatus["watchList"] = user["watchList"];
                    ResploginStatus["channelList"] = user["channels"];
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
                
    return ResploginStatus;

@app.route('/getChannelMembers', methods=['POST'])
def getChannelMembers():
    data = request.get_data();
    channelData = json.loads(data); 
    return getPrivateChannelMembers(channelData)

def getPrivateChannelMembers(channelData):
    RespChannelData["members"] = '[]';
    chName = channelData["name"]
    try:
        with open(r"CHANNEL/"+chName[0].upper()+"_Channel/"+chName[0].upper()+"_"+chName[1].upper()+"_Channel.txt", 'r+') as h:
            channelDataObj = json.load(h, strict=False);
            channelObj = next(filter(lambda row: row["name"].upper() == chName.upper(),channelDataObj), None);
            if(channelObj != None):
                RespChannelData["members"] = channelObj["members"];
        
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return RespChannelData
                

@app.route('/addChannelMembersDel', methods=['POST'])
def addChannelMembersDel():
    data = request.get_data();
    channelData = json.loads(data); 
    return getPrivateChannelMembers(channelData)

def addPrivateChannelMembers(channelData):
    RespChannelData["members"] = '[]';
    chName = channelData["name"]
    try:
        with open(r"CHANNEL/"+chName[0].upper()+"_Channel/"+chName[0].upper()+"_"+chName[1].upper()+"_Channel.txt", 'r+') as h:
            channelDataObj = json.load(h, strict=False);
            channelObj = next(filter(lambda row: row["name"].upper() == chName.upper(),channelDataObj), None);
            if(channelObj != None):
                RespChannelData["members"] = channelObj["members"];
        
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return RespChannelData

def generate_auth_token(userID):
    secret_key = "SRa1b2c3d4A1B2C3D4Roundup"
   
    payload = {
        "user_id": userID,
        "exp": datetime.now() + timedelta(seconds=30000),
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
    try:
        if not os.path.exists("CHANNEL/"+chName[0].upper()+"_Channel"):
            os.makedirs("CHANNEL/"+chName[0].upper()+"_Channel");
        
        if not os.path.exists("CHANNEL/"+chName[0].upper()+"_Channel/"+chName[0].upper()+"_"+chName[1].upper()+"_Channel.txt"):
            string_list = []
            string_list.append(channelData)
            with open("CHANNEL/"+chName[0].upper()+"_Channel/"+chName[0].upper()+"_"+chName[1].upper()+"_Channel.txt", 'w') as file:
                file.write(json.dumps(string_list))
        else:
            with open(r"CHANNEL/"+chName[0].upper()+"_Channel/"+chName[0].upper()+"_"+chName[1].upper()+"_Channel.txt", 'r+') as h:
                channelDataObj = json.load(h, strict=False)
                channelDataObj.append(channelData)
                h.seek(0)    
                json.dump(channelDataObj, h, indent=4)    
                h.truncate() 

        # userchannel = json.loads({"name":channelData["name"], "access":channelData["access"], "permission":"owner"});
        # addUserChannel(userchannel);
        return "Success"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Failed"
    
@app.route('/addChannelmembers', methods=['POST'])
def addChannelMembers():
    data = request.get_data();
    json_object = json.loads(data); 
    channelId = json_object["ChannelId"]
    channelData = json_object["ChannelData"]
    print(json_object);
    return addChannelMember(channelId,channelData)

def addChannelMember(channelId, channelData):
    try:
        if channelId != "":
            with open(r"CHANNEL/"+channelId[0].upper()+"_Channel/"+channelId[0].upper()+"_"+channelId[1].upper()+"_Channel.txt", 'r+') as h:
                channelListObj = json.load(h, strict=False)
                print(channelListObj)
                for row in channelListObj:
                    if row["name"] == channelId:
                        row["members"].append(channelData);
                        break;
                
                h.seek(0)    
                json.dump(channelListObj, h, indent=4)    
                h.truncate() 
                return "Success"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Member is not added to the Channel"
    

@app.route('/addChanneltoUsers', methods=['POST'])
def addChanneltoUsers():
    data = request.get_data();
    json_object = json.loads(data); 
    return addChanneltoUser(json_object)

def addChanneltoUser(channelData):
    try:
        if channelData["uid"] != "":
            SRUsernameWL = channelData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cm:
                channelDataObj = json.load(cm, strict=False)
                chUserList = [];
                for row in channelDataObj:
                    if row["uid"] == channelData["uid"]:
                        row["channels"].append(channelData["channelList"])
                        cm.seek(0)  
                        json.dump(channelDataObj, cm, indent=4)    
                        cm.truncate() 
                        break;
                
            return channelData
        return "{}"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Member is not added to the Channel"
    

@app.route('/removeChannelmember', methods=['POST'])
def removeChannelMember():
    data = request.get_data();
    json_object = json.loads(data); 
    return removeChMember(json_object)

def removeChMember(channelData):
    try:
        channelId = channelData["ChannelId"]
        if channelId != "":
            with open(r"CHANNEL/"+channelId[0].upper()+"_Channel/"+channelId[0].upper()+"_"+channelId[1].upper()+"_Channel.txt", 'r+') as h:
                channelListObj = json.load(h, strict=False)
                
                for rowCH in channelListObj:
                    if rowCH["name"] == channelId:
                        data = [row for row in rowCH["members"] if (row["userName"] != channelData["userName"])]
                        rowCH["members"] = data
                        break;
                
                h.seek(0)    
                json.dump(channelListObj, h, indent=4)    
                h.truncate() 
                return "Success"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Member is not added to the Channel"
    

@app.route('/removeChannelfromUsers', methods=['POST'])
def removeChannelfromUsers():
    data = request.get_data();
    json_object = json.loads(data); 
    return removeChannelfromUser(json_object)

def removeChannelfromUser(channelData):
    try:
        if channelData["uid"] != "":
            SRUsernameWL = channelData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cm:
                channelDataObj = json.load(cm, strict=False)
                chUserList = [];
                for rowCh in channelDataObj:
                    if rowCh["uid"] == channelData["uid"]:
                        data = [row for row in rowCh["channels"] if (row["name"] != channelData["name"])]
                        rowCh["channels"] = data
                        cm.seek(0)  
                        json.dump(channelDataObj, cm, indent=4)    
                        cm.truncate() 
                        break;
                
            return channelData
        return "{}"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Member is not added to the Channel"


@app.route('/addUserChannels', methods=['POST'])
# @token_required
def addUserChannels():
    data = request.get_data();
    json_object = json.loads(data); 
    json_object["signupdt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S");
    return addUserChannel(json_object)

def addUserChannel(channelData):
    try:
        if channelData["uid"] != "":
            SRUsernameWL = channelData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cm:
                channelDataObj = json.load(cm, strict=False)
                for row in channelDataObj:
                    if row["uid"] == channelData["uid"]:
                        row["channels"]= channelData["channelList"]
                        break;
                
                cm.seek(0)    
                json.dump(channelDataObj, cm, indent=4)    
                cm.truncate() 
            return channelData
        return "{}"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Channel not added to the User"


@app.route('/addUserWatchList', methods=['POST'])
# @token_required
def addUserWatchList():
    data = request.get_data();
    json_object = json.loads(data); 
    return addWatchList(json_object)

def addWatchList(wathListData):
    try:
        if wathListData["uid"] != "":
            SRUsernameWL = wathListData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cm:
                wathListDataObj = json.load(cm, strict=False)
                for row in wathListDataObj:
                    if row["uid"] == wathListData["uid"]:
                        row["watchList"]= wathListData["watchlist"]
                        break;
                
                cm.seek(0)    
                json.dump(wathListDataObj, cm, indent=4)    
                cm.truncate() 
            return wathListData
        return "UserName is Missing"
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "WatchList not added to the User"
    
@app.route('/removeUserWatchList', methods=['POST'])
def removeUserWatchList():
    data = request.get_data();
    json_object = json.loads(data); 
    return removeWatchListByUser(json_object)

def removeWatchListByUser(wathListData):
     try:
        if wathListData["uid"] != "":
            SRUsernameWL = wathListData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cr:
                watchListObj = json.load(cr, strict=False);
                for rowWL in watchListObj:
                   if rowWL["uid"] == wathListData["uid"]:
                        # data = [row for row in rowWL["watchList"] if (row["options"] != wathListData["options"] and row["symbol"] != wathListData["symbol"])]
                        data = [row for row in rowWL["watchList"] if (row["symbol"] != wathListData["symbol"])]
                        rowWL["watchList"] = data

                cr.seek(0)    
                json.dump(watchListObj, cr, indent=4)    
                cr.truncate() 
            return "Success"
     except Exception as e:
        print(e);
        logging.error(f"An Error Occured: {e}")
        return "Failed"


@app.route('/removeChannelmembers', methods=['POST'])
@token_required
def removeChannelmembers():
    data = request.get_data();
    json_object = json.loads(data); 
    return removeChannelmember(json_object)

def removeChannelmember(channelData):
    try:
        if channelData["uid"] != "":
            channelId = channelData["name"]
            with open(r"CHANNEL/"+channelId[0].upper()+"_Channel/"+channelId[0].upper()+"_"+channelId[1].upper()+"_Channel.txt", 'r+') as h:
                channelListObj = json.load(h, strict=False)
                data = [row for row in channelListObj if (row["name"] != channelListObj["name"])]
                h.seek(0)    
                json.dump(channelListObj, h, indent=4)    
                h.truncate() 
            return "Success";    
        
        return channelData
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Failed"


@app.route('/removeUserChannel', methods=['POST'])
@token_required
def removeUserChannel():
    data = request.get_data();
    json_object = json.loads(data); 
    return removeChannelByUser(json_object)

def removeChannelByUser(ChannelData):
     try:
        if ChannelData["uid"] != "":
            SRUsernameWL = ChannelData["uid"];
            SRUserFilename = SRUsernameWL[0].upper()+SRUsernameWL[:2].upper()+"_"+str(ord(SRUsernameWL[0].upper()))+"_SRUPUsers.txt"
            with open(r"USERDATA/"+SRUsernameWL[0].upper()+"_User/"+SRUsernameWL[:2].upper()+"_User/"+SRUserFilename, 'r+') as cr:
                channelDataObj = json.loads(cr, strict=False)
                data = [row for row in channelDataObj if (row["name"] != ChannelData["name"])]
                cr.seek(0)    
                json.dumps(data, cr, indent=4)    
                cr.truncate() 
            
            if ChannelData["uid"] != "":
                channelId = ChannelData["name"]
                with open(r"CHANNEL/"+channelId[0].upper()+"_Channel/"+channelId[0].upper()+"_"+channelId[1].upper()+"_Channel.txt", 'r+') as h:
                    channelListObj = json.load(h, strict=False)
                    data = [row for row in channelListObj if (row["name"] != channelId)]
                    h.seek(0)    
                    json.dumps(data, h, indent=4)    
                    h.truncate() 
                
            return "Success"
     except Exception as e:
        logging.error(f"An Error Occured: {e}")
        return "Failed"


#Get Stock feed
@app.route('/stockfeed/<string:stquoteId>', methods = ['GET'])
def getStockFeedbyId(stquoteId):
    stockFeedObj = [{'uid': 'SR Admin', 'cmt': 'This Symbol is InActive for sometime in this Forum. Post your comments to make it Active', 'lang': 'English', 'dt': datetime.now()},{'uid': 'SR Admin', 'cmt': 'Welcome to Stock Roundup Social App. Join with Stock Roundup App to engage in discussions about global Indices, Stocks and receive updates from other traders/investors. Stay informed and connected with fellow investors/traders in the Stock market Community with the Language/Script you are familiar.', 'lang': 'English', 'dt': datetime.now()}];
    try:
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath =  stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks/"+filename;
        if os.path.exists("STKFD/"+filepath):
            with open(r"STKFD/"+filepath, 'r+') as f:
                stockFeedObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")

    return stockFeedObj

@app.route('/stkfeed', methods=['POST'])
def getStkFeedbyId():
    data = request.get_data();
    jsonData = json.loads(data); 
    stquoteId = jsonData["symbol"];
    stockFeedObj = [{'uid': 'SR Admin', 'cmt': 'This Symbol is InActive for sometime in this Forum. Post your comments to make it Active', 'lang': 'English', 'dt': datetime.now()},{'uid': 'SR Admin', 'cmt': 'Welcome to Stock Roundup Social App. Join with Stock Roundup App to engage in discussions about global Indices, Stocks and receive updates from other traders/investors. Stay informed and connected with fellow investors/traders in the Stock market Community with the Language/Script you are familiar.', 'lang': 'English', 'dt': datetime.now()}];
    try:
        filename =  stquoteId[0].upper()+stquoteId[:2].upper()+"_"+str(ord(stquoteId[0].upper()))+stquoteId+".txt";
        filepath =  stquoteId[0].upper()+"_Stocks/"+stquoteId[:2].upper()+"_Stocks/"+filename;
        if os.path.exists("STKFD/"+filepath):
            with open(r"STKFD/"+filepath, 'r+') as f:
                stockFeedObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")

    return stockFeedObj



@app.route('/indicesfeed/<string:IndicesId>', methods = ['GET'])
def getIndicesFeedbyId(IndicesId):
    stockFeedObj = [{'uid': 'SR Admin', 'cmt': 'This Symbol is InActive for sometime in this Forum. Post your comments to make it Active', 'lang': 'English', 'dt': datetime.now()},{'uid': 'SR Admin', 'cmt': 'Welcome to Stock Roundup Social App. Join with Stock Roundup App to engage in discussions about global Indices, Stocks and receive updates from other traders/investors. Stay informed and connected with fellow investors/traders in the Stock market Community with the Language/Script you are familiar.', 'lang': 'English', 'dt': datetime.now()}];
    try:
        filename =  IndicesId[0].upper()+IndicesId[:2].upper()+"_"+str(ord(IndicesId[0].upper()))+IndicesId+".txt";
        if os.path.exists("INDSFD/"+filename):
            with open(r"INDSFD/"+filename, 'r+') as f:
                stockFeedObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return stockFeedObj

@app.route('/channelfeed/<string:chennalId>', methods = ['GET'])
def getChannelFeedbyId(chennalId):
    stockFeedObj = [{'uid': 'SR Admin', 'cmt': 'This Channel is InActive for sometime in this Forum. Post your comments to make it Active', 'lang': 'English', 'dt': datetime.now()},{'uid': 'SR Admin', 'cmt': 'Welcome to Stock Roundup Social App. Join with Stock Roundup App to engage in discussions about global Indices, Stocks and receive updates from other traders/investors. Stay informed and connected with fellow investors/traders in the Stock market Community with the Language/Script you are familiar.', 'lang': 'English', 'dt': datetime.now()}];
    try:
        filename =  chennalId[0].upper()+chennalId[:2].upper()+"_"+str(ord(chennalId[0].upper()))+chennalId+".txt";
        filepath =  chennalId[0].upper()+"_Channel/"+chennalId[:2].upper()+"_Channel/"+filename;
        if os.path.exists("CHFD/"+filepath):
            with open(r"CHFD/"+filepath, 'r+') as f:
                stockFeedObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return stockFeedObj

@app.route('/otherfeed/<string:otherId>', methods = ['GET'])
def getOtherFeedbyId(otherId):
    stockFeedObj = [{'uid': 'SR Admin', 'cmt': 'This Symbol is InActive for sometime in this Forum. Post your comments to make it Active', 'lang': 'English', 'dt': datetime.now()},{'uid': 'SR Admin', 'cmt': 'Welcome to Stock Roundup Social App. Join with Stock Roundup App to engage in discussions about global Indices, Stocks and receive updates from other traders/investors. Stay informed and connected with fellow investors/traders in the Stock market Community with the Language/Script you are familiar.', 'lang': 'English', 'dt': datetime.now()}];
    try:
        filename =  otherId[0].upper()+otherId[:2].upper()+"_"+str(ord(otherId[0].upper()))+otherId+".txt";
        if os.path.exists("OTFD/"+filename):
            with open(r"OTFD/"+filename, 'r+') as f:
                stockFeedObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return stockFeedObj

@app.route('/globalIndices', methods = ['GET'])
def globalIndices():
    globalIndicesListObj = [];
    try:
        if os.path.exists("COMDATA/GlobalIndices.txt"):
            with open(r"COMDATA/GlobalIndices.txt", 'r+') as f:
                globalIndicesListObj = json.load(f, strict=False)
    except Exception as e:
        logging.error(f"An Error Occured: {e}")
    return globalIndicesListObj

@app.route('/checksite', methods = ['GET'])
def checkSitefortesting():
    return "API Test is Valid"

# @app.route('/bsestocklist')
# def getBSEStockList():
#     print(b.getScripCodes())
#     with open(r"BSEStockListDetails.txt", 'r+') as ubse:
#         ubse.seek(0)    
#         json.dump(b.getScripCodes(), ubse, indent=4)    
#         ubse.truncate() 
#     return (b.getScripCodes())


#Get Stock List from NSE and BSE
# @app.route('/nsestocklist')
# def getNSEStockList():
#     print(ns.get_index_list('self'));
#     print(ns.get_stock_codes())
#     with open(r"NSEStockListDetails.txt", 'r+') as unse:
#         unse.seek(0)    
#         json.dump(ns.get_index_list(), unse, indent=4)    
#         unse.truncate();
#     with open(r"NSEStockCodeList.txt", 'r+') as unse1:
#         unse1.seek(0)    
#         json.dump(ns.get_stock_codes(), unse1, indent=4)    
#         unse1.truncate() 
#     return (ns.get_stock_codes())


#Get Live Stock Data




