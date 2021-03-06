import unbxd.api 
import json
from flask import Flask,session, redirect, url_for, escape
from flask import request
from flask import render_template
from flask_oauth import OAuth
from response_handler import *
from exception_handler import *
from services import *
from data_handler import *
import os

app = Flask(__name__)

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
    if "mail" in session:
        return redirect(url_for('dashboard'))
    elif request.method=='GET':
        return render_template("signup.html")
@app.route('/dashboard')
def dashboard():
    if "mail" in session:
        if request.method=='GET':
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
                    print session
                    session.pop('mail', None)
                    return redirect(url_for('login'))
                return res.read()
            print "$$$$$"
            response_text=str(res.read())
            parse_response_text=json.loads(response_text)
            session['gmail']=parse_response_text
            return render_template("box/profile.html",response=parse_response_text)
    else:
        return redirect(url_for("login"))

@app.route('/simple_login')
def simple_login():
    if "mail" in session:
        return render_template("box/simple_login.html",response=session.get('gmail',"not set"));
    else:
        return redirect(url_for('login'))

@app.route('/signin_data', methods=['POST','get'])
def signin_data():
    if "mail" in session:
        return redirect(url_for('dashboard'))
        #print"login"
    elif request.method=='POST':
        data_dict=request.form.to_dict()
        print data_dict
        user_name=str(request.form['mail'])
        password=str(request.form['password'])
        #print user_name,password
        #email_check=login_handler().email()
        service_obj=services()
        sign_done=service_obj.insert(user_name,password)
        #print email_check
        session['mail'] = request.form['mail']
        session['gmail']=str('NO')
        #Sprint session['mail'] 
        return '%s' % sign_done
    return render_template("unbxd_suggestion.html") 
#------------------------------------------------------------->
#--------------------------all unbxd suggestion--------------->       
@app.route('/unbxd_suggestion')
def unbxd_sugestion():
    if "mail" in session:
        return redirect(url_for('dashboard'))
        print"login"
        if request.method=='GET':
            return render_template("unbxd_suggestion.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

#-------------------------------------------------------------------------------------------------------------------->
@app.route('/all_unbxd_suggestion', methods=['POST','get'])
def all_unbxd_suggestion():
    if "mail" in session:
        try:
            if request.method=='POST':
                message=request.form['command']
                print message
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.all_unbxd_suggestion(message))
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.unbxdsuggestion.all(data=handler_data)
                    response_text_json=json.loads(products)
                    print response_text_json
                    #print str(asd['popularProductFields'][0])
                    #print(len(response_text_json['popularProductFields']))
                    if (type(response_text_json['keywordSuggestions']) is list):
                        response_text=''
                        fld_name=''
                        for val in response_text_json['keywordSuggestions']:
                            #print val
                            field_name=(val['fields'])
                            for values in field_name:
                                fld_name=fld_name+'>'+str(values)
                            #print type(field_name)
                            flds=str(val['name'])
                            response_text=response_text+(flds+"--->"+fld_name+" ")
                            fld_name=''
                            #print response_text
                        return '%s' % response_text
                    else:
                        #print response_text
                        return '%s' % response_text_json['errors'][0]['message']
                else:
                    return render_template("dashboard.html")
            else:
                render_template("dashboard.html")
               
        except Exception as e:
            print e
            return '%s' % e
        

        #data_object = DAO.DataDAO()
        #data_object.save_message(processed_text)
    else:    
        return redirect(url_for("login"))
#-------------------------------------------------------------->
#--------------------------all infield ------------------------>
@app.route('/all_infield')
def all_infield():
    if "mail" in session:
        if request.method=='GET':
            return render_template("get_all_infield.html")
    else:
        return redirect(url_for("login"))  
@app.route('/metric_type')
def metric_type():
    if "mail" in session:
        #if request.method=='POST':
        z = str(request.args.get('data'))
        s=z.replace("_"," ")
        return render_template("box/param.html",response=s,response_text=session)
    else:
        return redirect(url_for("login"))        
@app.route('/get_all_infield_data', methods=['POST','get'])
def get_all_infield_data():
    if "mail" in session:
        try:
            if request.method=='POST':
                message=request.form['command']
                #print message
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.get_all_infield(message))
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.infield.all(data=handler_data)
                    response_text_json=json.loads(products)
                    #print str(asd['popularProductFields'][0])
                    #print(len(response_text_json['popularProductFields']))
                    if (type(response_text_json['inFields']) is list):
                        response_text=''
                        if (len(response_text_json['inFields']) > 0 ):
                            print response_text_json
                            for val in response_text_json['inFields']:
                                #print val
                                fields=str(val)
                                response_text=response_text+(fields+" ")
                            print response_text
                            return render_template("box/table.html",response_text=response_text)
                        else:
                            response_text="infield_list_is_empty *_*"
                            return render_template("box/error.html",response_text=response_text)
                    else:
                        return render_template("box/error.html",response_text=response_text_json['errors'][0]['message'])
                else:
                    return render_template("unbxd_sugestion.html")
            else:
                render_template("unbxd_sugestion.html")
               
        except:
            render_template("login.html")
        

        #data_object = DAO.DataDAO()
        #data_object.save_message(processed_text)
    else:    
        return redirect(url_for("login"))
