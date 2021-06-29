
import json
from api.models import User, CourtCase, SlotList
from api.routes import add_lawyer_judge,enter_details_into_db
from api.routes import schedule_case,adjournment_details_add,close_case #3 funcs
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

    
'''
TEST SCHEDULE_CASE FUNCTION
'''
#for valid scheduling
def test_schedule_case():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    schedule = schedule = schedule_case({"cin":"1","slot":"2","date":{"month": "3", "year": "2021", "day": "4"}})
    print("Testing scheduling case 1 to Date:4/3/2021 and Slot:2")
    print(schedule)
    expected_output = {"confirm": "1", "message": "New hearing date assigned successfully!!"}
    assert json.loads(schedule) == expected_output

#for invalid cin
def test_schedule_case_invalid():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    schedule = schedule = schedule_case({"cin":"10","slot":"2","date":{"month": "2", "year": "2020", "day": "4"}})
    print("Testing scheduling invalid case 10 to Date:4/2/2020 and Slot:2")
    print(schedule)
    expected_output = {"confirm": "0", "message": "The given CIN does not exist!!"}
    assert json.loads(schedule) == expected_output

# for older date
def test_schedule_case_older():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    schedule = schedule = schedule_case({"cin":"1","slot":"2","date":{"month": "2", "year": "2021", "day": "4"}})
    print("Testing scheduling case 1 to Date:4/2/2021(whereas prev hearing was on 2/3/2021) and Slot:2")
    print(schedule)
    expected_output = {"confirm": "0", "message": "The new hearing date cannot be older than the previous one!!"}
    assert json.loads(schedule) == expected_output


'''
TEST ADDJOURNMENT_DDETAILS_ADD FUNCTION
'''
#test for valid inputs
def test_adjournment_details_add():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    adj = adjournment_details_add({'cin':"1","reason":"Not Complete"})
    print("Testing adding adjournment details to latest hearning of case 1.")
    print(adj)
    expected_output = {"confirm": "1", "message": "Adjournment details added successfully!!"}
    assert json.loads(adj) == expected_output

# test for invalid cin
def test_adjournment_details_add_invalid():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    adj = adjournment_details_add({'cin':"10","reason":"Not Complete"})
    print("Testing adding adjournment details to invalid case 10.")
    print(adj)
    expected_output = {"confirm": "0", "message": "The entered CIN is invalid!!"}
    assert json.loads(adj) == expected_output

# test for closed case
def test_adjournment_details_add_closed():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    close = close_case({'cin':"3",'case_summary':"closed"})
    adj = adjournment_details_add({'cin':"3","reason":"Not Complete"})
    print("Testing adding adjournment details to case 3 that has been closed.")
    print(adj)
    expected_output = {"confirm": "0", "message": "The case has already been closed!!"}
    assert json.loads(adj) == expected_output

# test for not scheduled case
def test_adjournment_details_add_nsched():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    adj = adjournment_details_add({'cin':"1","reason":"Not Complete"})
    adj = adjournment_details_add({'cin':"1","reason":"Need more Details"})
    print("Testing adding adjournment details to case 1 where hearning date was not assigned.")
    print(adj)
    expected_output = {"confirm": "0", "message": "Please assign the next hearing of the case!"}
    assert json.loads(adj) == expected_output

'''
TEST CLOSE_CASE FUNCTION
'''
# for invalid cin
def test_close_case_invalid():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    close = close_case({'cin':"30",'case_summary':"closed"})
    print("Test closing a invalid case 30")
    print(close)
    expected_output = {"confirm": "0", "message": "Sorry!! The given CIN does not exist!!"}
    assert json.loads(close) == expected_output
    
# for already closed
def test_close_case_closed():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    close = close_case({'cin':"3",'case_summary':"closed"})
    close = close_case({'cin':"3",'case_summary':"closed"})
    print("Test closing a already closed case 3")
    print(close)
    expected_output = {"confirm": "0", "message": "The case has already been closed!!"}
    assert json.loads(close) == expected_output

# for pending case
def test_close_case_pending():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    close = close_case({'cin':"4",'case_summary':"closed"})
    print("Test closing a pending case 4")
    print(close)
    expected_output = {"confirm": "1", "message": "The case has been successfully closed!!"}
    assert json.loads(close) == expected_output




if __name__=='__main__':
    # test_close_case_invalid()
    # test_close_case_closed()
    # test_close_case_pending()
    # test_schedule_case()
    # test_schedule_case_invalid()
    # test_schedule_case_older()
    test_adjournment_details_add()
    test_adjournment_details_add_invalid()
    test_adjournment_details_add_closed()
    test_adjournment_details_add_nsched()