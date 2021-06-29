from flask import   request, jsonify
from api import app, db, bcrypt
from api import json
import datetime
from api.models import User, CourtCase, SlotList
from flask_login import login_user, current_user, logout_user, login_required
import flask
from flask_cors import cross_origin

import os

if(not 'site.db' in os.listdir('./api')):
    db.create_all()
    user = User(name="Registrar", username="registrar",
                password=bcrypt.generate_password_hash('reg1234').decode('utf-8'), address="Kolkata", user_type="Registrar")
    db.session.add(user)
    db.session.commit()
# ************Functions****************


def resolved_case_list(jsonobj):
    ret_dict = {}
    try:
        y = jsonobj
        beg_date = datetime.datetime(int(y["beg_date"]["year"]), int(
            y["beg_date"]["month"]), int(y["beg_date"]["day"]))
        end_date = datetime.datetime(int(y["end_date"]["year"]), int(
            y["end_date"]["month"]), int(y["end_date"]["day"]))
        record = CourtCase.query.filter(CourtCase.starting_date.between(
            beg_date, end_date)).filter_by(is_closed=True).order_by(CourtCase.starting_date).all()
        ret_dict["confirm"] = 1
        ret_dict["case_list"] = []
        for i in record:
            temp_dict = {}
            temp_dict['cin'] = i.cin
            temp_dict['name_pres_judge'] = i.judge_name
            temp_dict['starting_date'] = {}
            temp_dict['starting_date']['month'] = str(i.starting_date.month)
            temp_dict['starting_date']['day'] = str(i.starting_date.day)
            temp_dict['starting_date']['year'] = str(i.starting_date.year)
            temp_dict['latest_date'] = {}
            temp_dict['latest_date']['month'] = str(i.hearing_date.month)
            temp_dict['latest_date']['day'] = str(i.hearing_date.day)
            temp_dict['latest_date']['year'] = str(i.hearing_date.year)
            temp_dict['case_summary'] = i.summary
            ret_dict["case_list"].append(temp_dict)
    except:
        db.session.rollback()
        ret_dict["confirm"] = "0"
        ret_dict["message"] = "Sorry!! There was a problem in viewing the resolved case list!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


def search_by_key(key, username):
    try:
        search_by_key_charge = 200
        record = User.query.filter_by(username=username).first()
        ret_dict = {}
        if record is None:
            ret_dict2 = {}
            ret_dict2["confirm"] = "0"
            ret_dict2["message"] = "Please enter a valid username!!"
            ret_json2 = json.dumps(ret_dict2)
            return ret_json2
        else:
            if record.user_type == 'Lawyer':
                record.due_amount = record.due_amount + search_by_key_charge
                db.session.commit()
                ret_dict['due_amt'] = str(record.due_amount)
            rec = CourtCase.query.all()
            ret_dict["confirm"] = "1"
            ret_dict["message"] = "The search was successful!!"
            ret_dict['cin_list'] = []
            for i in rec:
                if i.is_closed==True:
                    str_row = ""
                    str_row = str_row + i.defendent_name + " " + i.defendent_address + " " + i.judge_name + " " + i.crime_type + \
                        " " + i.crime_location + " " + i.arresting_officer_name + \
                        " " + i.public_prosecutor_name + " "
                    if i.hearing_details is not None:
                        str_row = str_row + i.hearing_details
                    if i.summary is not None:
                        str_row = str_row + i.summary
                    if key in str_row:
                        temp_dict = {}
                        temp_dict['cin'] = i.cin
                        temp_dict['crime_type'] = i.crime_type
                        temp_dict['name_pres_judge'] = i.judge_name
                        temp_dict['start_date'] = str(
                            i.starting_date.day)+"-"+str(i.starting_date.month)+"-"+str(i.starting_date.year)
                        ret_dict['cin_list'].append(temp_dict)
                ret_json = json.dumps(ret_dict)
            return ret_json
    except:
        db.session.rollback()
        return json.dumps({"confirm": "0", "message": "Some Error occured"})


