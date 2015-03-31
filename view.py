import unbxd.api 
import logging
import json
from flask import Flask,session, redirect, url_for, escape,g
from flask import request
from flask import render_template
from flask_oauth import OAuth
from response_handler import *
from exception_handler import *
from services import *
from data_handler import *
from flask.ext.mail import Mail,Message
import os
import smtplib
glob={}
glob['company']=[]
app = Flask(__name__)
gmail_user="autosuggest.unbxd@gmail.com"
gmail_pwd="sales@unbxd"
TO=['autosuggest.unbxd@gmail.com']
FROM = 'autosuggest.unbxd@gmail.com'
SUBJECT="COMMIT IN AUTOSUGGEST"



#-----------------logging------------------->
logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
#-------------------------------------------->
'''




mail=Mail(app)
app.config.update(MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'autosuggest.unbxd@gmail.com',
    MAIL_PASSWORD = 'sales@unbxd')
'''
@app.before_request
def load_company():
    g.company=glob['company']
REDIRECT_URI = '/oauth2callback'
oauth = OAuth()

GOOGLE_CLIENT_ID = '194053695850-lp2mvh02bjes0jopndeai2pnpo0ujsmv.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'z_m7wbB4fJEfVRYI9SvsehI5'

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def start():
    logger.info("company name stored in global variable")
    glob['company']=read_only_data()
    g.company=glob['company']
    if "mail" in session:
        return redirect(url_for('simple_login'))
    elif request.method=='GET':
        return render_template("signup.html")
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#--------------------------SIGN UP GET DATA-----------------------#

@app.route('/signup_data', methods=['POST','get'])
def signup_data():
    if "mail" in session:
        return redirect(url_for("simple_login"))
        #print"login"
    elif request.method=='POST':
        data_dict=request.form.to_dict()
        #print data_dict
        user_name=str(request.form['mail'])
        password=str(request.form['password'])
        service_obj=services()
        sign_done=service_obj.insert(user_name,password)
        session['mail'] = request.form['mail']
        session['gmail']='NO'
        logger.info("mail in session and gmail no")
        glob['company']=read_only_data()
        logger.info("sign in done")
        return '%s' % sign_done
    return redirect(url_for("simple_login"))
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#-------------------------LOG IN FOR GOOGLE--------------------------#
@app.route('/dashboard')
def dashboard():
    if "mail" in session:
        if "gmail" not in session:
            #print"gmail"
            if request.method=='GET':
                #print "get"
                access_token = session.get('mail')
                access_token = access_token[0]
                from urllib2 import Request, urlopen, URLError
                headers = {'Authorization': 'OAuth '+access_token}
                req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
                try:
                    res = urlopen(req)
                except URLError, e:
                    if e.code == 401:
                    # Unauthorized - bad token
                        logger.error("unauthorized bad token")
                        logger.error(e)
                        session.pop('mail', None)
                        return redirect(url_for('login'))
                    return res.read()
                response_text=str(res.read())
                parse_response_text=json.loads(response_text)
                logger.info("parse_response_text")
                verify_email=parse_response_text['email']
                logger.info("email_check")
                verify_email_id=verify_email[-9:]
                if(verify_email_id !='unbxd.com'):
                    logger.warn("pls use yours verified mail")
                    return redirect(url_for("logout"))
                service_obj=services()
                user_db=service_obj.check(verify_email)
                if(user_db=='new user'):
                    logger.info("new user")
                    service_obj.insert(verify_email,"google login")
                permissions=service_obj.session_permission(verify_email)
                #print permissions
                #print type(permissions[2])
                if(permissions[1]):
                    logger.info(session['mail'])
                    logger.info("write permission")
                    session['write']='YES'
                else:
                    logger.info(session['mail'])
                    logger.info("no write permission")
                    session['write']='NO'
                if(permissions[2]):
                    logger.info(session['mail'])
                    logger.info("delete permission")
                    session['delete']='YES'
                else:
                    logger.info(session['mail'])
                    logger.info("no delete permisssion")
                    session['delete']='NO'
                session['gmail']=parse_response_text
                glob['company']=read_only_data()
                return redirect(url_for("simple_login"))
            else:
                logger.info("not get request")
                return redirect(url_for("simple_login"))
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/simple_login')
def simple_login():
    print session
    if "mail" in session:
        logger.info("simple login")
        return render_template("box/simple_login.html");
    else:
        return redirect(url_for('login'))

