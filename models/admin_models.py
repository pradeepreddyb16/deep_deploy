from extensions import mysql
import json


class Models:


    # GET ADMIN LOGIN DETAILS
    def checkAdminLogin(uname,passs,cat_id):
        cur=mysql.connection.cursor()

        # sql="SELECT `admin_id`,`admin_name`,`cat_id`,`admin_pass`,`user_mail`,`user_mobile`,`login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` , `admin_role`,`token`  FROM `user_table`  WHERE ( `user_mail` = %s or `user_mobile`=%s ) and admin_pass=%s and cat_id = %s and `admin_status`=1"

        sql = "SELECT `user_id`,`user_name`, `user_cat_id`,`user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`, date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date`, `otp_attempts`, `user_reg_date`, `user_status`, `login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date, `token` FROM `user_table`  WHERE `user_mail` = %s and user_pass=%s and user_cat_id = %s and `user_status`=1"

        cur.execute(sql,[uname,passs,cat_id])
        print(sql)
        data=cur.fetchone()
        cur.close() 
        return data
    

# GET CLIENT LOGIN DETAILS
    def checkClientLogin(uname,passs,cat_id):
        cur=mysql.connection.cursor()

        # sql="SELECT `admin_id`,`admin_name`,`cat_id`,`admin_pass`,`user_mail`,`user_mobile`,`login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` , `admin_role`,`token`  FROM `user_table`  WHERE ( `user_mail` = %s or `user_mobile`=%s ) and admin_pass=%s and cat_id = %s and `admin_status`=1"

        sql = "SELECT `client_id`, `ca_id`,`cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, `user_reg_date`, `login_attempts`, `login_date`, `user_status`, `electrodes_count`, `device_count`, `device_name`, `token` FROM `client` WHERE `user_mail` = %s and user_pass=%s and user_cat_id = %s and `user_status`=1"

        cur.execute(sql,[uname,passs,cat_id])
        print(sql)
        data=cur.fetchone()
        cur.close() 
        return data
    

# ADMIN LOGIN ATTEMPTS WITH UNAME
    def getLoginAttemptsWithUname(uname):
        cur=mysql.connection.cursor()
        
        sql="SELECT `login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` FROM `user_table` WHERE ( `user_mail` = %s or `user_mobile`=%s )  and `user_status`=1"

        cur.execute(sql,[uname,uname])
        data=cur.fetchone()
        cur.close() 
        return data
    

