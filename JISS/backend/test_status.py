
import json
from api.models import User, CourtCase, SlotList
from api.routes import add_lawyer_judge,enter_details_into_db,close_case,schedule_case,adjournment_details_add
from api.routes import resolved_case_list,court_cases_by_date,case_status_query,unresolved_case_list,search_vacant_slot,add_to_slotlist    #6funcs
from api import db, bcrypt
import os
if(os.path.exists('./api/site.db')):
    os.remove('./api/site.db')
if(not os.path.exists('./api/site.db')):
    db.create_all()


def create_basic_db():
    #add users
    reg = add_lawyer_judge({"usr_type": "Registrar", "username": "jissReg", "usr_addr": "Kolkata", "name": "R", "password": "manage@01"})
    new_Judge = add_lawyer_judge({"usr_type": "Judge", "username": "judge1", "usr_addr": "Kol", "name": "J", "password": "12345"})
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    #add cases
    #CASE A
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
            "expected_completion_date": {"month":"3", "year":"2021", "day":"7"},
            "hearing_slot":"1",
            "hearing_date":{"month": "3", "year": "2021", "day": "2"}
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
            "expected_completion_date": {"month":"3", "year":"2021", "day":"30"},
            "hearing_slot":"1",
            "hearing_date":{"month": "3", "year": "2021", "day": "21"}
        }
    )
    #CASE C
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
            "expected_completion_date": {"month":"3", "year":"2021", "day":"30"},
            "hearing_slot":"3",
            "hearing_date":{"month": "3", "year": "2021", "day": "21"}
        }
    )
    #CASE D
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
            "expected_completion_date": {"month":"3", "year":"2021", "day":"30"},
            "hearing_slot":"5",
            "hearing_date":{"month": "3", "year": "2021", "day": "21"}
           }
    )
    #add more detalis about cases
    adj = adjournment_details_add({'cin':"1","reason":"Not Complete"})
    # print(adj)
    schedule = schedule_case({"cin":"1","slot":"2","date":{"month": "3", "year": "2021", "day": "4"}})
    # print(schedule)
    adj = adjournment_details_add({'cin':"1","reason":"More evidence required"})
    # print(adj)

    adj = adjournment_details_add({'cin':"2","reason":"Not Complete"})
    schedule = schedule_case({"cin":"2","slot":"3","date":{"month": "3", "year": "2021", "day": "22"}})
    adj = adjournment_details_add({'cin':"2","reason":"More evidence required"})
    schedule = schedule_case({"cin":"2","slot":"1","date":{"month": "3", "year": "2021", "day": "26"}})
    
    adj = adjournment_details_add({'cin':"3","reason":"Not Complete"})
    schedule = schedule_case({"cin":"3","slot":"1","date":{"month": "3", "year": "2021", "day": "22"}})
    # adj = adjournment_details_add({'cin':"3","reason":"More evidence required"})
    close = close_case({'cin':"3",'case_summary':"closed"})
    # print(close)

    adj = adjournment_details_add({'cin':"4","reason":"Not Complete"})
    schedule = schedule_case({"cin":"4","slot":"4","date":{"month": "3", "year": "2021", "day": "24"}})
    adj = adjournment_details_add({'cin':"4","reason":"More evidence required"})
    
    close = close_case({'cin':"4",'case_summary':"closed"})
    # print(close)




'''
TESTING RESOLVED_CASE_LIST FUNCTION
'''

'''
case starting date lying between start date and end date
    StartDate=’1/3/2021’  EndDate = ‘25/3/2021’
    Test Output :
    List of CIN(sorted by chronological order of start date) : [C4,C3]
    Test case2:
    StartDate=’1/3/2021’  EndDate = ‘20/3/2021’
    Test Output :
    List of CIN(sorted by chronological order of start date) :[C3]
'''
def test_resolved_case_list1():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    resolved_cases = resolved_case_list({"beg_date":{"month": "3", "year": "2021", "day": "1"},"end_date":{"month": "3", "year": "2021", "day": "25"}})
    print("List of resolved cases prensent in DB having starting date between 1/3/2021 and 25/3/2021 are:")
    print(resolved_cases)
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