#-------------------------------------------------------------------------------------------------------------------->
#-------------------------------------------------------------->
#--------------------------PRINT PARAMETER------------------------>
@app.route('/metric_type')
def metric_type():
    if "mail" in session:
        #if request.method=='POST':
        data_dict = str(request.args.get('data'))
        replace_data=data_dict.replace("_"," ")
        return render_template("box/param.html",response=replace_data)
    else:
        return redirect(url_for("login"))        
#-------------------------------------------------------------->
#--------------------------add suggestion --------------------->
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    if "mail" in session:
        try:
            if request.method=='GET':
                company = str(request.args.get('company'))
                data = str(request.args.get('data'))
                #print "add suggestion"
                #print company,data
                data=str(data[1:])
                if company!="":
                    handler=data_handler()
                    handler_data=str(handler.add_unbxd_suggestion(company,data))
                    #print handler_data                    
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.unbxdsuggestion.update(data=handler_data)
                    res_popular=response_handler()
                    final_message=str(res_popular.addSuggestion(products))
                    #return '%s' % final_message
                    #print products
                    try:
                        print session['gmail']['email']
                        logger.info("add suggestions "+str(session['gmail']['email'])+":"+data+":"+company)
                    except:
                        logger.info("add suggestion "+str(session['mail'])+":"+data+":"+company)
                    logger.info("updated the suggestion data")
                    return redirect(url_for("display_suggestion",command=company,metric="Suggestion"))                    
                else:
                    logger.critical("company not specified")
                    return redirect(url_for("error",message="Company not Specified"))
            else:
                logger.warn("access not allowed")
                return redirect(url_for("error",message="Access Not Allowed"))    
        except Exception as e:
            logger.debug(e)
            print e
            return redirect(url_for("error",message=e))
    else:
        return redirect(url_for("login"))

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------delete unbxd suggestion ---------->
@app.route('/delete_unbxd_suggestion')
def delete_unbxd_suggestion():
    if "mail" in session:
        if request.method=='GET':
            return render_template("delete_unbxd_suggestion.html")
    else:
        return redirect(url_for("login"))