#-------------------------------------------------------------->
#--------------------------add suggestion --------------------->
@app.route('/add_suggestions')
def add_suggestions():
    if "mail" in session:
        if request.method=='GET':
            return render_template("add_unbxd_suggestion.html")
    else:
        return redirect(url_for("login"))
@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    if "mail" in session:
        try:
            if request.method=='POST':
                print "add suggestion"
                data_dict=request.form.to_dict()
                keylist = data_dict.keys()
                print keylist
                message=str(data_dict["command"])
                data=str(data_dict["data"])
                print message,data
                data=str(data[1:])
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.add_unbxd_suggestion(message,data))
                    print handler_data
                    
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.unbxdsuggestion.update(data=handler_data)
                    res_popular=response_handler()
                    final_message=str(res_popular.addSuggestion(products))
                    #return '%s' % final_message
                    #print products
                    return '%s' % final_message
                    
                else:
                    return render_template("dashboard.html")
                '''
            else:
                return render_template("dashboard.html")
               
        except Exception as e:
            print e
            return '%s' % "error"
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
            if request.method=='POST':
                print ("2")
                data_dict=request.form.to_dict()
                print data_dict
                message=str(request.form['command'])
                print messagedele
                field=str(request.form['data'])
                
                '''
                field=field.split('--->')
                field=field[0]
                '''
                print message,field
                
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.delete_unbxd_suggestion(message,field))
                    #print handler_data
                    #api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    #products=api.unbxdsuggestion.delete(data=handler_data)
                    #res_popular=response_handler()
                    #final_message=str(res_popular.delSuggestion(products))
                    return '%s' % "final_message"
                    #print products
                    

                else:
                    return render_template("dashboard.html")
                
            else:
                return render_template("dashboard.html")
               
        except:
            return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))        

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------add popular product -------------->
@app.route('/add_popular_product')
def add_popular_product():
    if "mail" in session:
        if request.method=='GET':
            return render_template("add_popular_product.html")
    else:
        return redirect(url_for("login"))
@app.route('/add_popular', methods=['POST','get'])
def add_popular():
    if "mail" in session:
        try:
            if request.method=='POST':
                #print "1"
                data_dict=request.form.to_dict()
                #print data_dict
                keylist = data_dict.keys()
                message=str(data_dict["command"])
                field=str(data_dict['fields'])
                condition=str(request.form['condition'])
                #print field,message,condition
                '''
                values=[]
                for val in keylist:
                    if(val[0:6]=="alltxt"):
                        values.append(int(val[6:]))
                values=sorted(values)
                #print values
                string=""
                for param in values:
                    #print param
                    #print str(mydict["mytext"+str(param)])
                    string=string+str(data_dict["mytext"+str(param)])+"_"
                field=string[:-2]
                input_text_list=[]
                for param in values:
                    input_text_list.append(str(data_dict["alltxt"+str(param)]))
                string=""
                for items in input_text_list:
                    if items!="":
                        string=string+str(items)+"_"
                field=string[:-1]
                print field
                #print field,message,condition'''
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.add_popular_product(message,field,condition))
                    #print handler_data
                    handler_true_data=str(handler.all_popular_product(message))
                    #print handler_true_data
                    '''
                    print handler_true_data
                    multiple_true_check=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    resp=str(multiple_true_check.popularproduct.all(data=handler_true_data))
                    print resp
                    res_handler=response_handler()
                    times_true=res_handler.true_check(resp)
                    print type(times_true)'''
                    if (condition=='false'):
                        api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                        products=api.popularproduct.update(data=handler_data)
                        #print products
                        res_popular=response_handler()
                        final_message=str(res_popular.addPopular(products))
                        return '%s' % final_message
                    else:
                        multiple_true_check=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                        resp=str(multiple_true_check.popularproduct.all(data=handler_true_data))
                        #print "resp"
                        #print resp
                        res_handler=response_handler()
                        times_true=res_handler.true_check(resp)
                        #print times_true
                        if(times_true<=0):
                            api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                            products=api.popularproduct.update(data=handler_data)
                            #print products
                            res_popular=response_handler()
                            final_message=str(res_popular.addPopular(products))
                            return '%s' % final_message
                        else:
                            final_message="true already present->change the condition"
                            return '%s' % final_message
                else:
                    return render_template("dashboard.html")
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
            if request.method=='POST':
                #print ("2")
                data_dict=request.form.to_dict()
                
                print "++++++++++"
                print(request)
                print data_dict
                print "++++++++++"
                
                message=str(request.form['command'])
                print message
                try:
                    field=str(request.form['fields'])
                except:
                    field=""
                print message
                print field

                print message,field
                if(field==""):
                    try:
                        flds=str(request.form['data'])
                        #print flds
                        flds=flds.split("--->")
                        #print flds
                        field=flds[0]
                    except:
                        print "send is pressed with empty value"
                if message!="":
                    handler=data_handler()
                    handler_data=(handler.delete_popular_product(message,field))
                    print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=str(api.popularproduct.delete(data=handler_data))
                    #print products
                    #print products
                    res_popular=response_handler()
                    final_message=str(res_popular.delPopular(products))
                    return '%s' % final_message
                else:
                    return render_template("dashboard.html")
            else:
                return render_template("dashboard.html")
               
        except:
            return render_template("dashboard.html")
        

        #data_object = DAO.DataDAO()
        #data_object.save_message(processed_text)
    else:
        return redirect(url_for('login'))    
    #return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------add infield ---------------------->