# CLIENT LOGIN ATTEMPTS WITH UNAME
    def getclientLoginAttemptsWithUname(uname):
        cur=mysql.connection.cursor()
        
        sql="SELECT `login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` FROM `client` WHERE ( `user_mail` = %s or `user_mobile`=%s )  and `user_status`=1"

        cur.execute(sql,[uname,uname])
        data=cur.fetchone()
        cur.close() 
        return data


    # TOKEN GENERATION ON LOGIN
    def tokengen(token,uname):
        cur = mysql.connection.cursor()

        sql = "UPDATE `user_table` SET `token`= %s WHERE `user_mail` = %s"

        data = cur.execute(sql,[token,uname])
        mysql.connection.commit()
        cur.close
        return data
    

    # TOKEN GENERATION ON LOGIN
    def clienttokengen(token,uname):
        cur = mysql.connection.cursor()

        sql = "UPDATE `client` SET `token`= %s WHERE `user_mail` = %s"

        data = cur.execute(sql,[token,uname])
        mysql.connection.commit()
        cur.close
        return data


    # TOKEN DELETE ON LOGOUT
    def tokendel(uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `token`='' WHERE `user_mail`=%s or `user_mobile`=%s "
        data = cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close
        return data
    

    # CLIENT TOKEN DELETE ON LOGOUT
    def clienttokendel(uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `token`='' WHERE `user_mail`=%s or `user_mobile`=%s "
        data = cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close
        return data
                  
                  

    # OTP ADD
    def otpadd(otp,uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_otp`= %s WHERE `user_mail`=%s or `user_mobile`=%s "
        data = cur.execute(sql,[otp,uname,uname])
        mysql.connection.commit()
        cur.close
        

    # OTP DELETE
    def otpdel(uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_otp`= '0' WHERE `user_mail`=%s or `user_mobile`=%s"
        data = cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close
        return data


    # CLIENT OTP DELETE
    def clientotpdel(uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `user_otp`= '0' WHERE `user_mail`=%s or `user_mobile`=%s"
        data = cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close
        return data

    # ADMIN UPDATE LOGIN FAILED ATTEMPTS
    def failedLogin(datee,uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `user_table` SET  `login_attempts`=`login_attempts`+1,`login_date`=%s WHERE `user_mail`=%s or `user_mobile`=%s "

        cur.execute(sql,[datee,uname,uname])
        
        mysql.connection.commit()
        cur.close()


# CLIENT UPDATE LOGIN FAILED ATTEMPTS
    def clientfailedLogin(datee,uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `client` SET  `login_attempts`=`login_attempts`+1,`login_date`=%s WHERE `user_mail`=%s or `user_mobile`=%s "

        cur.execute(sql,[datee,uname,uname])
        
        mysql.connection.commit()
        cur.close()


    
     # ADMIN UPDATE LOGIN FAILED ATTEMPTS
    def addcheckaval(userid1,userid2,userid3):
        cur=mysql.connection.cursor()
        sql="UPDATE `user_table` SET  `check_aval`=`check_aval`+1,`login_date`=%s WHERE `user_id` in (%s,%s,%s) "

        cur.execute(sql,[userid1,userid2,userid3])
        
        mysql.connection.commit()
        cur.close()

        
    # ADMIN PASSWORD ATTEMPTS RESET
    def resetPasswordAttemptswithUname(uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `user_table` SET  `login_attempts`=0 WHERE  `user_mail`=%s or `user_mobile`=%s"
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close() 


# ADMIN PASSWORD ATTEMPTS RESET
    def resetclientPasswordAttemptswithUname(uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `client` SET  `login_attempts`=0 WHERE  `user_mail`=%s or `user_mobile`=%s"
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close() 
 
    
    # ADMIN OTP ATTEMPS WITH UNAME
    def getotpAttemptsWithUname(uname):
        cur=mysql.connection.cursor()
        sql="SELECT `login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` FROM `user_table` WHERE ( `user_mail` = %s or `user_mobile`=%s )  and `user_status`= 1"
        cur.execute(sql,[uname,uname])
        data=cur.fetchone()
        cur.close() 
        return data
    

        # CLIENT OTP ATTEMPS WITH UNAME
    def getclientotpAttemptsWithUname(uname):
        cur=mysql.connection.cursor()
        sql="SELECT `login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` FROM `client` WHERE ( `user_mail` = %s or `user_mobile`=%s )  and `user_status`= 1"
        cur.execute(sql,[uname,uname])
        data=cur.fetchone()
        cur.close() 
        return data


    # ADMIN OTP ATTEMPTS RESET
    def resetOTPAttemptswithUname(uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `user_table` SET  `otp_attempts`=0 WHERE  `user_mail`=%s or `user_mobile`=%s "
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close() 


    # ADMIN OTP ATTEMPTS RESET
    def resetclientOTPAttemptswithUname(uname):
        cur=mysql.connection.cursor()
        sql="UPDATE `client` SET  `otp_attempts`=0 WHERE  `user_mail`=%s or `user_mobile`=%s "
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close()

    # ADMIN UPDATE FAILED OTP ATTEMPTS
    def failedOTP(datee,username):
        cur=mysql.connection.cursor()
        sql="UPDATE `user_table` SET  `otp_attempts`=`otp_attempts`+1,`otp_date`=%s WHERE `user_mail`=%s or `user_mobile`=%s "
        cur.execute(sql,[datee,username,username])
        mysql.connection.commit()
        cur.close()


    # CLIENT UPDATE FAILED OTP ATTEMPTS
    def clientfailedOTP(datee,username):
        cur=mysql.connection.cursor()
        sql="UPDATE `client` SET  `otp_attempts`=`otp_attempts`+1,`otp_date`=%s WHERE `user_mail`=%s or `user_mobile`=%s "
        cur.execute(sql,[datee,username,username])
        mysql.connection.commit()
        cur.close()


    # ADD ADMIN DETAILS
    def useradd(uname,ucatid,ucat,umail,umobile,upass,uotp,uotpdate,uregdate,ustatus,availability,useraddedby,ulogindate):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `user_table`( `user_name`, `user_cat_id`, `user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`, `otp_date`, `user_reg_date`, `user_status`,`availability`, `user_added_by`,`login_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sql,[uname,ucatid,ucat,umail,umobile,upass,uotp,uotpdate,uregdate,ustatus,availability,useraddedby,ulogindate])
        mysql.connection.commit()
        cur.close()


    # ADD ADMIN DETAILS
    def addclient(cstid,cctid,cctname,managementid,managementname,financeid,financename,ucatid,ucat,uname,doctor,nurse,compounder,umobile,umail,upass,uregdate,ustatus):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `client`(`cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`,`doctor`,`nurse`,`compounder`, `user_mobile`, `user_mail`, `user_pass`, `user_reg_date`, `user_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sql,[cstid,cctid,cctname,managementid,managementname,financeid,financename,ucatid,ucat,uname,doctor,nurse,compounder,umobile,umail,upass,uregdate,ustatus])
        mysql.connection.commit()
        cur.close()


    # UPDATE CA_ID
    def updatecaid(caid,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `ca_id`= %s WHERE `client_id`= %s"

        cur.execute(sql,[caid,clientid])
        mysql.connection.commit()
        cur.close()
    

    # CHECK MOBILE NUMBER,EMAIL
    def checkMobileandEmail(umail,umobile):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_mail`,`user_mobile`,`user_cat_id` FROM `user_table` WHERE ( `user_mail` = %s or `user_mobile`=%s )"
        cur.execute(sql,[umail,umobile])
        data = cur.fetchone()
        cur.close()
        return data


    # CHECK AVALIBILITY
    def checkavaliability(uaddedby):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`,`user_mail`,`user_mobile`,`user_cat_id`,`availability`,`check_aval` FROM `user_table` WHERE `user_added_by`=%s"
        cur.execute(sql,[uaddedby])
        data = cur.fetchall()
        cur.close()
        return data


    # UPDATE AVALIABILITY
    def updateavaliabilityfalse(cctid,managementid,financeid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 0 WHERE `user_id` in (%s,%s,%s)"
        cur.execute(sql,[cctid,managementid,financeid])
        mysql.connection.commit()
        cur.close()

    #GET ALL USERS FROM USER_TABLES
    def select(ucatid,uaddedby):
        cur = mysql.connection.cursor()

        # sql = "SELECT `user_id`, `user_name`, `user_cat_id`, `user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`,date_format(`otp_date`,'%%Y-%%m-%%d') as otp_date, `otp_attempts`,date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`,`login_attempts`,date_format(`login_date`,'%%Y-%%m-%%d') as login_date, `token` FROM `user_table` where user_cat_id = %s and      user_added_by = %s"
        
        sql = "SELECT `user_id`, `user_name`, `user_cat_id`, `user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`, \
           DATE_FORMAT(`otp_date`, '%%Y-%%m-%%d') AS `otp_date`, `otp_attempts`, DATE_FORMAT(`user_reg_date`, '%%Y-%%m-%%d') AS `user_reg_date`, \
           `user_status`, \
           CASE `availability` \
               WHEN 1 THEN 'available' \
               WHEN 0 THEN 'assigned' \
               ELSE NULL \
           END AS `availability`, \
           `login_attempts`, DATE_FORMAT(`login_date`, '%%Y-%%m-%%d') AS `login_date`, `token` \
           FROM `user_table` \
           WHERE `user_cat_id` = %s AND `user_added_by` = %s AND `user_status`= 1 "

        cur.execute(sql,[ucatid,uaddedby])
        data = cur.fetchall()
       
        cur.close()
        return data


    #GET ALL USERS FROM USER_TABLES
    def selectcst():
        cur = mysql.connection.cursor()

        sql = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE 1 "

        cur.execute(sql)
        data = cur.fetchall()
       
        cur.close()
        return data


    # GET ALL CLIENTS  FORM USER_TABLES 
    def selectclient(ucatid,uaddedby,userid1,userid2,userid3):
        cur = mysql.connection.cursor()

        sql = "SELECT `user_id`, `user_name`, `user_cat_id`, `user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`,date_format(`otp_date`,'%%Y-%%m-%%d') as otp_date, `otp_attempts`,date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`,`login_attempts`,date_format(`login_date`,'%%Y-%%m-%%d') as login_date, `token` FROM `user_table` where user_cat_id = %s and      user_added_by = %s"

        sql1 = "SELECT  `user_name` FROM `user_table` WHERE `user_id` IN(%s, %s, %s);"

        cur.execute(sql,[ucatid,uaddedby])
        data1 = cur.fetchone()
        cur.execute(sql1,[userid1,userid2,userid3])
        data2 = cur.fetchall()

        if data1 and data2:
            s1 = len(data2)
            if s1 :
                s1 -= 1
                data1["name1"] = data2[0]["user_name"]
            if s1 :
                s1 -= 1
                data1["name2"] = data2[1]["user_name"]
            if s1 :
                s1 -= 1
                data1["name3"] = data2[2]["user_name"]

        data = data1
        cur.close()
        return data


    # GET ALL USERS  FORM user_table 
    def select1():
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_name`, `user_cat_id`, `user_cat`, `user_mail`, `user_mobile`, `user_pass`, `user_otp`,date_format(`otp_date`,'%Y-%m-%d') as otp_date, `otp_attempts`,date_format(`user_reg_date`,'%Y-%m-%d') as user_reg_date, `user_status`, `availability`,`user_added_by`,`login_attempts`,date_format(`login_date`,'%Y-%m-%d') as login_date, `token` FROM `user_table` where `user_status`= 1 "
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data


       # GET ALL USERS  FORM user_table 
    def selectnewclient(cstid):
        cur = mysql.connection.cursor()

        sql = "SELECT  `client_id`, `ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`,`user_name`, `user_mobile`, `user_mail`, `user_pass`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date FROM `client` WHERE `cst_id`=%s and `user_status`= 1 "

        cur.execute(sql,[cstid])
        data = cur.fetchall()
        cur.close()
        return data


    # CLIENT SELECT ALL
    def clientselect():
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `management`, `cc_team`, `finance`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%Y-%m-%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE 1"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data


    # GET ALL USERS  FORM user_table 
    def clientsingle(clientid):
        cur = mysql.connection.cursor()
        sql = "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, `user_reg_date`, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `client_id` = %s"
        cur.execute(sql,[clientid])
        data = cur.fetchone()
        cur.close()
        return data

    
    # CLIENT UPDATE
    def clientupdate(uname,umobile,umail,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `user_name`=%s,`user_mobile`= %s,`user_mail`= %s WHERE `client_id`= %s"
        cur.execute(sql,[uname,umobile,umail,clientid])
        mysql.connection.commit()
        cur.close()


    # GET SINGLE USER FROM user_table
    def single(uidd):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_id` = %s "
        cur.execute(sql,[uidd])
        data = cur.fetchone()
        cur.close()
        return data


    # EDIT DETAILS
    def edit(uname,ucatid,ucat,umail,umobile,ustatus,uid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_name`= %s,`user_cat_id`= %s,`user_cat`= %s,`user_mail`= %s,`user_mobile`= %s,`user_status`= %s  WHERE `user_id`= %s "
        cur.execute(sql,[uname,ucatid,ucat,umail,umobile,ustatus,uid])
        mysql.connection.commit()
        cur.close()


    # CHECK EMAIL FOR EDIT
    def checkEmailforUpdate(umail,uid):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_mail` from user_table where `user_mail` = %s and `user_id` != %s"
        cur.execute(sql,[umail,uid])
        data = cur.fetchone()
        cur.close()
        return data


    # CHECK MOBILE FOR EDIT
    def checkMobileforUpdate(umobile,uidd):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_mobile` from user_table where `user_mobile` = %s and `user_id` != %s"
        cur.execute(sql,[umobile,uidd])
        data = cur.fetchone()
        cur.close()
        return data


   ############### GET LAST ID ###############


    # LAST ID
    def lastid():
        cur=mysql.connection.cursor()
        sql = "SELECT MAX(`client_id`) as client_id FROM `client` WHERE 1;"
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
        return data


############### FORGOT PASSWORD ##############


    # CHECK ADMIN EMAIL FOR FORGOT PASSWORD
    def forget(uname):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id`,`user_name`,`user_pass`,`user_mail`,`user_mobile`,`login_attempts`, date_format(`login_date`,'%%Y-%%m-%%d') as login_date,`otp_attempts`,date_format(`otp_date`,'%%Y-%%m-%%d') as`otp_date` , `user_role`,`token`  FROM `user_table`  WHERE ( `user_mail` = %s ) and `user_status`=1"

        cur.execute(sql,[uname])
        data = cur.fetchone()
        return data


    # FORGET PASSWORD
    def forgetpass(pas,mail):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_pass`= %s WHERE `user_mail`=%s"
        cur.execute(sql,[pas,mail])
        mysql.connection.commit()
        cur.close()
   
############### Added By ################ 


# ADDING DETAILS TO DEEPFACTS
    def adddeeplink(superadminid,adminid,cstid):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `user_tables`(`super_admin_id`, `admin_id`, `cst_id`) VALUES (%s,%s,%s)"

        cur.execute(sql,[superadminid,adminid,cstid])
        mysql.connection.commit()
        cur.close()


############### GETTING USERID WITH MOBILE NUMBER ################ 

# GETTING DETAILS WITH MOBILE NUMBER
    def detailswithmobile(umobile):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id` FROM `user_table` WHERE `user_mobile` = %s"

        cur.execute(sql,[umobile])
        data = cur.fetchone()
        return data 


 # DELETE ADMIN
    def deleteuser(userid):
        cur=mysql.connection.cursor()
        sql ="DELETE FROM `user_table` WHERE `user_id`= %s "
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()


# UPDATE AVALIABILITY
    def updateavaliabilitytrue(cctid,managementid,financeid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 1 WHERE `user_id` in (%s,%s,%s)"
        cur.execute(sql,[cctid,managementid,financeid])
        mysql.connection.commit()
        cur.close()



#SELECT CLIENT ADD DETAILS
    def detailsofclientadded(clientid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `cct_id`, `management_id`, `finance_id` FROM `tagging` WHERE  `client_id`=%s"

        cur.execute(sql,[clientid])
        data = cur.fetchone()
        return data 


    # SELECT CLIENT ADD DETAILS
    def deleteclient(clientid):
        cur=mysql.connection.cursor()
        sql ="UPDATE `client` SET`user_status`= 0 WHERE `client_id`=%s"
        cur.execute(sql,[clientid])
        mysql.connection.commit()
        cur.close()

# SELECT CLIENT DELETED DETAILS
    def selectdeleteclientdetails(clientid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `cct_id`, `management_id`, `finance_id` FROM `client` WHERE  `client_id`=%s"

        cur.execute(sql,[clientid])
        data = cur.fetchone()
        return data 


# checkcctavaliabilitytodelete
    def checkcmfavaliabilitytodelete(userid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_id` = %s"

        cur.execute(sql,[userid])
        data = cur.fetchone()
        return data 


# DELETE CCT/MANAGEMENT/FINANACE
    def updatecmf(userid):
        cur=mysql.connection.cursor()
        sql ="UPDATE `user_table` SET `user_status`= 0 WHERE `user_id` = %s"
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()


# DELETE CCT/MANAGEMENT/FINANACE
    def updatecmf1(useridold):
        cur=mysql.connection.cursor()
        sql ="UPDATE `user_table` SET `user_status`= 0 WHERE  `user_id` = %s"
        cur.execute(sql,[useridold])
        mysql.connection.commit()
        cur.close()

# select cct
    def selectcctclientdatatodelete(cctid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`,  date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `cct_id` = %s and `user_status`= 1"

        cur.execute(sql,[cctid])
        data = cur.fetchall()
        return data


# select management
    def selectmanagementclientdatatodelete(managementid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`,  date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `management_id` = %s and `user_status`= 1"

        cur.execute(sql,[managementid])
        data = cur.fetchall()
        return data


# select management
    def selectfinanceclientdatatodelete(financeid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`,  date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `finance_id` = %s and `user_status`= 1"

        cur.execute(sql,[financeid])
        data = cur.fetchall()
        return data


# single cct client


    def selectsingleclientdatatoupdate(clientid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, `user_reg_date`, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `client_id` = %s"

        cur.execute(sql,[clientid])
        data = cur.fetchone()
        return data


# UPDATE SINGLE CCT CLIENT
    def updatesinglecctclient(cctid,cctname,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `cct_id`= %s, `cct_name`= %s WHERE `client_id`= %s"
        cur.execute(sql,[cctid,cctname,clientid])
        mysql.connection.commit()
        cur.close()


# UPDATE SINGLE MANAGEMENT CLIENT
    def updatesinglemanagementclient(managementid,managementname,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `management_id`= %s, `management_name`= %s WHERE `client_id`= %s"
        cur.execute(sql,[managementid,managementname,clientid])
        mysql.connection.commit()
        cur.close()


# UPDATE SINGLE FINANACE CLIENT
    def updatesinglefinanceclient(financeid,financename,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `finance_id`= %s, `finance_name`= %s WHERE `client_id`= %s"
        cur.execute(sql,[financeid,financename,clientid])
        mysql.connection.commit()
        cur.close()


# UPDATE SINGLE CCT CLIENT
    def updateoldcctavaliability(useridold):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 1 WHERE `user_id`= %s"
        cur.execute(sql,[useridold])
        mysql.connection.commit()
        cur.close()


# UPDATE SINGLE CCT CLIENT
    def updatenewcctavaliability(useridnew):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 0 WHERE `user_id`= %s"
        cur.execute(sql,[useridnew])
        mysql.connection.commit()
        cur.close()


# UPDATE SINGLE CST CLIENT
    def updatecstavaliability(cstid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 1 WHERE `user_id`= %s"
        cur.execute(sql,[cstid])
        mysql.connection.commit()
        cur.close()


# GETTING THE NUMBER OF CST ADDED BY CLIENT
    def selectnoofcstaddedbyadmin(useradded1,useradded2):
        cur=mysql.connection.cursor()

        cst_data=[]
        
        sql = "SELECT `user_cat_id`, `user_cat` FROM `user_table` WHERE `user_added_by`= %s"
        sql1= "SELECT `user_id` FROM `user_table` WHERE `user_added_by`= %s "

        a1 = cur.execute(sql,[useradded1])
        d1=cur.fetchone()
        a2 = cur.execute(sql1,[useradded2])
        d2=cur.fetchall()

        if d1 and d2:
            d1['cst_team'] = [d["user_id"] for d in d2]
            
            cst_data.append(d1)

        # cst_team.append(data)
            return cst_data


# GETTING TEAM DETAILS WRT TO ADMIN ADDED BY CST

    def selectcatdatawrtclient(cst_team,ucatid):
        
        cur = mysql.connection.cursor()

        print(cst_team)
        print(type(cst_team))
        cst_team = json.loads(cst_team)
        print(cst_team)
        print(type(cst_team))
       
        placeholders = ",".join(["%s"] * len(cst_team))

        sql = f"SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval` FROM `user_table` WHERE `user_added_by` IN ({placeholders}) "

        sql1 = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval` FROM `user_table` WHERE 	`user_cat_id`= %s"

       

        print(sql)
        # params = [cst_team] + [ucatid]
        cur.execute(sql,cst_team)
        cur.execute(sql1,[ucatid])
        
        data = cur.fetchall()
        cur.close()
        return data


# CLIENT SELECT WRT TO ADMIN

    def selectclientwrtadmin(cst_team):
        
        cur = mysql.connection.cursor()

        print(cst_team)
        print(type(cst_team))
        cst_team = json.loads(cst_team)
        print(type(cst_team))
       
        placeholders = ",".join(["%s"] * len(cst_team))

        sql = f"SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE  `cst_id` IN ({placeholders}) "

        sql1 = "SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%d-%m-%Y') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `user_status`= 1"

       

        print(sql)
        # params = [cst_team] + [ucatid]
        cur.execute(sql,cst_team)
        cur.execute(sql1)
        # cur.execute(sql1,[ucatid])
        
        data = cur.fetchall()
        cur.close()
        return data
    

# SELECT INACTIVE USERS WRT ADMIN
    def selectinactiveusers(ustatus):#   pending to do later
        cur = mysql.connection.cursor()
        

        sql = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%d-%%m-%%Y') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_status` = %s"

        cur.execute(sql, [ustatus])
        data = cur.fetchall()

        return data


# UPDATE STATUS TO 1
    def updatestatustoactive(useridold):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_status`= 1 WHERE `user_id`= %s"
        cur.execute(sql,[useridold])
        mysql.connection.commit()
        cur.close()


############### SUPER ADMIN ###############


# SELECT CST data WRT SUPER ADMIN

    def selectnoofcstaddedbysuperadmin(useradded1,useradded2):
        cur=mysql.connection.cursor()

        admin_data=[]
        
        sql = "SELECT `user_cat_id`, `user_cat` FROM `user_table` WHERE `user_added_by`= %s"
        sql1= "SELECT `user_id` FROM `user_table` WHERE `user_added_by`= %s "

        a1 = cur.execute(sql,[useradded1])
        d1=cur.fetchone()
        a2 = cur.execute(sql1,[useradded2])
        d2=cur.fetchall()

        if d1 and d2:
            d1['admin_team'] = [d["user_id"] for d in d2]
            
            admin_data.append(d1)
            return admin_data
        

# SELECT CST DATA WRT SUPER ADMIN
    def selectadmindatawrtsuperadmin(admin_team,ucatid):
        
        cur = mysql.connection.cursor()

        print(admin_team)
        print(type(admin_team))
        admin_team = json.loads(admin_team)
        print(type(admin_team))
       
        placeholders = ",".join(["%s"] * len(admin_team))

        sql = f"SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval` FROM `user_table` WHERE `user_added_by` IN ({placeholders}) "

        sql1 = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval` FROM `user_table` WHERE 	`user_cat_id`= %s"
        
        print(sql)
        # params = [cst_team] + [ucatid]
        cur.execute(sql,admin_team)
        cur.execute(sql1,[ucatid])
        
        data = cur.fetchall()
        cur.close()
        return data


# SELECT  CCT/MANAGEMENT/FINANACE WRT SUPER ADMIN
    def selectcctmfwrtsuperadmin(ucatid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_cat_id` = %s and `user_status`= 1"

        cur.execute(sql,[ucatid])
        data = cur.fetchall()
        return data
   

# SELECT  CLIENT WRT SUPER ADMIN
    def selectclientwrtsuperadmin(ucatid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `user_cat_id`=%s and `user_status`= 1"

        cur.execute(sql,[ucatid])
        data = cur.fetchall()
        return data


############## INACTIVATE CST ###############


# SELECT  CLIENT TO CHANGE CST
    def selectusertabletochangecst(userid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_id` = %s"

        cur.execute(sql,[userid])
        data = cur.fetchone()
        return data
    

# SELECT  CLIENT TO CHANGE CST
    def selectclienttochangecst(userid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, `user_reg_date`, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE  `cst_id` = %s AND `user_status` = 1"
        

        cur.execute(sql,[userid])
        data = cur.fetchall()
        return data
    

# SELECT  CLIENT TO CHANGE CST
    def selectclientusertabletochangecst(userid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, `user_reg_date`, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE  `cst_id` = %s AND `user_status` = 1"
        
        sql1 ="SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_added_by`=%s AND `availability`= 1"

        cur.execute(sql,[userid])
        data = cur.fetchall()
        cur.execute(sql1,[userid])
        data1 = cur.fetchall()
        return data,data1
    


# UPDATE USER ADDED BY WRT USER_TABLE
    def updateuseraddedby(uaddedby,userid1,userid2,userid3):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_added_by`= %s WHERE `user_id` IN (%s, %s, %s)"
        cur.execute(sql,[uaddedby,userid1,userid2,userid3])
        mysql.connection.commit()
        cur.close()


# UPDATE USER ADDED BY WRT USER_TABLE
    def updateuserstatus(userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_status`= 0 ,`availability`= 1 WHERE `user_id`=%s"
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()


# UPDATE USER ADDED BY WRT  CLIENT
    def updateclientcst(cstid,clientid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `client` SET `cst_id`= %s WHERE `client_id`= %s"
        cur.execute(sql,[cstid,clientid])
        mysql.connection.commit()
        cur.close()

# UPDATE USER ADDED BY in cst avaliable team
    def updateuseraddedbyforcstdeactivate(uaddedby,userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `user_added_by`= %s WHERE `user_id`= %s"
        cur.execute(sql,[uaddedby,userid])
        mysql.connection.commit()
        cur.close()


############### DEACTIVATE ADMIN WRT TO SUPER ADMIN ###############


# SELECT  CLIENT TO CHANGE CST
    def selectusertabletochangecstaddedby(userid1):
        cur=mysql.connection.cursor()
        
        
        sql ="SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_added_by`=%s AND `availability`= 1"

        cur.execute(sql,[userid1])
        data = cur.fetchall()
       
        return data
    

# SELECT SINGLE CST TO CHANGE ADDEDBY 
    def selectsinglecsttochangecstaddedby(userid):
        cur=mysql.connection.cursor()
        
        sql ="SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_id` = %s"

        cur.execute(sql,[userid])
        data = cur.fetchone()
       
        return data
    

# SELECT  CLIENT TO CHANGE CST
    def selectcstuseraddedbytodeactivate():
        cur=mysql.connection.cursor()
        
        sql= "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE 1"

        cur.execute(sql)
        data = cur.fetchall()
        return data
    

############# MISC #############


# SELECT  CLIENT TO CHANGE CST
    def selectcsttocheckavaliability(ucatid,useraddedby):
        cur=mysql.connection.cursor()
        
        sql= "SELECT COUNT(`user_added_by`) as count FROM `user_table` WHERE `user_cat_id` = %s and `user_added_by`= %s and `user_status` = 1;"

        cur.execute(sql,[ucatid,useraddedby])
        data = cur.fetchone()
        return data
    

# SELECT  ALL USERTABLE CST COUNT TO CAHNGE AVALIABILITY TO FALSE
    def selectallcstcount(ucatid1,ucatid2,ucatid3,useraddedby):
        cur=mysql.connection.cursor()
        
        sql= "SELECT COUNT(`user_added_by`) as count FROM `user_table` WHERE `user_cat_id` IN (%s,%s,%s) and `user_added_by`= %s and `user_status` = 1;"

        cur.execute(sql,[ucatid1,ucatid2,ucatid3,useraddedby])
        data = cur.fetchone()
        return data
    

# SELECT  ALL USERTABLE CST COUNT TO CAHNGE AVALIABILITY TO FALSE
    def selectallclientcstcount(cstid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT COUNT(`cst_id`) as count FROM `client` WHERE `cst_id` = %s and `user_status` = 1;"

        cur.execute(sql,[cstid])
        data = cur.fetchone()
        return data
    

# UPDATE AVALIABILITY
    def updateavaliabilityforall(cstid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `user_table` SET `availability`= 0 WHERE `user_id`= %s"
        cur.execute(sql,[cstid])
        mysql.connection.commit()
        cur.close()
    

############### FINANACE ###############


# SELECT  FINANCE TAGGED CLIENT FROM CLIENT TABLE
    def selectfinancetaggedclient(financeid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `finance_id` = %s and `user_status` = 1"

        cur.execute(sql,[financeid])
        data = cur.fetchall()
        return data


############### MANAGEMENT ###############


# SELECT  FINANCE TAGGED CLIENT FROM CLIENT TABLE
    def selectmanagementtaggedclient(managementid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `management_id` = %s and `user_status` = 1"

        cur.execute(sql,[managementid])
        data = cur.fetchall()
        return data
    

############### MANAGEMENT ###############


# SELECT  CCT TAGGED CLIENT FROM CLIENT TABLE
    def selectcctaggedclient(managementid):
        cur=mysql.connection.cursor()
        
        sql= "SELECT `client_id`,`ca_id`, `cst_id`, `cct_id`, `cct_name`, `management_id`, `management_name`, `finance_id`, `finance_name`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `client` WHERE `cct_id` = %s and `user_status` = 1"

        cur.execute(sql,[managementid])
        data = cur.fetchall()
        return data
    

############### SUB FINANCE  ###############

#ADDING TO SUB FINANACE
    def addsubfinance(financeid,financename,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `finance`(`finance_id`, `finance_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_reg_date`, `user_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sql,[financeid,financename,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus])
        mysql.connection.commit()
        cur.close()


# CHECK MOBILE AND MAIL IN  SUB FINANACE
    def checkMobileandEmailinsubfinanace(submobile,submail):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_sub_mobile`, `user_sub_mail` FROM `finance` WHERE (`user_sub_mobile` = %s or `user_sub_mail` = %s)"
        cur.execute(sql,[submobile,submail])
        data = cur.fetchone()
        cur.close()
        return data
    

# SELECT ALL FROM SUB FINANACE
    def selectallsubfinance(usubcatid,financeid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `finance_id`, `finance_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `finance` WHERE  `user_sub_cat_id` = %s and `finance_id` = %s and `user_status`=1 "
        cur.execute(sql,[usubcatid,financeid])
        data = cur.fetchall()
        cur.close()
        return data
    

# SELECT ONE FROM SUB FINANACE TO UPDATE
    def selectonesubfinancetoupdate(userid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `finance_id`, `finance_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `finance` WHERE  `user_id` =%s "
        cur.execute(sql,[userid])
        data = cur.fetchone()
        cur.close()
        return data
    
    
# UPDATE SUB FINANCE
    def updatesubfinance(subname,submobile,submail,userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `finance` SET  `user_sub_name`= %s,`user_sub_mobile`= %s,`user_sub_mail`= %s WHERE `user_id`=%s"
        cur.execute(sql,[subname,submobile,submail,userid])
        mysql.connection.commit()
        cur.close()


# DEACTIVATE SUB FINANACE
    def deactivatesubfinance(userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `finance` SET `user_status`= 0 WHERE `user_id`= %s"
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()
    
    
############### SUB MANAGEMENT  ###############

#ADDING TO SUB MANAGEMENT
    def addsubmanagement(managementid,managementname,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `management`(`management_id`, `management_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_reg_date`, `user_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sql,[managementid,managementname,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus])
        mysql.connection.commit()
        cur.close()


# CHECK MOBILE AND MAIL IN  SUB COMMAND CENTER TEAM
    def checkMobileandEmailinmanagement(submobile,submail):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_sub_mobile`, `user_sub_mail` FROM `management` WHERE (`user_sub_mobile` = %s or `user_sub_mail` = %s)"
        cur.execute(sql,[submobile,submail])
        data = cur.fetchone()
        cur.close()
        return data
    

# SELECT ALL FROM SUB COMMAND CENTER TEAM
    def selectallsubmanagement(usubcatid,managementid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `management_id`, `management_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `management` WHERE  `user_sub_cat_id` = %s and `management_id` = %s and `user_status`=1 "
        cur.execute(sql,[usubcatid,managementid])
        data = cur.fetchall()
        cur.close()
        return data
    

# SELECT ONE FROM SUB COMMAND CENTER TEAM TO UPDATE
    def selectonesubmanagementtoupdate(userid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `management_id`, `management_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `management` WHERE  `user_id` =%s "
        cur.execute(sql,[userid])
        data = cur.fetchone()
        cur.close()
        return data
    
    
# UPDATE SUB COMMAND CENTER TEAM
    def updatesubmanagement(subname,submobile,submail,userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `management` SET  `user_sub_name`= %s,`user_sub_mobile`= %s,`user_sub_mail`= %s WHERE `user_id`=%s"
        cur.execute(sql,[subname,submobile,submail,userid])
        mysql.connection.commit()
        cur.close()


# DEACTIVATE SUB FINANACE
    def deactivatesubmanagement(userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `management` SET `user_status`= 0 WHERE `user_id`= %s"
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()


############### SUB COMMAND CENTER TEAM  ###############

#ADDING TO SUB COMMAND CENTER TEAM
    def addsubcct(cctid,cctname,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `cct`(`cct_id`, `cct_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_reg_date`, `user_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur.execute(sql,[cctid,cctname,subcatid,subcat,subname,submobile,submail,subpass,userregdate,userstatus])
        mysql.connection.commit()
        cur.close()


# CHECK MOBILE AND MAIL IN  SUB COMMAND CENTER TEAM
    def checkMobileandEmailinsubcct(submobile,submail):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_sub_mobile`, `user_sub_mail` FROM `cct` WHERE (`user_sub_mobile` = %s or `user_sub_mail` = %s)"
        cur.execute(sql,[submobile,submail])
        data = cur.fetchone()
        cur.close()
        return data
    

# SELECT ALL FROM SUB COMMAND CENTER TEAM
    def selectallsubcct(usubcatid,cctid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `cct_id`, `cct_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `cct` WHERE  `user_sub_cat_id` = %s and `cct_id` = %s and `user_status`=1 "
        cur.execute(sql,[usubcatid,cctid])
        data = cur.fetchall()
        cur.close()
        return data
    

# SELECT ONE FROM SUB COMMAND CENTER TEAM TO UPDATE
    def selectonesubccttoupdate(userid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `cct_id`, `cct_name`, `user_sub_cat_id`, `user_sub_cat`, `user_sub_name`, `user_sub_mobile`, `user_sub_mail`, `user_sub_pass`, `user_sub_otp`, `otp_attempts`, `otp_date`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date, `login_attempts`, `login_date`, `user_status`, `token` FROM `cct` WHERE  `user_id` =%s "
        cur.execute(sql,[userid])
        data = cur.fetchone()
        cur.close()
        return data
    
    
# UPDATE SUB COMMAND CENTER TEAM
    def updatesubcct(subname,submobile,submail,userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `cct` SET  `user_sub_name`= %s,`user_sub_mobile`= %s,`user_sub_mail`= %s WHERE `user_id`=%s"
        cur.execute(sql,[subname,submobile,submail,userid])
        mysql.connection.commit()
        cur.close()


# DEACTIVATE SUB CCT
    def deactivatesubcct(userid):
        cur = mysql.connection.cursor()
        sql = "UPDATE `cct` SET `user_status`= 0 WHERE `user_id`= %s"
        cur.execute(sql,[userid])
        mysql.connection.commit()
        cur.close()


############### SERVICE TEAM ###############


# SELECT ALL FROM SUB FINANACE
    def selectallserviceteam(ucatid):
        cur=mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_cat_id`, `user_cat`, `user_name`, `user_mobile`, `user_mail`, `user_pass`, `user_otp`, `user_reg_date`, `user_status`, `availability`, `user_added_by`, `check_aval`, `login_attempts`, `login_date`, `otp_attempts`, `otp_date`, `token` FROM `user_table` WHERE `user_cat_id` = %s "
        cur.execute(sql,[ucatid])
        data = cur.fetchall()
        cur.close()
        return data
        

# ADDING TO SUB COMMAND CENTER TEAM
    def addemployee(name,age,occupation):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO `employee`(`name`, `age`, `occupation`) VALUES (%s, %s, %s)"

        cur.execute(sql,[name,age,occupation])
        mysql.connection.commit()
        cur.close()


############## SHOW DOCTOR NURSE AND COMPOUNDER ################


# DOCTOR
    def selectclinicdetails(clientid):
        cur=mysql.connection.cursor()
        sql = "SELECT  `doctor`,`nurse`,`compounder`, date_format(`user_reg_date`,'%%Y-%%m-%%d') as user_reg_date FROM `client` WHERE `client_id` = %s"
        cur.execute(sql,[clientid])
        data = cur.fetchall()
        cur.close()
        return data
    

# NURSE 
    def selectallnurse(clientid):
        cur=mysql.connection.cursor()
        sql = "SELECT `nurse` FROM `client` WHERE `client_id` = %s"
        cur.execute(sql,[clientid])
        data = cur.fetchall()
        cur.close()
        return data
    

# COMPOUNDER
    def selectallcompounders(clientid):
        cur=mysql.connection.cursor()
        sql = "SELECT `compounder` FROM `client` WHERE `client_id` = %s"
        cur.execute(sql,[clientid])
        data = cur.fetchall()
        cur.close()
        return data