@app.route('/delete_suggestion_data', methods=['POST','get'])
def delete_suggestion_data():
    #print("1")
    if "mail" in session:
        try:
            if request.method=='GET':
                company=str(request.args.get('company'))
                field=str(request.args.get('data'))[1:-1]
                if company!="":
                    handler=data_handler()
                    handler_data=str(handler.delete_unbxd_suggestion(company,field))
                    print handler_data
                    #msg = Message('Hello',sender='autosuggest.unbxd@gmail.com',recipients=['autosuggest.unbxd@gmail.com'])
                    #msg.body = "suggestion deleted"
                    #print msg
                    #print mail
                    #print "mail"
                    #mail.send(msg)
                    #smtpObj = smtplib.SMTP('localhost')
                    #smtpObj.login("alok.gupta1785@gmail.com", "applemacbookpro")
                    #smtpObj.sendmail("autosuggest.unbxd@gmail.com", "alok.gupta1785@gmail.com", session['mail']) 

                    #TEXT = session['mail']+"THIS EMAIL-ID COMMITED IN AUTOSUGGEST API"

                    # Prepare actual message
                    #message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
                
                    #server = smtplib.SMTP(SERVER) 
                    #server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                    #server.ehlo()
                    #server.starttls()
                    #server.login(gmail_user, gmail_pwd)
                    #server.sendmail(FROM, TO, message)
                    #server.quit()
                    #server.close()
                    #print 'successfully sent the mail'
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.unbxdsuggestion.delete(data=handler_data)
                    res_popular=response_handler()
                    final_message=str(res_popular.delSuggestion(products))
                    print final_message
                    try:
                        print session['gmail']['email']
                        logger.info("delete suggestion "+str(session['gmail']['email'])+":"+field+":"+company)
                    except:
                        logger.info("delete suggestion "+str(session['mail'])+":"+field+":"+company)
                    
                    logger.info("suggestion deleted")
                    
                    return redirect(url_for("display_suggestion",command=company,metric="Suggestion"))
                else:
                    logger.debug("company not specified")
                    return redirect(url_for("error",message="Company Not Specified"))
            else:
                logger.warn("call not allowed")
                return redirect(url_for("error",message="Call Not Allowed"))       
        except Exception as e:
            logger.error(e)
            return redirect(url_for("error",message=e))
    else:
        return redirect(url_for("login"))        

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------add popular product -------------->
@app.route('/add_popular', methods=['POST','get'])
def add_popular():
    if "mail" in session:
        try:
            if request.method=='GET':
                company=str(request.args.get("company"))
                field=str(request.args.get('fields'))
                condition=str(request.args.get('condition'))
                if company!="":
                    handler=data_handler()
                    handler_data=str(handler.add_popular_product(company,field,condition))
                    handler_true_data=str(handler.all_popular_product(company))
                    if (condition=='false'):
                        api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                        products=api.popularproduct.update(data=handler_data)
                        res_popular=response_handler()
                        final_message=str(res_popular.addPopular(products))
                        logger.info("popular product addded withh condition false")
                        try:
                            print session['gmail']['email']
                            logger.info("add popular "+str(session['gmail']['email'])+":"+field+":"+company)
                        except:
                            logger.info("add popular "+str(session['mail'])+":"+field+":"+company)
                    
                        return redirect(url_for("display_suggestion",command=company,metric="Popular Product"))
                    else:
                        multiple_true_check=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                        resp=str(multiple_true_check.popularproduct.all(data=handler_true_data))
                        res_handler=response_handler()
                        times_true=res_handler.true_check(resp)
                        if(times_true<=0):
                            api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                            products=api.popularproduct.update(data=handler_data)
                            res_popular=response_handler()
                            final_message=str(res_popular.addPopular(products))
                            try:
                                print session['gmail']['email']
                                logger.info("add popular "+str(session['gmail']['email'])+":"+field+":"+company)
                            except:
                                logger.info("add popular "+str(session['mail'])+":"+field+":"+company)
                    
                            logger.info("popular product addded withh condition true")
                            return redirect(url_for("display_suggestion",command=company,metric="Popular Product"))
                        else:
                            logger.info("more than one true conditions exits")
                            final_message="true already present->change the condition"
                            return redirect(url_for("display_suggestion",command=company,metric="Popular Product",message="Already Present"))
                else:
                    logger.warn("company not specified")
                    return redirect(url_for("error",message="Company Not Specified"))
            else:
                logger.info("call not allowed")
                return redirect(url_for("error",message="Call Not Allowed"))       
        except Exception as e:
            logger.debug(e)
            return redirect(url_for("error",message=e))
    else:
        return redirect(url_for('login')) 
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>
#---------------------delete popular product ---------------->
@app.route('/delete_popular_product')
def delete_popular_product():
    if "mail" in session:
        if request.method=='GET':
            return render_template("delete_popular_product.html")
    else:
        return redirect(url_for("login"))
@app.route('/delete_popular', methods=['POST','get'])
def delete_popular():
    if "mail" in session:
        try:
            if request.method=='GET':
                company=str(request.args.get("company"))
                field=str(request.args.get("data"))[1:-1]
                if company!="":
                    handler=data_handler()
                    handler_data=(handler.delete_popular_product(company,field))
                    print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=str(api.popularproduct.delete(data=handler_data))
                    #print products
                    #print products
                    res_popular=response_handler()
                    final_message=str(res_popular.delPopular(products))
                    logger.info("popular product deleted")
                    try:
                        print session['gmail']['email']
                        logger.info("delete popular "+str(session['gmail']['email'])+":"+field+":"+company)
                    except:
                        logger.info("delete popular "+str(session['mail'])+":"+field+":"+company)
                    
                    return redirect(url_for("display_suggestion",command=company,metric="Popular Product"))
                else:
                    logger.info("company not specified")
                    return redirect(url_for("error",message="Company Not Specified"))
            else:
                return redirect(url_for("error",message="Call Not Allowed"))       
        except Exception as e:
            logger.debug(e)
            return redirect(url_for("error",message=e))
    else:
        return redirect(url_for("login"))