def search_by_id(cin_str, username):
    try:
        search_by_id_charge = 100
        ret_dict = {}
        ret_dict['due_amt'] = "0"
        cin = int(cin_str)
        i = CourtCase.query.get(cin)
        if i is None:
            ret_dict["confirm"] = "0"
            ret_dict["message"] = "Please search for a valid CIN number!!"
        elif i.is_closed!=True:
            ret_dict["confirm"] = "0"
            ret_dict["message"] = "This is a pending Case!!"
        else:
            ret_dict['case_details'] = {}
            ret_dict['case_details']['CIN'] = str(i.cin)
            ret_dict['case_details']['def_name'] = i.defendent_name
            ret_dict['case_details']['def_addr'] = i.defendent_address
            ret_dict['case_details']['crime_type'] = i.crime_type
            ret_dict['case_details']['crime_date'] = str(
                i.crime_date.day)+"-"+str(i.crime_date.month)+"-"+str(i.crime_date.year)
            ret_dict['case_details']['date_arrest'] = str(
                i.date_of_arrest.day)+"-"+str(i.date_of_arrest.month)+"-"+str(i.date_of_arrest.year)
            ret_dict['case_details']['start_date'] = str(
                i.starting_date.day)+"-"+str(i.starting_date.month)+"-"+str(i.starting_date.year)
            ret_dict['case_details']['latest_hearing_date'] = str(
                i.hearing_date.day)+"-"+str(i.hearing_date.month)+"-"+str(i.hearing_date.year)
            ret_dict['case_details']['expected_completion_date'] = str(
                i.expected_completion_date.day)+"-"+str(i.expected_completion_date.month)+"-"+str(i.expected_completion_date.year)
            ret_dict['case_details']['crime_loc'] = i.crime_location
            ret_dict['case_details']['arresting_off_name'] = i.arresting_officer_name
            ret_dict['case_details']['name_pres_judge'] = i.judge_name
            ret_dict['case_details']['pros_name'] = i.public_prosecutor_name
            ret_dict['case_details']['adj_details'] = []
            adj = i.hearing_details
            if adj is not None:
                for x in adj.split('|'):
                    jobj = json.loads(x)
                    temp_dict = {}
                    temp_dict["date"] = jobj["date"]
                    temp_dict["reason"] = jobj["reason"]
                    ret_dict['case_details']['adj_details'].append(temp_dict)
            record = User.query.filter_by(username=username).first()
            if record is None:
                ret_dict2 = {}
                ret_dict2["confirm"] = "0"
                ret_dict2["messaage"] = "Please enter a valid username!!"
                ret_json2 = json.dumps(ret_dict2)
                return ret_json2
            else:
                if record.user_type == 'Lawyer':
                    record.due_amount = record.due_amount + search_by_id_charge
                    db.session.commit()
                    ret_dict['due_amt'] = str(record.due_amount)
        ret_json = json.dumps(ret_dict)
        return ret_json
    except:
        db.session.rollback()
        return json.dumps({"confirm": "0", "message": "Some Error occured"})


def court_cases_by_date(json_obj):
    ret_dict = {}
    try:
        y = json_obj
        query_date = datetime.datetime(int(y["query_date"]["year"]), int(
            y["query_date"]["month"]), int(y["query_date"]["day"]))
        record = CourtCase.query.filter_by(
            hearing_date=query_date, is_closed=False).all()
        ret_dict['confirm'] = "1"
        ret_dict['case_list'] = []
        for i in record:
            temp_dict = {}
            temp_dict['cin'] = str(i.cin)
            temp_dict['slot'] = i.hearing_slot
            temp_dict['name_pres_judge'] = i.judge_name
            temp_dict['crime_type'] = i.crime_type
            ret_dict['case_list'].append(temp_dict)
    except:
        db.session.rollback()
        ret_dict["confirm"] = "0"
        ret_dict["message"] = "Sorry!! There was a issue with the date!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


def case_status_query(json_obj):
    ret_dict = {}
    try:
        y = json_obj
        cin = int(y['cin'])
        record = CourtCase.query.get(cin)
        if record is None:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "The input CIN does not exist!!"
        else:
            ret_dict['confirm'] = "1"
            ret_dict["message"] = "Success!!!"
            if record.is_closed == True:
                ret_dict["case_status"] = "Resolved"
            else:
                ret_dict["case_status"] = "Pending"
    except:
        db.session.rollback()
        ret_dict["confirm"] = "0"
        ret_dict["message"] = "Sorry!There was a problem in the query!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