@app.route('/add_infield')
def add_infield():
    if "mail" in session:
        if request.method=='GET':
            return render_template("add_infield.html")
    else:
        return redirect(url_for('login'))

@app.route('/add_in_field', methods=['POST','get'])
def add_in_field():
    if "mail" in session:
        try:
            #print("alok")
            if request.method=='POST':
                data_dict=request.form.to_dict()
                #print mydict
                field=str(request.form['fields'])
                #keylist = data_dict.keys()
                message=str(data_dict["command"])
                '''
                values=[]
                for val in keylist:
                    if(val[0:6]=="alltxt"):
                        values.append(int(val[6:]))
                values=sorted(values)
                #print values
                string=""
                for param in values:
                    #print param
                    #print str(mydict["mytext"+str(param)])
                    string=string+str(data_dict["alltxt"+str(param)])+"_"
                field=string[:-2]
                #print field
                
                input_text_list=[]
                for param in values:
                    input_text_list.append(str(data_dict["alltxt"+str(param)]))
                string=""
                for items in input_text_list:
                    if items!="":
                        string=string+str(items)+"_"
                field=string[:-1]
                print field'''
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.add_in_field(message,field))
                    #print handler_data
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=api.infield.update(data=handler_data)

                    #print products
                    return '%s' % products
                else:
                    return render_template("dashboard.html")
            else:
                render_template("dashboard.html")
               
        except:
            render_template("dashboard.html")
        

        #data_object = DAO.DataDAO()
        #data_object.save_message(processed_text)
    else:
         return redirect(url_for('login'))   
    #return render_template("dashboard.html")
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
            if request.method=='POST':
               # print ("2")
                data_dict=request.form.to_dict()
                #print mydict
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
            else:
                render_template("dashboard.html")
               
        except:
            render_template("dashboard.html")
    else:        
        return redirect(url_for('login'))
    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")
#------------------------------------------------------------>
#-----------------add popular searchable -------------------->
@app.route('/popular_product')
def popular_product():
    if "mail" in session:
        if request.method=='GET':
            return render_template("popular_product.html")
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
@app.route('/in_field')
def in_field():
    if "mail" in session:
        if request.method=='GET':
            return render_template("infield.html")
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
@app.route('/get_all_popular_product')
def get_all_popular_product():
    if "mail" in session:
        #return redirect(url_for('login'))
        if request.method=='GET':
            return render_template("get_all_popular_product.html")
    else:
         return redirect(url_for('login'))
@app.route('/get_popular_product', methods=['POST','get'])
def get_popular_product():
    if "mail" in session:
        try:
            if request.method=='POST':
                message=request.form['command']
                print message
                if message!="":
                    handler=data_handler()
                    handler_data=str(handler.all_popular_product(message))
                    api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                    products=str(api.popularproduct.all(data=handler_data))
                    #print products


                    response_text_json=json.loads(products)
                    #print str(asd['popularProductFields'][0])
                    #print(len(response_text_json['popularProductFields']))
                    if (type(response_text_json['popularProductFields']) is list):
                        response_text=''
                        for val in response_text_json['popularProductFields']:
                            field_name=str(val['fieldName'])
                            condition=str(val['required'])
                            response_text=response_text+(field_name+"--->"+condition+" ")
                            #print response_text

                        #print response_text
                        return '%s' % response_text
                    else:                  
                        return '%s' % response_text_json['errors'][0]['message']
                else:
                    return render_template("dashboard.html")
            else:
                return render_template("dashboard.html")
               
        except:
            return render_template("dashboard.html")
    else:
        return redirect(url_for('login'))

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

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
                temp=service_obj.check(email)
                #print temp 
                #print data_dict
                return '%s' % temp
            else:
                render_template("dashboard.html")
               
        except:
            render_template("dashboard.html")
    