#------------------------------------------------------------>
#--------------------------add infield ---------------------->
@app.route('/add_in_field', methods=['POST','get'])
def add_in_field():
    if "mail" in session:
        try:
            if request.method=='GET':
                field=str(request.args.get('fields'))
                company=str(request.args.get("company"))
                if company!="":
                    handler=data_handler()
                    handler_data=str(handler.add_in_field(company,field))
                    #print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.infield.update(data=handler_data)
                    try:
                        print session['gmail']['email']
                        logger.info("add infield "+str(session['gmail']['email'])+":"+field+":"+company)
                    except:
                        logger.info("add infield "+str(session['mail'])+":"+field+":"+company)
                                    
                    print products
                    return redirect(url_for("display_suggestion",command=company,metric="In Field"))
                else:
                    return redirect(url_for("error",message="Company Not Specified"))
            else:
                logger.info("request not allowed")
                return redirect(url_for("error",message="Request Not Allowed"))      
        except Exception as e:
            logger.debug(e)
            return redirect(url_for("error",message="Some error occured"))
    else:
         return redirect(url_for('login'))   
#------------------------------------------------------------->
#--------------------------delete infield -------------------->
@app.route('/delete_infield')
def delete_infield():
    if "mail" in session:
        if request.method=='GET':
            return render_template("delete_infield.html")
    else:        
        return redirect(url_for('login'))
@app.route('/delete_in_field', methods=['POST','get'])
def delete_in_field():
    if "mail" in session:                                       
        try:
            if request.method=='GET':
                company=str(request.args.get("company"))
                field=str(request.args.get("data"))[1:-1]
                if company!="":
                    handler=data_handler()
                    handler_data=str(handler.delete_in_field(company,field))
                    #print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.infield.delete(data=handler_data)
                    #print products
                    logger.info("delete in field")
                    try:
                        print session['gmail']['email']
                        logger.info("delete infield "+str(session['gmail']['email'])+":"+field+":"+company)
                    except:
                        logger.info("delete infield "+str(session['mail'])+":"+field+":"+company)
                    
                    return redirect(url_for("display_suggestion",command=company,metric="In Field"))
                else:
                    return redirect(url_for("error",message="Company Not Specified"))
            else:
                return redirect(url_for("error",message="Call Not Allowed"))       
        except Exception as e:
            logger.debug(e)
            return redirect(url_for("error",message=e))
    else:
        return redirect(url_for("login"))
                    
#------------------------------------------------------------>
#-----------------add popular searchable -------------------->
'''
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                services=handler()
                return '%s' % services.infield(message)
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
'''
#------------------------------------------------------------>
#----------------------delete popular searchable  ----------->
@app.route('/delete_popular_searchable_field')
def delete_popular_searchable_field():
    if "mail" in session:
        if request.method=='GET':
            return render_template("delete_popular_product_searchable_field.html")
    else:
        return redirect(url_for('login'))
'''
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                services=handler()
                return '%s' % services.infield(message)
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
'''
#------------------------------------------------------------>
#-----------------view popular searchable ------------------->
'''
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                services=handler()
                return '%s' % services.infield(message)
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
'''
#------------------------------------------------------------>
#--------------------------send autosuggest data------------->
@app.route('/send_autosuggest_data')
def send_autosuggest_data():
    if "mail" in session:
        #return redirect(url_for('login'))
        if request.method=='GET':
            return render_template("send_autosuggest_data.html")
    else:
        return redirect(url_for('login'))
'''
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                services=handler()
                return '%s' % services.infield(message)
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
'''
#------------------------------------------------------------>
#---------------get all popular product --------------------->
    #return render_template("dashboard.html")
#-----------------------login data-------------------------->
@app.route('/validate_mail', methods=['POST','get'])
def validate_mail():
    if "mail" in session:
        return redirect(url_for('dashboard'))
    else:        
        try:
            #print("validate_mail")
            if request.method=='POST':
                data_dict=request.form.to_dict()
                email=str(request.form['mail'])
                service_obj=services()
                response=service_obj.check(email)
                #print temp 
                #print data_dict
                logger.info("email checked")
                return '%s' % response
            else:
                return render_template("dashboard.html")
               
        except:
            return render_template("dashboard.html")
    