def test_resolved_case_list2():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    resolved_cases = resolved_case_list({"beg_date":{"month": "3", "year": "2021", "day": "1"},"end_date":{"month": "3", "year": "2021", "day": "20"}})
    print("List of resolved cases prensent in DB having starting date between 1/3/2021 and 20/3/2021 are:")
    print(resolved_cases)
    expected_output = {
        "confirm": 1, 
        "case_list": [
            {"cin": 4, 
            "name_pres_judge": "Raghu Sen", 
            "starting_date": {"month": "3", "day": "19", "year": "2021"}, 
            "latest_date": {"month": "3", "day": "24", "year": "2021"}, 
            "case_summary": "closed"}
            ]
        }
    assert json.loads(resolved_cases) == expected_output

'''
TESTING UNRESOLVED_CASE_LIST FUNCTION
'''
# a single test is sufficient
def test_unresolved_case_list():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    unresolved_cases = unresolved_case_list()
    print("List of pending cases prensent in DB are:")
    print(unresolved_cases)
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

'''
TESTING COURT_CASE_BY_DATE FUNCTION
'''
# a single test is sufficient
def test_court_cases_by_date():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    by_date = court_cases_by_date({"query_date":{"month": "3", "day": "26", "year": "2021"}})
    print("Cases coming up on 26/3/2021 are:")
    print(by_date)
    expected_output = {"confirm": "1", 
    "case_list": [
        {"cin": "2", "slot": 1, "name_pres_judge": "Abhijit Ray", "crime_type": "robbery"}
        ]
    }
    assert json.loads(by_date) == expected_output


'''
TESTING CASE_STATUS_QUERY FUNCTION
'''
# for closed case
def test_case_status_query_resolved():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    status = case_status_query({"cin":"3"})
    print("Testing status of closed case C.")
    print(status)
    expected_output = {"confirm": "1", "message": "Success!!!", "case_status": "Resolved"}
    assert json.loads(status) == expected_output

# for pending case
def test_case_status_query_pending():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    status = case_status_query({"cin":"1"})
    print("Testing status of pending case A.")
    print(status)
    expected_output = {"confirm": "1", "message": "Success!!!", "case_status": "Pending"}
    assert json.loads(status) == expected_output

# for invalid case
def test_case_status_query_invalid():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    status = case_status_query({"cin":"30"})
    print("Testing status of a case with invalid cin.")
    print(status)
    expected_output = {"confirm": "0", "message": "The input CIN does not exist!!"}
    assert json.loads(status) == expected_output

'''
TEST SERACH_VACAT_SLOT FUNCTION
'''
def test_search_vacant_slot():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    srch = search_vacant_slot({"month": "3", "day": "26", "year": "2021"})
    print("Testing vacant slots on 26/03/2021:")
    print(srch)
    expected_output = {"free_slot": {"slot1": "0", "slot2": "1", "slot3": "1", "slot4": "1", "slot5": "1"}, "confirm": "1", "message": "Success!!!"}
    assert json.loads(srch) == expected_output


'''
TEST ADD_TO_SLOTLIST FUNCTION
'''
def test_add_to_slotlist():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    addslot = add_to_slotlist(1,5,2021,4,30)
    print("CIN:1 date:30/4/2021 slot:5 inserted in DB")
    print(addslot)



# if __name__=='__main__':
#     # test_resolved_case_list1()
#     # test_resolved_case_list2()
#     # test_unresolved_case_list()
#     # test_court_cases_by_date()
#     # test_case_status_query_resolved()
#     # test_case_status_query_pending()
#     # test_case_status_query_invalid()
#     # test_search_vacant_slot()
#     test_add_to_slotlist()