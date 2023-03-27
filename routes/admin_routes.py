from flask import Flask,session,request,jsonify,Blueprint,render_template
import hashlib
from flask_mysqldb import MySQL
import random
import datetime
from pytz import timezone
from extensions import mysql
from models.admin_models import Models as db
from werkzeug.utils import secure_filename


api=Blueprint('api',__name__,url_prefix='/api')


# get Only Date Function
def getDateOnly():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    datetimeee=datetime.datetime(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    datetimee=str(datetimeee)
    return datetimee


# FOR UPLOAD IMAGE
def genToken():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    datetimeee = datetime.datetime(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    datetimee = str(datetimeee)
    ranNew = str(random.randint(00000, 99999))
    ran_text = str('thalaiva')
    
    tknname = ran_text+datetimee+ran_text
    tknname = tknname.replace(":", "")
    tknname = tknname.replace("-", "")
    tknname = tknname.replace(" ", "")
    tknname = tknname.replace(",", "")
    return tknname


# OTP
def onetimepassword():
    num1 = str(123456)
    # num1 = str(random.randint(100000,999999))
    return num1


############### ADMIN LOGIN ###############




# ROUTE FOR LOGIN
@api.route('/user_login',methods=['POST','GET'])
def login():

    if request.method=='POST':

        # content = request.json
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        cat_id = request.form['cat_id']
        # token = request.form['token']
        current_date=getDateOnly()
        
        data=db.checkAdminLogin(uname,passs,cat_id)
       
        # Different date with Correct Password
        if data and data['login_attempts']>=5 and data['login_date']!=current_date:
            db.resetPasswordAttemptswithUname(uname)

        if data:
            print(data)
            if data['login_attempts']>=5 and data['login_date']==current_date:
                return jsonify({'status':False,'msg':'Too many Failed Login Attempts, Please retry after sometime...'})
            else:    
                db.resetPasswordAttemptswithUname(uname)
            
            # OTP GENERATION
                # otp = str(random.randint(100000,999999))
                otp = onetimepassword()
                print(otp)
                session['login_otp'] = otp
                db.otpadd(otp,uname) 
                
                return jsonify({'status':True,'msg':'Please Enter The OTP'}) 
        else:
            data=db.getLoginAttemptsWithUname(uname)
            if data['login_attempts']>=5 and data['login_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed login Attempts, Please retry after sometime...'})
            db.failedLogin(current_date,uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'})


# ROUTE FOR OTP VALIDATION
@api.route('/validate_otp',methods=['POST','GET'])
def validate_otp():
    if request.method=='POST':
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        cat_id = request.form['cat_id']
        otp = str(request.form['otp'])
        # token = str(hashlib.sha256(genToken().encode('utf-8')).hexdigest())
        current_date=getDateOnly()
        token = genToken()
        print(token)
        
        if otp == session['login_otp']:

                data=db.checkAdminLogin(uname,passs,cat_id) 
                
                session.pop('login_otp', None)
                db.resetOTPAttemptswithUname(uname)
                db.tokengen(token,uname)
            
                session['user_data']=data
                
                return jsonify({'status':True,'msg':'Login Successful','data':{ 'user_id': session['user_data']['user_id'],'user_cat_id': session['user_data']['user_cat_id'], 'user_name': session['user_data']['user_name'], 'user_mail': session['user_data']['user_mail'],'user_cat': session['user_data']['user_cat'],'token': session['user_data']['token']}})
        else:
            print("else check")
            data=db.getotpAttemptsWithUname(uname)
            if data and data['otp_atempts']>=5 and data['otp_date']!=current_date:
                db.resetOTPAttemptswithUname(uname)
            if data:
                if data['otp_attempts']>=5 and data['otp_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed OTP Attempts, Please retry after sometime...'})
            db.failedOTP(current_date,uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'})


############### CLIENT LOGIN ###############


# ROUTE FOR LOGIN
@api.route('/client_login',methods=['POST','GET'])
def clientlogin():

    if request.method=='POST':

        # content = request.json
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        cat_id = request.form['cat_id']
        # token = request.form['token']
        current_date=getDateOnly()
        
        data=db.checkClientLogin(uname,passs,cat_id)
       
        # Different date with Correct Password
        if data and data['login_attempts']>=5 and data['login_date']!=current_date:
            db.resetclientPasswordAttemptswithUname(uname)

        if data:
            print(data)
            if data['login_attempts']>=5 and data['login_date']==current_date:
                return jsonify({'status':False,'msg':'Too many Failed Login Attempts, Please retry after sometime...'})
            else:    
                db.resetclientPasswordAttemptswithUname(uname)
            
            # OTP GENERATION
                # otp = str(random.randint(100000,999999))
                otp = onetimepassword()
                print(otp)
                session['login_otp'] = otp
                db.otpadd(otp,uname) 
                
                return jsonify({'status':True,'msg':'Please Enter The OTP'}) 
        else:
            data=db.getclientLoginAttemptsWithUname(uname)
            if data['login_attempts']>=5 and data['login_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed login Attempts, Please retry after sometime...'})
            db.clientfailedLogin(current_date,uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'})


# ROUTE FOR OTP VALIDATION
@api.route('/client_validate_otp',methods=['POST','GET'])
def clientvalidateotp():
    
    if request.method=='POST':
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        cat_id = request.form['cat_id']
        otp = str(request.form['otp'])
        # token = str(hashlib.sha256(genToken().encode('utf-8')).hexdigest())
        current_date=getDateOnly()
        token = genToken()
        print(token)
        
        if otp == session['login_otp']:

                data=db.checkClientLogin(uname,passs,cat_id) 
                
                session.pop('login_otp', None)
                db.resetclientOTPAttemptswithUname(uname)
                db.clienttokengen(token,uname)
            
                session['user_data']=data
                
                return jsonify({'status':True,'msg':'Login Successful','data':{ 'user_id': session['user_data']['client_id'],'ca_id': session['user_data']['ca_id'],'user_cat_id': session['user_data']['user_cat_id'], 'user_name': session['user_data']['user_name'], 'user_mail': session['user_data']['user_mail'],'user_cat': session['user_data']['user_cat'],'token': session['user_data']['token']}})
        else:
            print("else check")
            data=db.getclientotpAttemptsWithUname(uname)
            if data and data['otp_atempts']>=5 and data['otp_date']!=current_date:
                db.resetclientOTPAttemptswithUname(uname)
            if data:
                if data['otp_attempts']>=5 and data['otp_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed OTP Attempts, Please retry after sometime...'})
            db.clientfailedOTP(current_date,uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'})


# LOGOUT ROUTE
@api.route('/logout',methods=['POST','GET'])
def logout():

    if  'user_data' in session:
        session.pop('user_data', None)
        
        umail = request.form['uname']
        db.tokendel(umail)
        db.otpdel(umail)
        
        return jsonify({'status':True,'msg':"Logged out Successfully...."}) 
    else:
        return jsonify({'status':False,'msg':"Already Logged out...."})
    

# CLIENT LOGOUT ROUTE
@api.route('/client_logout',methods=['POST','GET'])
def clientlogout():

    if  'user_data' in session:
        session.pop('user_data', None)
        
        umail = request.form['uname']
        db.clienttokendel(umail)
        db.clientotpdel(umail)
        
        return jsonify({'status':True,'msg':"Logged out Successfully...."}) 
    else:
        return jsonify({'status':False,'msg':"Already Logged out...."})


# CHECK SESSION ROUTE
@api.route('/getsession',methods=['POST','GET'])
def getsession():


    if 'user_data' in session and int(session['user_data']['user_cat_id']) == 501:
    # do something
 
        print(session['user_data'])
        return jsonify({'status':True,'data':{ 'user_id': session['user_data']['client_id'],'ca_id': session['user_data']['ca_id'],'user_cat_id': session['user_data']['user_cat_id'], 'user_name': session['user_data']['user_name'], 'user_mail': session['user_data']['user_mail'],'user_cat': session['user_data']['user_cat'],'token': session['user_data']['token']}})

    elif 'user_data' in session: 
        print(session['user_data'])
        return jsonify({'status':True,'data':{ 'user_id': session['user_data']['user_id'],'user_cat_id': session['user_data']['user_cat_id'], 'user_name': session['user_data']['user_name'], 'user_mail': session['user_data']['user_mail'],'user_cat': session['user_data']['user_cat'],'token': session['user_data']['token']}})
    else:
        return jsonify({'status':False})
    
        

############### USERS ###############


# ADD USER
@api.route('/user_add',methods = ['GET','POST'])
def adduser():
    
    # if request.method == 'POST'  and 'user_data' in session and session['user_data']['admin_role']==1:
       
        uname = request.form['uname']
        ucatid = request.form['ucatid']
        ucat = request.form['ucat']
        umail = request.form['umail']
        umobile = request.form['umobile']      
        upass = str(hashlib.md5(request.form['upass'].encode('UTF-8')).hexdigest())
        uotp = 0
        uotpdate = getDateOnly()
        uregdate = getDateOnly()
        availability = 1
        uregdate = getDateOnly()
        useraddedby = request.form['useraddedby']
        ulogindate = getDateOnly()
        ucatid1 = 401
        ucatid2 = 601
        ucatid3 = 701
        
        data = db.checkMobileandEmail(umail,umobile)

        data1 = db.selectcsttocheckavaliability(ucatid,useraddedby)
        print(data1)
        data2 = db.selectallcstcount(ucatid1,ucatid2,ucatid3,useraddedby)
        print(data2)
        

        if data2 :
            if data2['count'] == 15  :
                db.updateavaliabilityforall(useraddedby)
                return jsonify({'status':True,'msg':'Maximum Limit Reached hello'})
        
        if data1:
            if data1['count'] >= 5:
                # db.updateavaliabilityforall(useraddedby)
                return jsonify({'status':True,'msg':'Maximum Limit Reached'})
        
        if data:
            if (data['user_mail'] ==umail):
                return jsonify({"status":False,"msg":"email_id already exits"})
            elif (data['user_mobile']==umobile):
                return jsonify({"status":False,"msg":"mobile number already exits"})
        else:
            db.useradd(uname,ucatid,ucat,umail,umobile,upass,uotp,uotpdate,uregdate,request.form['ustatus'],availability,useraddedby,ulogindate)        
        return jsonify({'status':True,'msg':'successfully Added'})


# select details from taging 
@api.route('/select_client', methods = ['GET', 'POST'])
def selectclient():

    ucatid = request.form['ucatid']
    uaddedby = request.form['uaddedby']
    userid1 = request.form['userid1']
    userid2 = request.form['userid2']
    userid3 = request.form['userid3']

    data=db.selectclient(ucatid,uaddedby,userid1,userid2,userid3)
    return jsonify({'status': True, 'data':data,'msg' : 'Details Fetched Successfully'})


# SELECT ALL USERS
@api.route('/user_select',methods = ['GET','POST'])
def select():
    
    # if request.method == 'GET' :
        ucatid = request.form['ucatid']
        uaddedby = request.form['uaddedby']
        data = db.select(ucatid,uaddedby)
        print(data)
        
    
        return jsonify ({'status':True,'data':data})


# SELECT ALL USERS
@api.route('/user_select1',methods = ['GET','POST'])
def select1():
    
    # if request.method == 'GET' :
       # ucatid = request.form['ucatid']
        data = db.select1()
        print(data)
   
        return jsonify ({'status':True,'data':data})


# SELECT ALL CLIENTS
@api.route('/client_select',methods = ['GET','POST'])
def clientselect():
    
    # if request.method == 'GET' :
        clientid = request.form['clientid']
        data = db.detailsofclientadded(clientid)
        print(data)
        return jsonify ({'status':True,'data':data})


# SELECT SINGLE CLIENT
@api.route('/client_single',methods = ['GET','POST'])
def clientsingle():
    
    # if request.method == 'GET' :
        clientid = request.form['clientid']
        data = db.clientsingle(clientid)
        print(data)
        return jsonify ({'status':True,'data':data})


# UPDATE CLIENT
@api.route('/client_update',methods = ['GET','POST'])
def clientupdate():
    
    # if request.method == 'GET' :
        uname = request.form['uname']
        umobile = request.form['umobile']
        umail = request.form['umail']
        clientid = request.form['clientid']
        data = db.clientupdate(uname,umobile,umail,clientid)
        print(data)
        return jsonify ({'status':True,'data':data})


# SELECT SINGLE USER
@api.route('/single_user',methods = ['GET','POST'])
def single():
    
    # if request.method == 'POST' and 'user_data' in session and session['user_data']['admin_role']==1:
        uidd = request.form['user_id']
        data = db.single(uidd)
        print(data)
        return jsonify ({'status':True,'data':data})  


# EDIT USER 
@api.route('/edit_user', methods = ['GET','POST'])
def edit():

    # if request.method == 'POST' and 'user_data' in session and session['user_data']['admin_role']==1:
    
        uname = request.form['user_name']
        ucatid = request.form['user_cat_id']
        ucat = request.form['user_cat']
        umail = request.form['user_mail']
        umobile = request.form['user_mobile']
        ustatus = request.form['user_status']
        uid = request.form['user_id']
    
        data=db.checkEmailforUpdate(umail,uid)
        data1=db.checkMobileforUpdate(umobile,uid)

        if data:           
            return jsonify({"status":False,"msg":"email_id already exits"})
        if data1:    
            return jsonify({"status":False,"msg":"mobile number already exits"})

        db.edit(uname,ucatid,ucat,umail,umobile,ustatus,uid)

        return jsonify({'status':True,'msg':'successfully Updated'})


# DELETE USER
@api.route('/delete_user', methods = ['GET', 'POST'])
def deleteuser():

    userid = request.form['userid']
    clientid = request.form['clientid']
    userid1 = request.form['userid1']
    userid2 = request.form['userid2']
    userid3 = request.form['userid3']

    
    db.updateavaliabilitytrue(userid1,userid2,userid3)
    db.deleteclient(clientid)
    db.deleteuser(userid)
    return jsonify({'status': True, 'msg' : 'Deleted Successfully'})


############### GET LAST ID ###############


# GET MAX ID
@api.route('/last_id',methods = ['POST','GET'])
def lastid():
    
    data = db.lastid()
    return jsonify({'data':data})


############### FORGOT PASSWORD ###############


# ROUTE FOR FORGOT PASSWORD
@api.route('/forgot_password',methods=['POST','GET'])
def forgetpass():

    if request.method=='POST':
        # content = request.json
        uname = request.form['uname']
        print(uname)
        data=db.forget(uname)
        if data:
            print(data)
            
            return jsonify({'status':True,'msg':'change password'}) 
        else:
           return jsonify({'status':False,'msg':'Incorrect Credentials...'})
    

# UPDATE PASSWORD
@api.route('/update_password',methods =['POST','GET'])
def forgetpassword():

    maill = request.form['mail']
    passs = str(hashlib.md5(request.form['pas'].encode('UTF-8')).hexdigest())
    # passs = request.form['pas']

    db.forgetpass(passs,maill)
    return jsonify({'status':True,'msg': 'password updated'})


############### GETTING USERID WITH MOBILE NUMBER ################ 


# GETTING DETAILS WITH MOBILE NUMBER
@api.route('/user_mobile',methods = ['GET','POST'])
def user_mobile():
    
    # if request.method == 'GET' :
        
        mobile = request.form['umobile']
        data = db.detailswithmobile(mobile)
        print(data)
        
        return jsonify ({'status':True,'data':data})


############### CUSTOMER SUCCESS TEAM ###############


# NEW ADD CLIENT TABLE
@api.route('/adding_client',methods = ['GET','POST'])
def addingclient():
    
    # if request.method == 'POST'  and 'user_data' in session and session['user_data']['admin_role']==1:
        
        cstid = request.form['cstid']
        cctid = request.form['cctid']
        cctname = request.form['cctname']
        managementid = request.form['managementid']
        managementname = request.form['managementname']
        financeid = request.form['financeid']
        financename = request.form['financename']
        ucatid = request.form['ucatid']
        ucat = request.form['ucat']
        uname = request.form['uname']
        doctor = request.form['doctor']
        nurse = request.form['nurse']
        compounder = request.form['compounder']
        umobile = request.form['umobile']
        umail = request.form['umail']
        upass = str(hashlib.md5(request.form['upass'].encode('UTF-8')).hexdigest())
        uregdate = getDateOnly()
        ustatus = 1

        data = db.checkMobileandEmail(umail,umobile)

        data1 = db.selectallclientcstcount(cstid)
        print(data1)

        if data1:
            if data1['count'] == 4:
                db.updateavaliabilityforall(cstid)
                return jsonify({'status':True,'msg':'Maximum Limit Reached hello'})

        if cctid == "" and cctname == "":
            return jsonify ({'Status':False,'msg':'cct team should be assigned'})    
        elif managementid == "" and managementname == "":
            return jsonify ({'Status':False,'msg':'management team should be assigned'})
        elif financeid == "" and financename == "":
            return jsonify ({'Status':False,'msg':'finanace team should be assigned'})
        
        if data:
            if (data['user_mail'] ==umail):
                return jsonify({"status":False,"msg":"email_id already exits"})
            elif (data['user_mobile']==umobile):
                return jsonify({"status":False,"msg":"mobile number already exits"})
        
        else:
            db.addclient(cstid,cctid,cctname,managementid,managementname,financeid,financename,ucatid,ucat,uname,doctor,nurse,compounder,umobile,umail,upass,uregdate,ustatus)
            db.updateavaliabilityfalse(cctid,managementid,financeid)
            data12 = db.lastid()
        return jsonify({'status':True,'data':data12,'msg':'successfully Added'})


# UPDATE CA_ID
@api.route('/update_caid',methods = ['POST','GET'])
def updatecaid():

    caid = request.form['caid']
    clientid = request.form['clientid']

    if caid and clientid:
        if caid != "" and clientid != "":
            db.updatecaid(caid,clientid)
        return jsonify({'status':True,'msg':'ca id updated'})
    else:
        return jsonify({'status':False,'msg':'please check the data'})


# UPDATE CST AVALIABILITY FASLE IN USERTABLE TABLE
@api.route('/update_cst_avaliability_usertable',methods = ['GET','POST'])
def updatecstavaliabilityusertable():
    
    # if request.method == 'GET' :
        
        cstid = request.form['cstid']
        
        data1 = db.selectallclientcstcount(cstid)
        print(data1)

        if data1:
            if data1['count'] < 5 :
                db.updatecstavaliability(cstid)
                return jsonify({'status':True,'msg':'cst avaliability changed'})

        if data1:
            if data1['count'] == 5:
                db.updateavaliabilityforall(cstid)
                return jsonify({'status':True,'msg':'Maximum Limit Reached try another cst'})
        
        else :
            return jsonify ({'status':True,'msg':'please check again'})


# GETTING DETAILS WITH MOBILE NUMBER
@api.route('/select_new_client',methods = ['GET','POST'])
def selectnewclient():
    
    # if request.method == 'GET' :
        
        cstid = request.form['cstid']
        
        data = db.selectnewclient(cstid)
        print(data)
        return jsonify ({'status':True,'data':data})


# DELETE CLIENT
@api.route('/delete_client', methods = ['GET', 'POST'])
def deleteclient():

    clientid = request.form['clientid']
    data = db.selectdeleteclientdetails(clientid)
    print(data)
    db.deleteclient(clientid)
    return jsonify({'status': True, 'data':data,'msg' : 'Deleted Successfully'})

# UPDATE AVALIABILITY
@api.route('/update_avaliability', methods = ['GET', 'POST'])
def updateavaliability():

    cctid = request.form['cctid']
    managementid = request.form['managementid']
    financeid = request.form['financeid']
    cstid = request.form['cstid']

    data1 = db.selectallclientcstcount(cstid)
    print(data1)

    data = db.updateavaliabilitytrue(cctid, managementid, financeid)
    
    if data1:
            if data1['count'] <= 5 :
                db.updatecstavaliability(cstid)
                return jsonify({'status':True,'msg':'cst avaliability changed'})
            
    else:
        return jsonify({'status': True, 'data':data,'msg' : 'nothing to show'})

        


# SELECT CCT
@api.route('/select_cct',methods = ['GET','POST'])
def selectcct():

    cctid = request.form['cctid']

    data = db.selectcctclientdatatodelete(cctid)
    print(data)
    
    return jsonify({'status': True,'data':data,'msg' : 'data fetched successfully'})

  
# SELECT MANAGEMENT
@api.route('/select_management',methods = ['GET','POST'])
def selectmanagement():

    managementid = request.form['managementid']

    data = db.selectmanagementclientdatatodelete(managementid)
    print(data)

    return jsonify({'status': True,'data':data,'msg' : 'data fetched successfully'})


# SELECT FINANCE
@api.route('/select_finance',methods = ['GET','POST'])
def selectfinance():

    financeid = request.form['financeid']

    data = db.selectfinanceclientdatatodelete(financeid)
    print(data)

    return jsonify({'status': True,'data':data,'msg' : 'data fetched successfully'})
   

# SELECT SINGLE CLIENT
@api.route('/select_single_client',methods = ['GET','POST'])
def selectsingleclient():

    clientid = request.form['clientid']
    data = db.selectsingleclientdatatoupdate(clientid)
    print(data)

    return jsonify({'status':True,'data':data,'msg':'data fetched successfully'})


# UPDATE SINGLE CCT CLIENT
@api.route('/update_single_cctclient',methods = ['GET','POST'])
def updatesinglecctclient():

    cctid = request.form['cctid']
    cctname = request.form['cctname']
    clientid = request.form['clientid']
    useridold = request.form['useridold']
    useridnew = request.form['useridnew']
    data = db.updatesinglecctclient(cctid,cctname,clientid)
    db.updateoldcctavaliability(useridold)
    db.updatenewcctavaliability(useridnew)
    db.updatecmf1(useridold)
    print(data)

    return jsonify({'status':True,'data':data,'msg':'data fetched successfully'})


# UPDATE SINGLE MANAGEMENT CLIENT
@api.route('/update_single_managementclient',methods = ['GET','POST'])
def updatesinglemanagementclient():

    managementid = request.form['managementid']
    managementname = request.form['managementname']
    clientid = request.form['clientid']
    useridold = request.form['useridold']
    useridnew = request.form['useridnew']
    data = db.updatesinglemanagementclient(managementid,managementname,clientid)
    db.updateoldcctavaliability(useridold)
    db.updatenewcctavaliability(useridnew)
    db.updatecmf1(useridold)
    print(data)

    return jsonify({'status':True,'data':data,'msg':'data fetched successfully'})


# UPDATE SINGLE FINANCE CLIENT
@api.route('/update_single_financeclient',methods = ['GET','POST'])
def updatesinglefinanceclient():

    financeid = request.form['financeid']
    financename = request.form['financename']
    clientid = request.form['clientid']
    useridold = request.form['useridold']
    useridnew = request.form['useridnew']
    data = db.updatesinglefinanceclient(financeid,financename,clientid)
    db.updateoldcctavaliability(useridold)
    db.updatenewcctavaliability(useridnew)
    db.updatecmf1(useridold)
    print(data)

    return jsonify({'status':True,'data':data,'msg':'data fetched successfully'})   


# DELETE CCT
@api.route('/delete_cct',methods = ['GET','POST'])
def deletecct():

    userid = request.form['userid']

    data = db.checkcmfavaliabilitytodelete(userid)
    print(data)

    if data:
        if data['availability'] == 0:
            return jsonify ({'status': False,'data':data,'msg' : 'cct has a client assigned.Assign that cient to other cct '})
        else:
            db.updatecmf(userid)
            return jsonify({'status': True,'msg' : 'Deleted Successfully'})
    else :
        return jsonify({'msg':'Unable to Delete'})


# DELETE MANAGEMENT
@api.route('/delete_management',methods = ['GET','POST'])
def deletemanagement():

    userid = request.form['userid']
    
    data = db.checkcmfavaliabilitytodelete(userid)
    print(data)

    if data:
        if data['availability'] == 0:
            return jsonify ({'status': False,'data':data,'msg' : 'management has a client assigned.Assign that cient to other management '})
        else:
            db.updatecmf(userid)
            return jsonify({'status': True,'msg' : 'Deleted Successfully'})
    else :
        return jsonify({'msg':'Unable to Delete'})


# DELETE FINANCE
@api.route('/delete_finance',methods = ['GET','POST'])
def deletefinanace():

    userid = request.form['userid']

    data = db.checkcmfavaliabilitytodelete(userid)
    print(data)

    if data:
        if data['availability'] == 0:
            return jsonify ({'status': False,'data':data,'msg' : 'finance has a client assigned.Assign that cient to other finance '})
        else:
            db.updatecmf(userid)
            return jsonify({'status': True,'msg' : 'Deleted Successfully'})
    else:
        return jsonify({'msg':'Unable to Delete'})


############### ADMIN ###############


# GETTING CCT TEAM DETAILS WRT TO CLIENT
@api.route('/select_noofcst_addedby_admin',methods = ['GET','POST'])
def selectnocstaddedbyadmin():

    user1 = request.form['useradded1']
    user2 = request.form['useradded2']

    cst_data = db.selectnoofcstaddedbyadmin(user1,user2)
    return jsonify({'status':True,'data': cst_data,'msg':'data fetched successfully'})   


# SELECT CCT/MANAGEMENT/FINANCE ADDED BY THE ADMINS CST TEAM
@api.route('/select_cctmf_cst_adddedbyadmin',methods = ['GET','POST'])
def selectcctmfcstadddedbyadmin():

    cst_team = request.form['cst_team']
    ucatid = request.form['ucatid']

    data = db.selectcatdatawrtclient(cst_team,ucatid)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'}) 


#SELECT CLIENT WRT ADMIN
@api.route('/select_client_cst_adddedbyadmin',methods = ['GET','POST'])
def selectclientcstadddedbyadmin():

    cst_team = request.form['cst_team']
    # ucatid = request.form['ucatid']

    data = db.selectclientwrtadmin(cst_team)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# SELECT INACTIVE USERS 
@api.route('/select_inactive_users',methods = ['GET','POST'])
def selectactiveorinactiveusers():

    # ucatid = request.form['ucatid']
    ustatus = 0
    # ucatid = request.form['ucatid']

    data = db.selectinactiveusers(ustatus)

    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# UPDATE STATUS TO ACTIVE 


############### SUPER ADMIN ###############


# SELECT ADMIN WRT SUPER ADMIN

@api.route('/select_adminadded_wrt_superadmins',methods = ['GET','POST'])
def selectadminswrtsuperadmins():

    useradded1 = request.form['useradded1']
    useradded2 = request.form['useradded2']

    data = db.selectnoofcstaddedbysuperadmin(useradded1,useradded2)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# SELECT ADMIN WRT SUPER ADMIN
@api.route('/select_admindata_wrt_superadmins',methods = ['GET','POST'])
def selectadmindatawrtsuperadmins():

    admin_team = request.form['admin_team']
    ucatid = request.form['ucatid']

    data = db.selectadmindatawrtsuperadmin(admin_team,ucatid)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# SELECT  CCT/MANAGEMENT/FINANACE WRT SUPER ADMIN
@api.route('/select_cctmf_wrt_superadmin',methods = ['GET','POST'])
def selectcctmfwrtsuperadmin():

    ucatid = request.form['ucatid']
    print(request.form)

    data = db.selectcctmfwrtsuperadmin(ucatid)
    print(data)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# SELECT  CLIENT WRT SUPER ADMIN
@api.route('/select_client_wrt_superadmin',methods = ['GET','POST'])
def selectclientwrtsuperadmin():

    ucatid = request.form['ucatid']

    data = db.selectclientwrtsuperadmin(ucatid)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


############## INACTIVATE CST ###############


# SELECT  CLIENT DETAILS TO DEACTIVATE CST
@api.route('/select_client_to_deactivate_cst',methods = ['GET','POST'])
def selectclienttodeactivatecst():

    cstid = request.form['cstid']
    userid = request.form['userid']
    print(request.form)
    data = db.selectusertabletochangecst(userid)
    data12=db.selectclienttochangecst(cstid)
    print(data12)
    print("===============================================")
    data13 = db.selectcst()
    print(data13)

    if data and data12 and data13:
        for data1 in data12:
            for data2 in data13:
                if data['availability'] == 1 and data1['cst_id'] != int(cstid) and data2['user_added_by'] != cstid:
                    db.updateuserstatus(userid)
                    return jsonify({'status':True,'msg':'cst deactivated'})
                else :
                    data11=db.selectclientusertabletochangecst(cstid)
                    return jsonify({'status':False,'data': data11,'msg':'data fetched successfully'})
    else:
        db.updateuserstatus(userid)
        return jsonify({'status':True,'msg':'hello'})



# UPDATE USER ADDEB BY IN  USERTABLE
@api.route('/update_useraddedby_usertable',methods = ['GET','POST'])
def updateuseraddedbyusertable():

    uaddedby = request.form['uaddedby'] #new cst id
    userid = request.form['userid'] # existing cst id
    userid1 = request.form['userid1'] #cct id
    userid2 = request.form['userid2'] # finance id
    userid3 = request.form['userid3'] # management id
    cstid = request.form['cstid'] #new cst id
    clientid = request.form['clientid'] # client id

    db.updateuseraddedby(uaddedby,userid1,userid2,userid3)
    # db.updateuseraddedbyforcstdeactivate(uaddedby,userid)
    db.updateclientcst(cstid,clientid)

    data12=db.selectclienttochangecst(userid)
    data13 = db.selectcst()

    if data12 and data13:
        for data1 in data12:
            for data2 in data13:
                if data1['cst_id'] != int(userid) and data2['user_added_by'] != userid:
                    db.updateuserstatus(userid)
                    return jsonify({'status':True,'msg':'cst deactivated'})
    else:
        # db.updateuserstatus(userid)
        return jsonify({'status':True,'msg':'hello'})
    

# SELECT  CLIENT WRT SUPER ADMIN
@api.route('/update_useraddedby_to_deactivate_cst',methods = ['GET','POST'])
def update_useraddedby_to_deactivate_cst():

    uaddedby = request.form['uaddedby']
    userid = request.form['userid']

    data = db.updateuseraddedbyforcstdeactivate(uaddedby,userid)
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


############### DEACTIVATE ADMIN WRT TO SUPER ADMIN ###############


# SELECT  CST DETAILS TO DEACTIVATE ADMIN
@api.route('/select_cst_to_deactivate_admin',methods = ['GET','POST'])
def selectcsttodeactivateadmin():

    userid = request.form['userid']

    data = db.selectusertabletochangecst(userid)
    print(data)
    data1 = db.selectcstuseraddedbytodeactivate()
    print(data1)
    
    if data and data1:
        if data['availability'] == 1 and all(data12['user_added_by'] != userid for data12 in data1):
            db.updateuserstatus(userid)
            return jsonify({'status': True, 'msg': 'admin deactivated'})
        else:
            data1 = db.selectusertabletochangecstaddedby(userid)
            return jsonify({'status': False, 'data': data1, 'msg': 'data fetched successfully'})
    else:
        db.updateuserstatus(userid)
        return jsonify({'status': True, 'msg': 'hello'})

    

# UPDATE SINGLE USERADDEDBY 
@api.route('/select_single_cst_useraddedby',methods = ['GET','POST'])
def selectsinglecstuseraddedby():

    userid = request.form['userid']

    data = db.selectsinglecsttochangecstaddedby(userid)
    
    return jsonify({'status':True,'data': data,'msg':'data fetched successfully'})


# SELECT  CST DETAILS TO DEACTIVATE ADMIN
@api.route('/update_cst_addedby',methods = ['GET','POST'])
def update_cst_addedby():

    userid = request.form['userid']
    uaddedby = request.form['uaddedby']

    db.updateuseraddedbyforcstdeactivate(uaddedby,userid)
    return jsonify({'status': True, 'msg': 'single addedby updated'})


############### FINANACE ###############


# SELECT  FINANCE TAGGED CLIENT FROM CLIENT TABLE
@api.route('/select_finance_client',methods = ['GET','POST'])
def selectfinanceclient():

    financeid = request.form['financeid']

    data = db.selectfinancetaggedclient(financeid)
    return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


############### MANAGEMENT ###############


# SELECT  MANAGEMENT TAGGED CLIENT FROM CLIENT TABLE
@api.route('/select_management_client',methods = ['GET','POST'])
def selectmanagementclient():

    managementid = request.form['managementid']

    data = db.selectmanagementtaggedclient(managementid)
    return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


############### CCT ###############


# SELECT  CCT TAGGED CLIENT FROM CLIENT TABLE
@api.route('/select_cct_client',methods = ['GET','POST'])
def selectcctclient():

    cctid = request.form['cctid']

    data = db.selectcctaggedclient(cctid)
    return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


############### SUB FINANCE  ###############


# INSERT INTO SUB FINANCE TABLE
@api.route('/add_sub_finance',methods = ['GET','POST'])
def insertsubfinanace():

    financeid = request.form['financeid']
    financename = request.form['financename']
    subcatid = request.form['subcatid']
    subcat = request.form['subcat']
    subname = request.form['subname']
    umobile = request.form['submobile']
    umail = request.form['submail']
    subpass = str(hashlib.md5(request.form['subpass'].encode('UTF-8')).hexdigest())
    userregdate = getDateOnly()
    userstatus = 1

    data = db.checkMobileandEmail(umail,umobile)
    data1 = db.checkMobileandEmailinsubfinanace(umail,umobile)

    if data and data1:
            if data['user_mail'] ==umail and data1['user_sub_mail'] ==umail:
                return jsonify({"status":False,"msg":"email_id already exits"})
            elif data['user_mobile'] ==umobile and data1['user_sub_mobile']  ==umobile:
                return jsonify({"status":False,"msg":"mobile number already exits"})
        
    else:
        data = db.addsubfinance(financeid,financename,subcatid,subcat,subname,umobile,umail,subpass,userregdate,userstatus)
        return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


# SELECT ALL FROM SUB FINANACE
@api.route('/select_sub_finance',methods = ['GET','POST'])
def selectsubfinanace():

    usubcatid = request.form['usubcatid']
    financeid = request.form['financeid']

    data = db.selectallsubfinance(usubcatid,financeid)
    return jsonify({'status':True, 'data':data, 'msg':'sub finance details fetched successfully'})


# SELECT ONE FROM SUB FINANACE TO UPDATE
@api.route('/select_single_sub_finance',methods = ['GET','POST'])
def selectsinglesubfinance():

    userid = request.form['userid']

    data = db.selectonesubfinancetoupdate(userid)
    return jsonify({'status':True, 'data':data, 'msg':'sub finance details fetched successfully'})


# UPDATE SUB FINANACE 
@api.route('/update_single_sub_finance',methods = ['GET','POST'])
def updatesinglesubfinance():

    subname = request.form['subname']
    submobile = request.form['submobile']
    submail = request.form['submail']
    userid = request.form['userid']

    db.updatesubfinance(subname,submobile,submail,userid)
    return jsonify({'status':True, 'msg':'sub finance details fetched successfully'})


# DEACTIVATE SUB FINANACE
@api.route('/deactivate_single_sub_finance',methods = ['GET','POST'])
def deactivatesinglesubfinance():

    userid = request.form['userid']

    db.deactivatesubfinance(userid)
    return jsonify({'status':True, 'msg':'sub finance deactivated'})


############### SUB MANAGEMENT  ###############

# INSERT INTO SUB MANAGEMENT TABLE
@api.route('/add_sub_management',methods = ['GET','POST'])
def insertsubmanagement():

    managementid = request.form['managementid']
    managementname = request.form['managementname']
    subcatid = request.form['subcatid']
    subcat = request.form['subcat']
    subname = request.form['subname']
    umobile = request.form['submobile']
    umail = request.form['submail']
    subpass = str(hashlib.md5(request.form['subpass'].encode('UTF-8')).hexdigest())
    userregdate = getDateOnly()
    userstatus = 1

    data = db.checkMobileandEmail(umail,umobile)
    data1 = db.checkMobileandEmailinmanagement(umail,umobile)

    if data and data1:
            if data['user_mail'] ==umail and data1['user_sub_mail'] ==umail:
                return jsonify({"status":False,"msg":"email_id already exits"})
            elif data['user_mobile'] ==umobile and data1['user_sub_mobile']  ==umobile:
                return jsonify({"status":False,"msg":"mobile number already exits"})
        
    else:
        data = db.addsubmanagement(managementid,managementname,subcatid,subcat,subname,umobile,umail,subpass,userregdate,userstatus)
        return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


# SELECT ALL FROM SUB MANAGEMENT
@api.route('/select_sub_management',methods = ['GET','POST'])
def selectsubmanagement():

    usubcatid = request.form['usubcatid']
    managementid = request.form['managementid']

    data = db.selectallsubmanagement(usubcatid,managementid)
    return jsonify({'status':True, 'data':data, 'msg':'sub management details fetched successfully'})


# SELECT ONE FROM SUB MANAGEMENT TO UPDATE
@api.route('/select_single_sub_management',methods = ['GET','POST'])
def selectsinglesubmanagement():

    userid = request.form['userid']

    data = db.selectonesubmanagementtoupdate(userid)
    return jsonify({'status':True, 'data':data, 'msg':'sub management details fetched successfully'})


# UPDATE SUB MANAGEMENT
@api.route('/update_single_sub_management',methods = ['GET','POST'])
def updatesinglesubmanagement():

    subname = request.form['subname']
    submobile = request.form['submobile']
    submail = request.form['submail']
    userid = request.form['userid']

    db.updatesubmanagement(subname,submobile,submail,userid)
    return jsonify({'status':True, 'msg':'sub management details fetched successfully'})


# DEACTIVATE SUB MANAGEMENT
@api.route('/deactivate_single_sub_management',methods = ['GET','POST'])
def deactivatesinglesubmanagement():

    userid = request.form['userid']

    db.deactivatesubmanagement(userid)
    return jsonify({'status':True, 'msg':'sub management deactivated'})


############### SUB CCT  ###############


# INSERT INTO SUB CCT TABLE
@api.route('/add_sub_cct',methods = ['GET','POST'])
def insertsubcct():

    cctid = request.form['cctid']
    cctname = request.form['cctname']
    subcatid = request.form['subcatid']
    subcat = request.form['subcat']
    subname = request.form['subname']
    umobile = request.form['submobile']
    umail = request.form['submail']
    subpass = str(hashlib.md5(request.form['subpass'].encode('UTF-8')).hexdigest())
    userregdate = getDateOnly()
    userstatus = 1

    data = db.checkMobileandEmail(umail,umobile)
    data1 = db.checkMobileandEmailinsubcct(umail,umobile)

    if data and data1:
            if data['user_mail'] ==umail and data1['user_sub_mail'] ==umail:
                return jsonify({"status":False,"msg":"email_id already exits"})
            elif data['user_mobile'] ==umobile and data1['user_sub_mobile']  ==umobile:
                return jsonify({"status":False,"msg":"mobile number already exits"})
    else:
        data = db.addsubcct(cctid,cctname,subcatid,subcat,subname,umobile,umail,subpass,userregdate,userstatus)
        return jsonify({'status':True, 'data':data, 'msg':'client details fetched successfully'})


# SELECT ALL FROM SUB CCT
@api.route('/select_sub_cct',methods = ['GET','POST'])
def selectsubcct():

    usubcatid = request.form['usubcatid']
    cctid = request.form['cctid']

    data = db.selectallsubcct(usubcatid,cctid)
    return jsonify({'status':True, 'data':data, 'msg':'sub cct details fetched successfully'})


# SELECT ONE FROM SUB CCT TO UPDATE
@api.route('/select_single_sub_cct',methods = ['GET','POST'])
def selectsinglesubcct():

    userid = request.form['userid']

    data = db.selectonesubccttoupdate(userid)
    return jsonify({'status':True, 'data':data, 'msg':'sub cct details fetched successfully'})


# UPDATE SUB CCT 
@api.route('/update_single_sub_cct',methods = ['GET','POST'])
def updatesinglesubcct():

    subname = request.form['subname']
    submobile = request.form['submobile']
    submail = request.form['submail']
    userid = request.form['userid']

    db.updatesubcct(subname,submobile,submail,userid)
    return jsonify({'status':True, 'msg':'sub cct details fetched successfully'})


# DEACTIVATE SUB CCT
@api.route('/deactivate_single_sub_cct',methods = ['GET','POST'])
def deactivatesinglesubcct():

    userid = request.form['userid']

    db.deactivatesubcct(userid)
    return jsonify({'status':True, 'msg':'sub cct deactivated'})


############### SERVICE TEAM  ###############


# DEACTIVATE SERVICE TEAM
@api.route('/deactivate_service_team',methods = ['GET','POST'])
def deactivateserviceteam():

    userid = request.form['userid']

    db.updatecmf(userid)
    return jsonify({'status':True, 'msg':'sub cct deactivated'})

# DEACTIVATE SERVICE TEAM
@api.route('/add_employee',methods = ['GET','POST'])
def addemployee():

    name = request.form['name']
    age = request.form['age']
    occupation = request.form['occupation']

    db.addemployee(name,age,occupation)
    return jsonify({'status':True, 'msg':'sub cct deactivated'})


############## SHOW DOCTOR NURSE AND COMPOUNDER ################


#DOCTORS
@api.route('/select_clinic_details',methods = ['GET','POST'])
def selectdoctor():

    clientid = request.form['clientid']

    data = db.selectclinicdetails(clientid)
    print(data)
    return jsonify({'status':True,'data':data,'msg':'client details fetched'})


#NURSE
@api.route('/select_nurse',methods = ['GET','POST'])
def selectnurse():

    clientid = request.form['clientid']

    data = db.selectclinicdetails(clientid)
    return jsonify({'status':True,'data':data,'msg':'sub cct deactivated'})


#COMPOUNDER
@api.route('/select_compounder',methods = ['GET','POST'])
def selectcompounder():

    clientid = request.form['clientid']

    data = db.selectallcompounders(clientid)
    return jsonify({'status':True,'data':data,'msg':'sub cct deactivated'})