#------------------------------------------------------------->
#--------------------------all unbxd suggestion---------------> 
@app.route('/login')
def login():
    if "mail" in session:
        return redirect(url_for('simple_login'))
    elif request.method=='GET':
        return render_template("login.html")
@app.route('/login_data', methods=['POST','get'])
def login_data():
    print session
    if "mail" in session:
        #print"login"
        return redirect(url_for("dashboard"))
    elif request.method=='POST':
        data_dict=request.form.to_dict()
        print data_dict
        user_name=str(request.form['mail'])
        password=str(request.form['password'])
        #print user_name,password
        #email_check=login_handler().email()
        service_obj=services()
        temp=service_obj.validate_user(user_name,password)
        print temp 
        if(str(temp)=='valid'):
            service_obj=services()
            permissions=service_obj.session_permission(user_name)
            print permissions
            #logger.info(session['mail'])
            print type(permissions[2])
            if(permissions[1]):
                #logger.info(session['mail'])
                logger.info("read permission")
                session['write']='YES'
            else:
                #logger.info(session['mail'])
                logger.info("no read permission")
                session['write']='NO'
            if(permissions[2]):
                #logger.info(session['mail'])
                logger.info("delete permission")
                print permissions[2]
                session['delete']='YES'
            else:
                session['delete']='NO'

            session['mail'] = request.form['mail']
            session['gmail']= 'NO'
            glob['company']=read_only_data()
            print session
            return '%s' % temp
        else:
            return redirect(url_for("login"))
        #return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))
#------------------------------------------------------------->
#---------------------get popular data------------------------>        
@app.route('/get_popular_input_data', methods=['POST','get'])
def get_popular_input_data():
    if "mail" in session:                                       
        try:
            if request.method=='POST':
               # print ("2")
                data_dict=request.form.to_dict()
                print "get popular input data"
                print data_dict
                #return data_dict
                '''
                message=str(request.form['command'])

                field=str(request.form['fields'])
                #print message,field
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.delete_in_field(message,field))
                    #print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.infield.delete(data=handler_data)
                    #print products
                    return '%s' % products
                
                else:
                    return render_template("dashboard.html")
                '''
            else:
                return render_template("dashboard.html")
               
        except:
            return render_template("dashboard.html")
    else:        
        return redirect(url_for('login'))
    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>  
#-------------------------read_only_data--------------------->
def read_only_data():
    if "mail" in session:                                       
        try:
            service_obj=services()
            data=service_obj.read_data("alok")
            data=str(data).split(" ")
            outer=[]
            for entry in data[0:-1]:
                inner=[]
                entry=entry.split("_")
                inner.append(entry[0])
                inner.append(entry[1])
                outer.append(inner)
            return outer
            
        except Exception as e:
            logger.debug(e)
            return e
    else:        
        return redirect(url_for('login'))
    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")      
#------------------------------------------------------------>
#-----------------------------log out------------------------>
@app.route('/logout', methods=['POST','get'])
def logout():
    logger.critical("read ,write,delete,mail,gmail session clear")
    session.pop('read',None)
    session.pop('write', None)
    session.pop('delete',None)
    session.pop('mail', None)
    session.pop('gmail', None)
    glob['company']=[]
    return redirect(url_for('login'))

#------------------------------------------------------------>
#----------------------get index files----------------------->
@app.route('/error', methods=['POST','get'])
def error():
    if "mail" in session:
        logger.info("error in alert")
        message=request.args.get("message")
        return render_template("box/error.html",response_text=message)
    else:
        return redirect(url_for("login"))