#------------------------------------------------------------->
#--------------------------all unbxd suggestion---------------> 
@app.route('/login')
def login():
    if "mail" in session:
        return redirect(url_for('display_suggestion'))
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
            session['mail'] = request.form['mail']
            print session['mail']
            print "session mein stor ho gaya"
        return '%s' % temp
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
@app.route('/read_only_data', methods=['POST','get'])
def read_only_data():
    if "mail" in session:                                       
        try:
            if request.method=='POST':
               # print ("2")
                data_dict=request.form.to_dict()
                print "get popular input data"
                print data_dict
                a=services()
                print "1"
                data=a.read_data("alok")
                print "2"
                return '%s' % data
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
               
        except Exception as e:
            return '%s' % e
    else:        
        return redirect(url_for('login'))
    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    #return render_template("dashboard.html")      
#------------------------------------------------------------>
#-----------------------------log out------------------------>
@app.route('/logout', methods=['POST','get'])
def logout():
    session.pop('mail', None)
    session.pop('gmail', None)
    return redirect(url_for('login'))

#------------------------------------------------------------>
#----------------------get index files----------------------->
@app.route('/display_suggestion', methods=['POST','get'])
def display_suggestion():
    if "mail" in session:
        # z=str(request.form['command'])
        company = str(request.args.get('command'))
        metric = str(request.args.get('metric'))
        #print "company id=>"+z
        handler=data_handler()
        if metric=="Suggestion":
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
                print outerlist
                return render_template("box/table.html",response=outerlist ,response_text=session)
        elif metric=="In Field":
            #try:
                if company!="":
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
                            print response_text
                            return render_template("box/infield.html",response_text=response_text)
                        else:
                            response_text=["infield_list_is_empty *_*"]
                            return render_template("box/error.html",response_text=response_text)
                    else:
                        return render_template("box/error.html",response_text=response_text_json['errors'][0]['message'])
                else:
                    return render_template("unbxd_suggestion.html")
            #except:
             #   render_template("unbxd_suggestion.html")'''
        elif metric=="Popular Product":
            if company!="":
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
                        return render_template("box/popular.html",response=outer)
                    else:                  
                        return render_template("box/error.html",response_text=response_text_json['errors'][0]['message'])
        else:
            return render_template("box/error.html",response_text="Enter the required Metric")
    else:
        redirect(url_for('login'))
#------------------------------------------------------------------------->
#------------------------------------------------------------------------->
@app.route('/display_popular', methods=['POST','get'])
def display_popular():
    if "mail" in session:
        # z=str(request.form['command'])
        company = str(request.args.get('command'))
        metric = str(request.args.get('metric'))
        print "company id=>"+z
        handler=data_handler()
        if metric=="Popular Product":
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
                print outerlist
                return render_template("box/table.html",response=outerlist)

    else:
        redirect(url_for('login'))
#------------------------------------------------------------------------->
#------------------------------------------------------------------------->
    
    
@app.route('/get_index_fields', methods=['POST','get'])
def get_index_fields():
    if "mail" in session:                                       
        try:
            if request.method=='POST':
               # print ("2")
                data_dict=request.form.to_dict()
                #print mydict
                message=str(request.form['command'])
                exception_obj=exception_handler()
                handler_data=str(exception_obj.get_index_field(message))
                json_data=json.loads(handler_data)
                string=""
                for item in json_data:
                    string=string+item['fieldName']+" "
                #print string
                #return '%s' % string
                return render_template('/box/table.html',response=string)
        except Exception as e:
            print e
            return '%s' % "select_company"
#----------------------------------------------------------->                
#-----------------------------ststics file------------------->


@app.route('/dashboard_files/<path:path>')
def dashboard_files(path):
    return app.send_static_file(os.path.join('dashboard_files', path))
@app.route('/all_unbxd_suggestion_files/<path:path>')
def all_unbxd_suggestion_files(path):
    return app.send_static_file(os.path.join('all_unbxd_suggestion_files', path))
@app.route('/get_all_infield_files/<path:path>')
def get_all_infield_files(path):
    return app.send_static_file(os.path.join('get_all_infield_files', path))
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