import unbxd.api 
from flask import Flask
from flask import request
from flask import render_template
from services import *
from data_handler import *
import os

app = Flask(__name__)

@app.route('/')
def my_form():
    if request.method=='GET':
        return render_template("dashboard.html")
#------------------------------------------------------------->
#--------------------------all unbxd suggestion--------------->       
@app.route('/all_unbxd')
def all_unbxd():
    if request.method=='GET':
        return render_template("all_unbxd_suggestion.html")
@app.route('/all_unbxd_suggestion', methods=['POST','get'])
def all_unbxd_suggestion():
    try:
        if request.method=='POST':
            message=request.form['command']
            if message!="":
                handler=data_handler()
                handler_data=str(handler.all_unbxd_suggestion(message))
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.unbxdsuggestion.all(data=handler_data)
                return '%s' % products
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
#-------------------------------------------------------------->
#--------------------------all infield ------------------------>
@app.route('/all_infield')
def all_infield():
    if request.method=='GET':
        return render_template("get_all_infield.html")

@app.route('/get_all_infield_data', methods=['POST','get'])
def get_all_infield_data():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                handler=data_handler()
                handler_data=str(handler.get_all_infield(message))
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.infield.all(data=handler_data)
                return '%s' % products
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
#-------------------------------------------------------------->
#--------------------------add suggestion --------------------->
@app.route('/add_suggestions')
def add_suggestions():
    if request.method=='GET':
        return render_template("add_unbxd_suggestion.html")

@app.route('/add_suggestion_data', methods=['POST','get'])
def add_suggestion_data():
    try:
        if request.method=='POST':
            data_dict=request.form.to_dict()
            keylist = data_dict.keys()
            message=str(data_dict["command"])
            values=[]
            for val in keylist:
                if(val[0:6]=="mytext"):
                    values.append(int(val[6:]))
            values=sorted(values)
            string=""
            for param in values:
                #print param
                #print str(data_dict["mytext"+str(param)])
                string=string+str(data_dict["mytext"+str(param)])+"_"
            field=string[:-2]
            if message!="":
                handler=data_handler()
                handler_data=str(handler.add_unbxd_suggestion(message,field))
                #print handler_data
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.unbxdsuggestion.update(data=handler_data)
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

    return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------delete unbxd suggestion ---------->
@app.route('/delete_unbxd_suggestion')
def delete_unbxd_suggestion():
    if request.method=='GET':
        return render_template("delete_unbxd_suggestion.html")
@app.route('/delete_suggestion_data', methods=['POST','get'])
def delete_suggestion_data():
    print("1")
    try:
        if request.method=='POST':
            #print ("2")
            data_dict=request.form.to_dict()
            #print mydict
            message=str(request.form['command'])
            field=str(request.form['fields'])
            #print message,field
            if message!="":
                handler=data_handler()
                handler_data=str(handler.delete_unbxd_suggestion(message,field))
                #print handler_data
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.unbxdsuggestion.delete(data=handler_data)
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

    return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------add popular product -------------->
@app.route('/add_popular_product')
def add_popular_product():
    if request.method=='GET':
        return render_template("add_popular_product.html")
@app.route('/add_popular', methods=['POST','get'])
def add_popular():
    try:
        if request.method=='POST':
            data_dict=request.form.to_dict()
            #print mydict
            keylist = data_dict.keys()
            message=str(data_dict["command"])
            condition=str(data_dict['condition'])
            values=[]
            for val in keylist:
                if(val[0:6]=="mytext"):
                    values.append(int(val[6:]))
            values=sorted(values)
            #print values
            string=""
            for param in values:
                #print param
                #print str(mydict["mytext"+str(param)])
                string=string+str(data_dict["mytext"+str(param)])+"_"
            field=string[:-2]
            #print field,message,condition
            if message!="":
                handler=data_handler()
                handler_data=str(handler.add_popular_product(message,field,condition))
                #print handler_data
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.popularproduct.update(data=handler_data)
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

    return render_template("dashboard.html")
#------------------------------------------------------------>
#---------------------delete popular product ---------------->
@app.route('/delete_popular_product')
def delete_popular_product():
    if request.method=='GET':
        return render_template("delete_popular_product.html")

@app.route('/delete_popular', methods=['POST','get'])
def delete_popular():
    try:
        if request.method=='POST':
            #print ("2")
            data_dict=request.form.to_dict()
            #print mydict
            message=str(request.form['command'])
            field=str(request.form['fields'])
            #print message,field
            if message!="":
                handler=data_handler()
                handler_data=str(handler.delete_popular_product(message,field))
                #print handler_data
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.popularproduct.delete(data=handler_data)
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

    return render_template("dashboard.html")
#------------------------------------------------------------>
#--------------------------add infield ---------------------->
@app.route('/add_infield')
def add_infield():
    if request.method=='GET':
        return render_template("add_infield.html")

@app.route('/add_in_field', methods=['POST','get'])
def add_in_field():
    try:
        #print("alok")
        if request.method=='POST':
            data_dict=request.form.to_dict()
            #print mydict
            keylist = data_dict.keys()
            message=str(data_dict["command"])
            values=[]
            for val in keylist:
                if(val[0:6]=="mytext"):
                    values.append(int(val[6:]))
            values=sorted(values)
            #print values
            string=""
            for param in values:
                #print param
                #print str(mydict["mytext"+str(param)])
                string=string+str(data_dict["mytext"+str(param)])+"_"
            field=string[:-2]
            #print field
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

    return render_template("dashboard.html")
#------------------------------------------------------------->
#--------------------------delete infield -------------------->
@app.route('/delete_infield')
def delete_infield():
    if request.method=='GET':
        return render_template("delete_infield.html")
@app.route('/delete_in_field', methods=['POST','get'])
def delete_in_field():
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
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
#------------------------------------------------------------>
#-----------------add popular searchable -------------------->
@app.route('/add_popular_searchable_field')
def add_popular_searchable_field():
    if request.method=='GET':
        return render_template("add_popular_product_searchable_field.html")
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
    if request.method=='GET':
        return render_template("delete_popular_product_searchable_field.html")
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
@app.route('/view_popular_searchable_field')
def view_popular_searchable_field():
    if request.method=='GET':
        return render_template("view_popular_product_searchable_field.html")
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
    if request.method=='GET':
        return render_template("send_autosuggest_data.html")
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
    if request.method=='GET':
        return render_template("get_all_popular_product.html")
@app.route('/get_popular_product', methods=['POST','get'])
def get_popular_product():
    try:
        if request.method=='POST':
            message=request.form['command']
            #print message
            if message!="":
                handler=data_handler()
                handler_data=str(handler.all_popular_product(message))
                api=unbxd.api.PostmanApi(host="feed.unbxdapi.com")
                products=api.popularproduct.all(data=handler_data)
                return '%s' % products
            else:
                return render_template("dashboard.html")
        else:
            render_template("dashboard.html")
           
    except:
        render_template("dashboard.html")
    

    #data_object = DAO.DataDAO()
    #data_object.save_message(processed_text)

    return render_template("dashboard.html")
#------------------------------------------------------------>
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
#------------------------------------------------------------->