#------------------------------------------------------------>
#----------------------get index files----------------------->
@app.route('/display_suggestion', methods=['POST','get'])
def display_suggestion():
    if "mail" in session:
        # z=str(request.form['command'])
        #print glob['company']
        company = str(request.args.get('command'))
        #print(company)
        logger.info(company)
        if company!="":
            fields=get_index_fields_to_add(company)
            #print fields
            metric = str(request.args.get('metric'))
            if isinstance(fields,list):
                print "got add data fields"
            else:
                return redirect(url_for("error",message=fields))
            if metric=="Suggestion":            
                result=show_suggestion(company,metric);
                if isinstance(result,list):
                    if len(result)==0:
                        response_text=["infield_list_is_empty *_*"]
                        return redirect(url_for("error",message=response_text))
                    else:
                        logger.debug("error in chossing metrics")
                        return render_template("box/table.html",response_text=result,fields=fields,id=company)
                else:
                    return redirect(url_for("error",message=result))
            elif metric=="In Field":
                result=show_infield(company,metric)
                try:
                    if isinstance(result,list):
                        if len(result)==0:
                            response_text=["infield_list_is_empty *_*"]
                            return redirect(url_for("error",message=response_text))
                        else:
                            return render_template("box/infield.html",response_text=result,fields=fields,id=company)
                    else:
                        return redirect(url_for("error",message=result))
                except:
                    return redirect(url_for("error",message="Sometthing Went Wrong Try Again"))
            elif metric=="Popular Product":
                result=show_popular(company,metric)
                if isinstance(result,list):
                    if request.args.get("message"):
                        print"message"
                        return render_template("box/popular.html",response_text=result,fields=fields,id=company,message=request.args.get("message"))
                    else:
                        return render_template("box/popular.html",response_text=result,fields=fields,id=company)
                else:
                    return redirect(url_for("error",message=result))
            else:
                return redirect(url_for("error",message="Enter the required Metric"))
        else:
            return redirect(url_for("error",message="Company Name not specified"))    
    else:
        return redirect(url_for('login'))
#-------------------------------------------------------------------------------------------------------->
#---------------------------show_suggestion(reads the suggestion value----------------------------------->
def show_suggestion(company,metric):
    if "mail" in session:
        # z=str(request.form['command'])
        company = str(request.args.get('command'))
        metric = str(request.args.get('metric'))
        #print "company id=>"+z
        handler=data_handler()
        handler_data=str(handler.all_popular_product(company))
        api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
        products=api.unbxdsuggestion.all(data=handler_data)
        response_text_json=json.loads(products)
        print response_text_json
        #print str(asd['popularProductFields'][0])
        #print(len(response_text_json['popularProductFields']))
        if (type(response_text_json['keywordSuggestions']) is list):
            response_text=''
            fld_name=''
            outerlist=[]
            innerlist=[]
            for val in response_text_json['keywordSuggestions']:
                #print val
                field_name=(val['fields'])
                #print field_name
                for values in field_name:
                    #print values
                    fld_name=fld_name+str(values)+','
                    #print type(field_name)
                flds=str(val['name'])
                innerlist.append(flds)
                innerlist.append(fld_name[0:-1])
                outerlist.append(innerlist)
                innerlist=[]
                fld_name=''
                #print response_text
                #if request.method=='GET':
            return outerlist
        else:
            return response_text_json['errors'][0]['message']
    else:
        return redirect(url_for('login'))
#---------------------------------------------------------------------------------------------------#
#---------------------------show_infield(reads the in fields values)--------------------------------#
def show_infield(company,metric):
    if 'mail' in session:
        handler=data_handler()
        handler_data=str(handler.get_all_infield(company))
        api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
        products=api.infield.all(data=handler_data)
        response_text_json=json.loads(products)
        #print str(asd['popularProductFields'][0])
        #print(len(response_text_json['popularProductFields']))
        if (type(response_text_json['inFields']) is list):
            response_text=[]
            if (len(response_text_json['inFields']) > 0 ):
                print response_text_json
                for val in response_text_json['inFields']:
                    #print val
                    fields=str(val)
                    response_text.append(fields)
                return response_text
            else:
                return []
        else:
            return response_text_json['errors'][0]['message']
    else:
        return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------#
#---------------------------show_popular(reads popular products)------------------------------#

def show_popular(company,metric):
    handler=data_handler()
    handler_data=str(handler.all_popular_product(company))
    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
    products=str(api.popularproduct.all(data=handler_data))
    #print products
    response_text_json=json.loads(products)
    #print str(asd['popularProductFields'][0])
    #print(len(response_text_json['popularProductFields']))
    if (type(response_text_json['popularProductFields']) is list):
        outer=[]
        inner=[]
        for val in response_text_json['popularProductFields']:
            field_name=str(val['fieldName'])
            condition=str(val['required'])
            #response_text=response_text+(field_name+"--->"+condition+" ")
            #print response_text
            inner.append(field_name)
            inner.append(condition)
            outer.append(inner)
            inner=[]
            #print response_text
        return outer
    else:                  
        return response_text_json['errors'][0]['message']
