import json
from api.models import User, CourtCase, SlotList
#from api.routes import add_lawyer_judge, remove_lawyer_judge, close_case,  enter_details_into_db, search_by_id, search_by_key, unresolved_case_list, resolved_case_list, case_status_query, court_cases_by_date, adjournment_details_add, schedule_case,search_vacant_slot
from api.routes import *
from api import db, bcrypt
import os
if(os.path.exists('./api/site.db')):
    os.remove('./api/site.db')
if(not os.path.exists('./api/site.db')):
    db.create_all()


def create_basic_db():
    # CourtCase.query.delete()
    # User.query.delete()
    # SlotList.query.delete()
    # add users
    reg = add_lawyer_judge({"usr_type": "Registrar", "username": "jissReg",
                            "usr_addr": "Kolkata", "name": "R", "password": "manage@01"})
    new_Judge = add_lawyer_judge(
        {"usr_type": "Judge", "username": "judge1", "usr_addr": "Kol", "name": "J", "password": "12345"})
    new_lawyer = add_lawyer_judge(
        {"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    # add cases
    # CASE A
    new_case = enter_details_into_db(
        {
            "def_name": "A",
            "def_addr": "CDE",
            "crime_type": "theft",
            "crime_date": {"month": "2", "year": "2021", "day": "28"},
            "crime_loc": "Park Street ",
            "arresting_off_name": " Ram Pal",
            "arrest_date": {"month": "3", "year": "2021", "day": "1"},
            "name_pres_judge": "Rohan Ray",
            "public_prosecutor_name": "Raghu Sen ",
            "starting_date": {"month": "3", "year": "2021", "day": "2"},
            "expected_completion_date": {"month": "3", "year": "2021", "day": "7"},
            "hearing_slot": "1",
            "hearing_date": {"month": "3", "year": "2021", "day": "2"}
        }
    )
    # CASE B
    new_case = enter_details_into_db(
        {
            "def_name": "B",
            "def_addr": "CDE",
            "crime_type": "robbery",
            "crime_date": {"month": "3", "year": "2021", "day": "15"},
            "crime_loc": "Santragachi",
            "arresting_off_name": "Amresh Sen",
            "arrest_date": {"month": "3", "year": "2021", "day": "20"},
            "name_pres_judge": "Abhijit Ray",
            "public_prosecutor_name": "Raghu Sen ",
            "starting_date": {"month": "3", "year": "2021", "day": "21"},
            "expected_completion_date": {"month": "3", "year": "2021", "day": "30"},
            "hearing_slot": "1",
            "hearing_date": {"month": "3", "year": "2021", "day": "21"}
        }
    )
    # CASE C
    new_case = enter_details_into_db(
        {
            "def_name": "C",
            "def_addr": "CVB",
            "crime_type": "arson",
            "crime_date": {"month": "3", "year": "2021", "day": "15"},
            "crime_loc": "Salt Lake",
            "arresting_off_name": " DCV",
            "arrest_date": {"month": "3", "year": "2021", "day": "20"},
            "name_pres_judge": "iop",
            "public_prosecutor_name": "SDC",
            "starting_date": {"month": "3", "year": "2021", "day": "21"},
            "expected_completion_date": {"month": "3", "year": "2021", "day": "30"},
            "hearing_slot": "3",
            "hearing_date": {"month": "3", "year": "2021", "day": "21"}
        }
    )
    print(new_case)
    # CASE D
    new_case = enter_details_into_db(
        {
            "def_name": "D",
            "def_addr": "DEF",
            "crime_type": "murder",
            "crime_date": {"month": "3", "year": "2021", "day": "15"},
            "crime_loc": "Park Street",
            "arresting_off_name": "ioptestkey",
            "arrest_date": {"month": "3", "year": "2021", "day": "20"},
            "name_pres_judge": "Raghu Sen",
            "public_prosecutor_name": "Ranjan Bose",
            "starting_date": {"month": "3", "year": "2021", "day": "19"},
            "expected_completion_date": {"month": "3", "year": "2021", "day": "30"},
            "hearing_slot": "5",
            "hearing_date": {"month": "3", "year": "2021", "day": "21"}
        }
    )

    # add more detalis about cases
    adj = adjournment_details_add({'cin': "1", "reason": "Not Complete"})
    # print(adj)
    schedule = schedule_case({"cin": "1", "slot": "2", "date": {
                             "month": "3", "year": "2021", "day": "4"}})
    # print(schedule)
    adj = adjournment_details_add(
        {'cin': "1", "reason": "More evidence required"})
    # print(adj)

    adj = adjournment_details_add({'cin': "2", "reason": "Not Complete"})
    schedule = schedule_case({"cin": "2", "slot": "3", "date": {
                             "month": "3", "year": "2021", "day": "22"}})
    adj = adjournment_details_add(
        {'cin': "2", "reason": "More evidence required"})
    schedule = schedule_case({"cin": "2", "slot": "1", "date": {
                             "month": "3", "year": "2021", "day": "26"}})

    adj = adjournment_details_add({'cin': "3", "reason": "Not Complete"})
    schedule = schedule_case({"cin": "3", "slot": "1", "date": {
                             "month": "3", "year": "2021", "day": "22"}})
    # adj = adjournment_details_add({'cin':"3","reason":"More evidence required"})
    close = close_case({'cin': "3", 'case_summary': "closed"})
    # print(close)

    adj = adjournment_details_add({'cin': "4", "reason": "Not Complete"})
    schedule = schedule_case({"cin": "4", "slot": "4", "date": {
                             "month": "3", "year": "2021", "day": "24"}})
    adj = adjournment_details_add(
        {'cin': "4", "reason": "More evidence required"})

    close = close_case({'cin': "4", 'case_summary': "closed"})


create_basic_db()
# ******************TESTS*************************


def test_lawyer():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()

    # Do with 4 #check amounts 200 for search by key 100 for search by id
    new_search = search_by_id("3", "lawyer1")
    expected_output = {
        "due_amt": "100",
        "case_details": {
            "CIN": "3",
            "def_name": "C",
            "def_addr": "CVB",
            "crime_type": "arson",
            "crime_date": "15-3-2021",
            "date_arrest": "20-3-2021",
            "start_date": "21-3-2021",
            "latest_hearing_date": "22-3-2021",
            "expected_completion_date": "30-3-2021",
            "crime_loc": "Salt Lake",
            "arresting_off_name": " DCV",
            "name_pres_judge": "iop",
            "pros_name": "SDC",
            "adj_details": [{'date': '21-3-2021', 'reason': 'Not Complete'}]
        }
    }
    print(new_search)
    assert json.loads(new_search) == expected_output
    new_search = search_by_key("iop", "lawyer1")
    expected_output = {
        "due_amt": "300",
        "confirm": "1",
        "message": "The search was successful!!",
        "cin_list": [
            {"cin": 3,
             "crime_type": "arson",
             "name_pres_judge": "iop",
             "start_date": "21-3-2021"},
            {"cin": 4,
             "crime_type": "murder",
             "name_pres_judge": "Raghu Sen",
             "start_date": "19-3-2021"}
        ]
    }
    # print(new_search)
    assert json.loads(new_search) == expected_output




def test_judge():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("3", "judge1")
    expected_output = {
        "due_amt": "0",
        "case_details": {
            "CIN": "3",
            "def_name": "C",
            "def_addr": "CVB",
            "crime_type": "arson",
            "crime_date": "15-3-2021",
            "date_arrest": "20-3-2021",
            "start_date": "21-3-2021",
            "latest_hearing_date": "22-3-2021",
            "expected_completion_date": "30-3-2021",
            "crime_loc": "Salt Lake",
            "arresting_off_name": " DCV",
            "name_pres_judge": "iop",
            "pros_name": "SDC",
            "adj_details": [{'date': '21-3-2021', 'reason': 'Not Complete'}]
        }
    }
    print(new_search)
    assert json.loads(new_search) == expected_output
    new_search = search_by_key("iop", "judge1")
    expected_output = {
        "confirm": "1",
        "message": "The search was successful!!",
        "cin_list": [
            {"cin": 3,
             "crime_type": "arson",
             "name_pres_judge": "iop",
             "start_date": "21-3-2021"},
            {"cin": 4,
             "crime_type": "murder",
             "name_pres_judge": "Raghu Sen",
             "start_date": "19-3-2021"}
        ]
    }
    print(new_search)
    assert json.loads(new_search) == expected_output


def test_register():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()

    new_lawyer = add_lawyer_judge(
        {"usr_type": "Lawyer", "username": "l20", "usr_addr": "Kol", "name": "L20", "password": "l20"})
    expected_msg = {"add_status": "1",
                    "err_msg": "The account of has been created successfully!!"}
    assert json.loads(new_lawyer) == expected_msg
    new_lawyer = add_lawyer_judge(
        {"usr_type": "Judge", "username": "j20", "usr_addr": "Kol", "name": "J20", "password": "j20"})
    expected_msg = {"add_status": "1",
                    "err_msg": "The account of has been created successfully!!"}
    assert json.loads(new_lawyer) == expected_msg

    unresolved_cases = unresolved_case_list()
    #print(unresolved_cases)
    expected_output = {
        "confirm": "1",
        "case_list": [
            {"cin": "1",
             "def_name": "A",
             "def_addr": "CDE",
             "crime_type": "theft",
             "crime_date": {"month": "2", "day": "28", "year": "2021"},
             "arrest_date": {"month": "3", "day": "1", "year": "2021"},
             "starting_date": {"month": "3", "day": "2", "year": "2021"},
             "crime_loc": "Park Street ",
             "arresting_off_name": " Ram Pal",
             "name_pres_judge": "Rohan Ray",
             "public_prosecutor_name": "Raghu Sen "},
            {"cin": "2",
             "def_name": "B",
             "def_addr": "CDE",
             "crime_type": "robbery",
             "crime_date": {"month": "3", "day": "15", "year": "2021"},
             "arrest_date": {"month": "3", "day": "20", "year": "2021"},
             "starting_date": {"month": "3", "day": "21", "year": "2021"},
             "crime_loc": "Santragachi",
             "arresting_off_name": "Amresh Sen",
             "name_pres_judge": "Abhijit Ray",
             "public_prosecutor_name": "Raghu Sen "}]

    }
    assert json.loads(unresolved_cases) == expected_output
    
    resolved_cases = resolved_case_list({"beg_date": {"month": "3", "year": "2021", "day": "1"}, "end_date": {
                                        "month": "3", "year": "2021", "day": "25"}})
    #print(resolved_cases)
    expected_output = {
        "confirm": 1,
        "case_list": [
            {"cin": 4,
             "name_pres_judge": "Raghu Sen",
             "starting_date": {"month": "3", "day": "19", "year": "2021"},
             "latest_date": {"month": "3", "day": "24", "year": "2021"},
             "case_summary": "closed"},
            {"cin": 3,
             "name_pres_judge": "iop",
             "starting_date": {"month": "3", "day": "21", "year": "2021"},
             "latest_date": {"month": "3", "day": "22", "year": "2021"},
             "case_summary": "closed"}
        ]
    }
    
    assert json.loads(resolved_cases) == expected_output
    #Query by status
    status = case_status_query({"cin":"3"})
    #print(status)
    expected_output = {"confirm": "1", "message": "Success!!!", "case_status": "Resolved"}
    assert json.loads(status) == expected_output
    #Query By date
    by_date = court_cases_by_date({"query_date":{"month": "3", "day": "26", "year": "2021"}})
    #print(by_date)
    expected_output = {"confirm": "1", 
    "case_list": [
        {"cin": "2", "slot": 1, "name_pres_judge": "Abhijit Ray", "crime_type": "robbery"}
        ]
    }
    assert json.loads(by_date) == expected_output
    #Removal of User
    rmv_lawyer = remove_lawyer_judge({"username": "l20"})    
    expected_msg = {"removed_status": "1","err_msg": "Username removed successfully!!"}

    assert json.loads(rmv_lawyer) == expected_msg
    rmv_lawyer = remove_lawyer_judge({"username": "j20"})    
    expected_msg = {"removed_status": "1","err_msg": "Username removed successfully!!"}

    assert json.loads(rmv_lawyer) == expected_msg
    #Vacant Slots
    srch = search_vacant_slot({"month": "3", "day": "26", "year": "2021"})
    print(srch)
    expected_output = {"free_slot": {"slot1": "0", "slot2": "1", "slot3": "1", "slot4": "1", "slot5": "1"}, "confirm": "1", "message": "Success!!!"}
    assert json.loads(srch) == expected_output
    #Shedule 1
    schedule = schedule = schedule_case({"cin":"1","slot":"2","date":{"month": "3", "year": "2021", "day": "26"}})
    print(schedule)
    expected_output = {"confirm": "1", "message": "New hearing date assigned successfully!!"}
    assert json.loads(schedule) == expected_output
    #entry Adj to 1
    adj = adjournment_details_add({'cin':"1","reason":"Closed"})
    print(adj)
    expected_output = {"confirm": "1", "message": "Adjournment details added successfully!!"}
    assert json.loads(adj) == expected_output
    #Close Case 1
    close = close_case({'cin':"1",'case_summary':"closed"})
    print(close)
    expected_output = {"confirm": "1", "message": "The case has been successfully closed!!"}
    assert json.loads(close) == expected_output
    #entry Adj to 2
    adj = adjournment_details_add({'cin':"2","reason":"To be Cont"})
    print(adj)
    expected_output = {"confirm": "1", "message": "Adjournment details added successfully!!"}
    assert json.loads(adj) == expected_output
    #Vacant Slots
    srch = search_vacant_slot({"month": "3", "day": "27", "year": "2021"})
    print(srch)
    expected_output = {"free_slot": {"slot1": "1", "slot2": "1", "slot3": "1", "slot4": "1", "slot5": "1"}, "confirm": "1", "message": "Success!!!"}
    assert json.loads(srch) == expected_output
    #Shedule 2
    schedule = schedule = schedule_case({"cin":"2","slot":"1","date":{"month": "3", "year": "2021", "day": "27"}})
    print(schedule)
    expected_output = {"confirm": "1", "message": "New hearing date assigned successfully!!"}
    assert json.loads(schedule) == expected_output
    #entry Adj to 2
    adj = adjournment_details_add({'cin':"2","reason":"Closed"})
    print(adj)
    expected_output = {"confirm": "1", "message": "Adjournment details added successfully!!"}
    assert json.loads(adj) == expected_output
    #Close case 2
    close = close_case({'cin':"2",'case_summary':"closed"})
    print(close)
    expected_output = {"confirm": "1", "message": "The case has been successfully closed!!"}
    assert json.loads(close) == expected_output
    # Add new Case
    new_case = enter_details_into_db(
        {
            "def_name": "MNP",
            "def_addr": "DEF",
            "crime_type": "Murder",
            "crime_date": {"month": "4", "year": "2021", "day": "15"},
            "crime_loc": "Salt Lake ",
            "arresting_off_name": "DCV",
            "arrest_date": {"month": "4", "year": "2021", "day": "20"},
            "name_pres_judge": "IOM",
            "public_prosecutor_name": "VFR",
            "starting_date": {"month": "4", "year": "2021", "day": "21"},
            "expected_completion_date": {"month": "4", "year": "2021", "day": "30"},
            "hearing_slot": "3",
            "hearing_date": {"month": "4", "year": "2021", "day": "21"}
        }
    )
    expected_output = {"is_added": "1", "cin": "5", "message": "The Case has been added successfully!!"}
    assert json.loads(new_case) == expected_output
#test_register()