def unresolved_case_list():
    try:
        record = CourtCase.query.filter_by(is_closed=False).all()
        ret_dict = {}
        ret_dict['confirm'] = '1'
        ret_dict['case_list'] = []
        for i in record:
            temp_dict = {}
            temp_dict['cin'] = str(i.cin)
            temp_dict['def_name'] = i.defendent_name
            temp_dict['def_addr'] = i.defendent_address
            temp_dict['crime_type'] = i.crime_type
            temp_dict['crime_date'] = {}
            temp_dict['crime_date']['month'] = str(i.crime_date.month)
            temp_dict['crime_date']['day'] = str(i.crime_date.day)
            temp_dict['crime_date']['year'] = str(i.crime_date.year)
            temp_dict['arrest_date'] = {}
            temp_dict['arrest_date']['month'] = str(i.date_of_arrest.month)
            temp_dict['arrest_date']['day'] = str(i.date_of_arrest.day)
            temp_dict['arrest_date']['year'] = str(i.date_of_arrest.year)
            temp_dict['starting_date'] = {}
            temp_dict['starting_date']['month'] = str(i.starting_date.month)
            temp_dict['starting_date']['day'] = str(i.starting_date.day)
            temp_dict['starting_date']['year'] = str(i.starting_date.year)
            temp_dict['crime_loc'] = i.crime_location
            temp_dict['arresting_off_name'] = i.arresting_officer_name
            temp_dict['name_pres_judge'] = i.judge_name
            temp_dict['public_prosecutor_name'] = i.public_prosecutor_name
            ret_dict['case_list'].append(temp_dict)
        ret_json = json.dumps(ret_dict)
        return ret_json
    except:
        db.session.rollback()
        return json.dumps({"confirm": "0", "message": "Some Error occured"})


def schedule_case(jsonobj):
    ret_dict = {}
    #try:
    y = jsonobj
    cin = int(y['cin'])
    slot = int(y['slot'])
    new_hearing_date = datetime.datetime(
        int(y["date"]["year"]), int(y["date"]["month"]), int(y["date"]["day"]))
    record = CourtCase.query.filter_by(cin=cin).first()
    if record is None:
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "The given CIN does not exist!!"
    elif record.hearing_date and record.hearing_date >= new_hearing_date:
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "The new hearing date cannot be older than the previous one!!"
    else:
        record.hearing_date = new_hearing_date

        record.hearing_slot = slot
        db.session.commit()
        #print(record.hearing_date)  # DEBUG
        add_to_slotlist(cin, slot, record.hearing_date.year,
                        record.hearing_date.month, record.hearing_date.day)

        ret_dict['confirm'] = "1"
        ret_dict["message"] = "New hearing date assigned successfully!!"
    '''
    except:
        db.session.rollback()
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "There was a problem assigning a new hearing date!"
    '''
    ret_json = json.dumps(ret_dict)
    return ret_json


def adjournment_details_add(jsonobj):
    ret_dict = {}
    try:
        y = jsonobj
        cin = int(y['cin'])
        reason = y['reason']
        record = CourtCase.query.filter_by(cin=cin).first()
        if record is None:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "The entered CIN is invalid!!"
        elif record.is_closed == True:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "The case has already been closed!!"
        elif record.hearing_date <= record.latest_adjournment_date:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "Please assign the next hearing of the case!"
        else:
            adj_dict = {}
            adj_dict["date"] = str(record.hearing_date.day)+"-"+str(
                record.hearing_date.month)+"-"+str(record.hearing_date.year)
            adj_dict["reason"] = reason
            adj_json = json.dumps(adj_dict)
            record.latest_adjournment_date = record.hearing_date
            record.latest_adjournment_slot = record.hearing_slot
            if record.hearing_details is None:
                record.hearing_details = adj_json
            else:
                record.hearing_details = record.hearing_details + "|" + adj_json
            db.session.commit()
            ret_dict['confirm'] = "1"
            ret_dict['message'] = "Adjournment details added successfully!!"
    except:
        db.session.rollback()
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "There was some problem closing the case!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


'''
0 if not vacant
1 if vacant
'''