#--------------------------------------------------------------------------------------------------#
#--------------------------get_index_fields_to_add(gets the fields to add)-------------------------#

def get_index_fields_to_add(message):
    if "mail" in session:                                       
        try:
            data_dict=request.form.to_dict()
            #print mydict
            exception_obj=exception_handler()
            handler_data=str(exception_obj.get_index_field(message))
            json_data=json.loads(handler_data)
            fields=[]
            for item in json_data:
                fields.append(item['fieldName'])
                #print string
                #return '%s' % string
            return fields
        except Exception as e:
            logger.debug(e)
            return e
    else:
        return redirect(url_for('login'))
#----------------------------------------------------------->                
#-----------------------------ststics file------------------->


@app.route('/dashboard_files/<path:path>')
def dashboard_files(path):
    return app.send_static_file(os.path.join('dashboard_files', path))

@app.route('/css/<path:path>')
def css(path):
    return app.send_static_file(os.path.join('css', path))
@app.route('/scss/<path:path>')
def scss(path):
    return app.send_static_file(os.path.join('scss', path))
@app.route('/js/<path:path>')
def js(path):
    return app.send_static_file(os.path.join('js', path))
@app.route('/fonts/<path:path>')
def fonts(path):
    return app.send_static_file(os.path.join('fonts', path))
@app.route('/lib/<path:path>')
def lib(path):
    return app.send_static_file(os.path.join('lib', path))
#------------------------------------------------------------->

@app.route('/google_login')
def google_login():
    access_token = session.get('mail')
    if access_token is  None:
        return redirect(url_for('gmail_profile'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('mail', None)
            return redirect(url_for('gmail_profile'))
        return res.read()
    print res.read()
    return res.read()


@app.route('/gmail_profile')
def gmail_profile():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)




@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    print resp
    access_token = resp['access_token']
    session['mail'] = access_token, ''
    return redirect(url_for('dashboard'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
#-------------ADMIN----->
@app.route('/admin')
def admin():
    if "admin" in session:
        return redirect(url_for("users_detail"))
    else:
        return render_template("admin.html")
@app.route('/admin_login', methods=['POST','get'])
def admin_login():
    if "admin" in session:
        #print"login"
        return redirect(url_for("users_detail"))
    elif request.method=='POST':
        data_dict=request.form.to_dict()
        print data_dict
        user_name=str(request.form['mail'])
        password=str(request.form['password'])
        #print user_name,password
        #email_check=login_handler().email()
        service_obj=services()
        temp=service_obj.validate_admin(user_name,password)
        print temp 
        if(str(temp)=='valid'):
            session['admin'] = request.form['mail']
            return '%s' % temp
        #return render_template("dashboard.html")
    else:
        return redirect(url_for("admin"))
@app.route('/users_detail')
def users_detail():
    if "admin" in session:
        if request.method=='GET':
            return render_template("users_detail.html")
    else:
        return redirect(url_for("admin"))

@app.route('/users_data', methods=['POST','get'])
def users_data():
    if "admin" in session:
        service_obj=services()
        user_data=service_obj.user_data()
        print user_data
        return "%s" % str(user_data)
    else:
        return redirect(url_for("admin"))
@app.route('/delete_user', methods=['POST','get'])
def delete_user():
    if "admin" in session:
        if request.method=="GET":
            username = str(request.args.get('username'))
            service_obj=services()
            del_done=service_obj.delete_user(username)
            return redirect(url_for("users_detail"))
    else:
        return redirect(url_for("admin"))
@app.route('/update_user',methods=['POST','GET'])
def update_user():
    if "admin" in session:
        username = str(request.args.get('username'))
        read = str(request.args.get('read'))
        write = str(request.args.get('write'))
        delete = str(request.args.get('delete'))
        print read,write,delete
        service_obj=services()
        sign_done=service_obj.update_user(username,read,write,delete)
        return redirect(url_for("users_detail"))
    else:
        return redirect(url_for("admin"))
@app.route('/admin_logout', methods=['POST','get'])
def admin_logout():
    session.pop('admin',None)
    return redirect(url_for('admin'))