def search_vacant_slot(jsonobj):
    ret_dict = {}
    try:
        y = jsonobj
        date = datetime.datetime(int(y["year"]), int(y["month"]), int(y["day"]))
        list_of_case = SlotList.query.filter_by(date_of_hearing=date).all()
        slot_list = ['1', '1', '1', '1', '1']
        for i in list_of_case:
            slot_list[i.slot_of_hearing-1] = '0'
        ret_dict['free_slot'] = {}
        ret_dict['free_slot']['slot1'] = slot_list[0]
        ret_dict['free_slot']['slot2'] = slot_list[1]
        ret_dict['free_slot']['slot3'] = slot_list[2]
        ret_dict['free_slot']['slot4'] = slot_list[3]
        ret_dict['free_slot']['slot5'] = slot_list[4]
        ret_dict["confirm"] = "1"
        ret_dict["message"] = "Success!!!"
    except:
        db.session.rollback()
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "Sorry!! There was a problem in finding the vacant slots!!"
    ret_val = json.dumps(ret_dict)
    return ret_val


def add_to_slotlist(cin, slot, year, month, date):
    try:
        slotadd = SlotList(cin=cin, slot_of_hearing=slot,
                        date_of_hearing=datetime.datetime(year, month, date))
        db.session.add(slotadd)
        db.session.commit()
    except:
        db.session.rollback()


def enter_details_into_db(jsonobj):
    try:
    
        y = jsonobj
        def_name = y["def_name"]
        def_addr = y["def_addr"]
        crime_type = y["crime_type"]
        crime_date = datetime.datetime(int(y["crime_date"]["year"]), int(
            y["crime_date"]["month"]), int(y["crime_date"]["day"]))
        crime_loc = y["crime_loc"]
        arresting_off_name = y["arresting_off_name"]
        arrest_date = datetime.datetime(int(y["arrest_date"]["year"]), int(
            y["arrest_date"]["month"]), int(y["arrest_date"]["day"]))
        name_pres_judge = y["name_pres_judge"]
        pub_pros_name = y["public_prosecutor_name"]
        starting_date = datetime.datetime(int(y["starting_date"]["year"]), int(
            y["starting_date"]["month"]), int(y["starting_date"]["day"]))
        expected_completion_date = datetime.datetime(int(y["expected_completion_date"]["year"]), int(
            y["expected_completion_date"]["month"]), int(y["expected_completion_date"]["day"]))
        if int(y["hearing_slot"]) != -1:
            hearing_date = datetime.datetime(int(y["hearing_date"]["year"]), int(
                y["hearing_date"]["month"]), int(y["hearing_date"]["day"]))
            hearing_slot = y["hearing_slot"]
            case = CourtCase(defendent_name=def_name, defendent_address=def_addr, crime_type=crime_type, crime_date=crime_date, crime_location=crime_loc, arresting_officer_name=arresting_off_name, date_of_arrest=arrest_date,
                             judge_name=name_pres_judge, public_prosecutor_name=pub_pros_name, starting_date=starting_date, expected_completion_date=expected_completion_date, hearing_date=hearing_date, hearing_slot=hearing_slot)
        else:
            case = CourtCase(defendent_name=def_name, defendent_address=def_addr, crime_type=crime_type, crime_date=crime_date, crime_location=crime_loc, arresting_officer_name=arresting_off_name,
                             date_of_arrest=arrest_date, judge_name=name_pres_judge, public_prosecutor_name=pub_pros_name, starting_date=starting_date, expected_completion_date=expected_completion_date)
        db.session.add(case)
        db.session.commit()
        if int(y["hearing_slot"]) != -1:
            add_to_slotlist(case.cin, case.hearing_slot, case.hearing_date.year,
                            case.hearing_date.month, case.hearing_date.day)
        data_ret = {}
        data_ret['is_added'] = "1"
        data_ret['cin'] = str(case.cin)
        data_ret['message'] = "The Case has been added successfully!!"
        json_data_ret = json.dumps(data_ret)
        return json_data_ret
    except:
        db.session.rollback()
        data_ret = {}
        data_ret['is_added'] = "0"
        data_ret['message'] = "Sorry!! There was a problem adding the Case !!"
        json_data_ret = json.dumps(data_ret)
        return json_data_ret


def get_user_list():
    ret_dict = {}
    try:
        ret_dict['usr_list'] = []
        recr = User.query.all()
        for i in recr:
            if i.user_type != "Registrar":
                dct = {}
                dct['username'] = i.username
                dct['name'] = i.name
                dct['usr_type'] = i.user_type
                ret_dict['usr_list'].append(dct)
        ret_dict['confirm'] = "1"
        ret_dict['message'] = "Success!! Here is the list of users!!"
    except:
        db.session.rollback()
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "Sorry!!There was a problem getting the user list!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


def close_case(json_obj):
    ret_dict = {}
    try:
        y = json_obj
        cin = int(y['cin'])
        summary = y['case_summary']
        record = CourtCase.query.filter_by(cin=cin).first()
        if record is None:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "Sorry!! The given CIN does not exist!!"
        elif record.is_closed == True:
            ret_dict['confirm'] = "0"
            ret_dict['message'] = "The case has already been closed!!"
        else:
            record.is_closed = True
            record.summary = summary
            db.session.commit()
            ret_dict['confirm'] = "1"
            ret_dict['message'] = "The case has been successfully closed!!"
    except:
        db.session.rollback()
        ret_dict['confirm'] = "0"
        ret_dict['message'] = "There was some problem closing the case!!"
    ret_json = json.dumps(ret_dict)
    return ret_json


def add_lawyer_judge(json_obj):
    try:
        y = json_obj
        user_type = y['usr_type']
        username = y["username"]
        name = y["name"]
        passw = y["password"]
        address = y['usr_addr']
        hashed_password = bcrypt.generate_password_hash(passw).decode('utf-8')
        usr = User.query.filter_by(username=username).first()
        if(usr):
            return json.dumps({"add_status": "0", "err_msg": "Username Already Exists"})
        user = User(username=username, address=address, name=name,
                    password=hashed_password, user_type=user_type)

        db.session.add(user)
        db.session.commit()
        ret_val = {}
        ret_val['add_status'] = "1"
        ret_val['err_msg'] = "The account of has been created successfully!!"
        ret_json = json.dumps(ret_val)
        return ret_json

    except:
        db.session.rollback()
        ret_val = {}
        ret_val['add_status'] = "0"
        ret_val['err_msg'] = "Sorry!!We were unable to create the account!! The username probably exists !!"
        ret_json = json.dumps(ret_val)
        return ret_json


def remove_lawyer_judge(json_obj):
    ret_dict = {}
    try:
        y = json_obj
        username = y["username"]
        recr = User.query.filter_by(username=username).first()
        if recr is None:
            ret_dict['removed_status'] = "0"
            ret_dict['err_msg'] = "Sorry!! The username does not exist!!"
        else:
            db.session.delete(recr)
            db.session.commit()
            ret_dict['removed_status'] = "1"
            ret_dict['err_msg'] = "Username removed successfully!!"
    except:
        db.session.rollback()
        ret_dict['removed_status'] = "0"
        ret_dict['err_msg'] = "Sorry!!There was some problem !!"
    ret_json = json.dumps(ret_dict)
    return ret_json


# ************Routes********************


@ app.route("/api/isLoggedIn", methods=['GET', 'POST'])
def isLoggedIn():
    if current_user.is_authenticated:
        print('Logged INN')
        return jsonify({'login_status': '1', 'user_type': current_user.user_type, 'nameofuser': current_user.name, 'due_amt': current_user.due_amount})
    else:
        return {'login_status': '0'}


@ app.route("/api/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('Logged In')
        if current_user.user_type == 'Lawyer':
            return jsonify({'login_status': '1', 'user_type': current_user.user_type, 'nameofuser': current_user.name, 'due_amt': current_user.due_amount})
        return jsonify({'login_status': '1', 'user_type': current_user.user_type, 'nameofuser': current_user.name})
    if(flask.request.method == 'POST'):
        print('POST method')
        print(flask.request.values)
        print(flask.request.get_json())
        req = flask.request.get_json()
        username_data = req.get('username')
        print(username_data)
        password = req.get('password')
        print(password)
        user = User.query.filter_by(username=username_data).first()
        print(user)
       # print(user.password)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            print('Login Successful')
            print('Current User ', current_user)
            if current_user.user_type == 'Lawyer':
                return jsonify({'login_status': '1', 'user_type': user.user_type, 'nameofuser': user.name, 'due_amt': current_user.due_amount})
            return jsonify({'login_status': '1', 'user_type': user.user_type, 'nameofuser': user.name})
        else:
            print('Login Unsuccessful. Please check username and password')
    # login_user(user, remember=form.remember.data)
    return jsonify({'login_status': "0"})


@ app.route("/api/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    print("Logged Out")
    return {"logout_status": "1"}


@ app.route("/api/searchbyKey", methods=['GET', 'POST'])
@ login_required
def searchbyKey():
    '''
    Returns List of Cins
    param : {'key':'Key'}
    returns:
    {'cin_list':[{'cin':'<CIN>','crime_type':'<crime_type>'},...]}
    '''
    # do differently for usertype = judge and lawyer
    print(flask.request.get_json())
    return search_by_key(flask.request.get_json()['key'], current_user.username)
    '''
    return {'cin_list': [{'cin': '1', 'crime_type': 'theft'}, {'cin': '2', 'crime_type': 'theft'}],
            'due_amt': '0'}
'''


@ app.route("/api/addUser", methods=['GET', 'POST'])
@ login_required
def addUser():
    print(flask.request.get_json())
    # Check forcurrent user return Error if not Registrar
    print('Adding User')
    return add_lawyer_judge(flask.request.get_json())
    # return {'add_status': '1'}


@ app.route("/api/addAdjournmentSummary", methods=['GET', 'POST'])
@ login_required
def addAdjournmentSummary():
    print(flask.request.get_json())
    # Check forcurrent user return Error if not Registrar
    print('Adding Adjournment Details')
    return adjournment_details_add(flask.request.get_json())
    # return {'confirm': '1', 'message': 'Success'}


@ app.route("/api/queryStatus", methods=['GET', 'POST'])
@ login_required
def queryStatus():
    print(flask.request.get_json())
    # Check forcurrent user return Error if not Registrar
    print('Query Status')
    return case_status_query(flask.request.get_json())
    # return {'confirm': '1', 'case_status': 'Resolved', 'message': 'Success'}
    # return {'confirm':'0','message':'CIN doesnt exist'}


@ app.route("/api/removeUser", methods=['GET', 'POST'])
@ login_required
def removeUser():
    print(flask.request.get_json())
    # Check forcurrent user return Error if not Registrar
    print('Removing User')
    return remove_lawyer_judge(flask.request.get_json())
    # return {'remove_status': '1'}


@ app.route("/api/addCase", methods=['GET', 'POST'])
@ login_required
def addCase():
    print('Adding Case')
    print(flask.request.get_json())
    return enter_details_into_db(flask.request.get_json())
    # return {"is_added": "1", "cin": "3", "message": "The Case has been added successfully!!"}


@ app.route("/api/getPendingCase", methods=['GET'])
@ login_required
def getPendingCase():
    print(flask.request.get_json())
    return unresolved_case_list()
    '''
    return {
        "case_list": [
            {
                "cin": "1",
                "def_name": "A",
                "def_addr": "sdff",
                "crime_type": "theft",
                "crime_date": {"month": "4", "year": "2020", "day": "15"},
                "crime_loc": "Kolkata ",
                "arresting_off_name": " Ram",
                "arrest_date": {"month": "5", "year": "2020", "day": "15"},
                "name_pres_judge": "J.Kabir",
                "public_prosecutor_name": "Altim ",
                "starting_date": {"month": "4", "year": "2020", "day": "20"}
            },
            {
                "cin": "3",
                "def_name": "A",
                "def_addr": "sdff",
                "crime_type": "theft",
                "crime_date": {"month": "4", "year": "2020", "day": "15"},
                "crime_loc": "Kolkata ",
                "arresting_off_name": " Ram",
                "arrest_date": {"month": "5", "year": "2020", "day": "15"},
                "name_pres_judge": "J.Kabir",
                "public_prosecutor_name": "Altim ",
                "starting_date": {"month": "4", "year": "2020", "day": "20"}
            }
        ]
    }

'''


@ app.route("/api/queryResolved", methods=['GET', 'POST'])
@ login_required
def queryResolved():
    print(flask.request.get_json())
    return resolved_case_list(flask.request.get_json())
    '''
    return {
        "confirm": "1",
        "case_list": [
            {
                "cin": "1",
                "starting_date": {
                    "day": "1",
                    "month": "1",
                    "year": "2020"
                },
                "name_pres_judge": "J",
                "case_summary": "Jail"

            },
            {
                "cin": "1",
                "starting_date": {
                    "day": "5",
                    "month": "1",
                    "year": "2020"
                },
                "name_pres_judge": "J",
                "case_summary": "Jail"

            }
        ]
    }
'''


@ app.route("/api/queryUpcomingByDate", methods=['GET', 'POST'])
@ login_required
def queryUpcomingByDate():
    print(flask.request.get_json())
    return court_cases_by_date(flask.request.get_json())
    '''
    return {
        "confirm": "1",
        "case_list": [
            {
                "cin": "1",
                "slot": "1",
                "name_pres_judge": "J",
                "crime_type": "Theft"

            },
            {
                "cin": "2",
                "slot": "2",
                "name_pres_judge": "J",
                "crime_type": "Theft"

            }
        ]
    }

'''


@ app.route("/api/getUserList", methods=['GET'])
@ login_required
def getUserList():
    print(flask.request.get_json())
    print('First USe')
    return get_user_list()
    # return {'usr_list': [{'username': 'j1', 'name': 'Judge1', 'usr_type': 'Judge'}]}

# GETSLOT


@ app.route("/api/queryFreeSlot", methods=['GET', 'POST'])
@ login_required
def queryFreeSlot():
    print(flask.request.get_json())
    return search_vacant_slot(flask.request.get_json())
    # return {'free_slot': {'slot1': '1', 'slot2': '1', 'slot3': '0', 'slot4': '1', 'slot5': '0'}}


@ app.route("/api/searchbyId", methods=['GET', 'POST'])
@ login_required
def searchbyId():
    '''
    param : {'cin':'id'}
    '''
    # do differently for usertype = judge and lawyer
    print('Search by id')
    req = flask.request.get_json()
    print(req)
    return search_by_id(req['cin'], current_user.username)
    '''
    if(req.get('cin') == '1'):
        return {'case_details': {
            'def_name': 'A1',
            'def_addr': 'B',
            'pros_name': 'C',
            'pros_addr': 'D',
            'crime_type': 'E',
            'crime_date': 'F',
            'crime_loc': 'G',
            'arresting_off_name': 'H',
            'date_arrest': 'I',
            'CIN': 'J',
            'date_hearing': 'K',
            'latest_hearing_date': 'L',
            'adj_details': [{'date': "Date", 'reason': "Reason"}],
            'name_pres_judge': 'M',
            'start_date': 'N',
            'expected_completion_of_trial': 'O'
        },
            'due_amt': '0'
        }
    else:
        return {'case_details': {
            'def_name': 'A2',
            'def_addr': 'B',
            'pros_name': 'C',
            'pros_addr': 'D',
            'crime_type': 'E',
            'crime_date': 'F',
            'crime_loc': 'G',
            'arresting_off_name': 'H',
            'date_arrest': 'I',
            'CIN': 'J',
            'date_hearing': 'K',
            'latest_hearing_date': 'L',
            'adj_details': [{'date': "Date", 'reason': "Reason"}],
            'name_pres_judge': 'M',
            'start_date': 'N',
            'expected_completion_of_trial': 'O'
        },
            'due_amt': '0'
        }
    # and other case details
    # for lawyer
    # {'case_details':{...},'due_amt':'Amount in string'}
'''


@ app.route("/api/assignHearingSlot", methods=['GET', 'POST'])
@ login_required
def assignHearingSlot():
    print('Assign Hearing Date')
    req = flask.request.get_json()
    print(req)
    return schedule_case(req)
    # return {'confirm': "1", "message": "Success"}
    # return {"confirm":"0","message":"Failed"}


@ app.route("/api/closeCase", methods=['GET', 'POST'])
@ login_required
def closeCase():
    print('Close Case')
    req = flask.request.get_json()
    return close_case(req)
    # return {"confirm":"0","message":"Failed"}