
import json
from api.models import User, CourtCase, SlotList
from api.routes import add_lawyer_judge,add_lawyer_judge, close_case,  enter_details_into_db,search_by_id,search_by_key #3 funcs
from api import db, bcrypt
import os
if(os.path.exists('./api/site.db')):
    os.remove('./api/site.db')
if(not os.path.exists('./api/site.db')):
    db.create_all()



'''
TESTING ENTER_DETAILS_INTO_DB FUNCTION
'''
# test add new case without any hearing date assigned

def test_enter_details_into_db1():    
    CourtCase.query.delete()
    new_case = enter_details_into_db(
        {
            "def_name": "A",
            "def_addr": "sdff",
            "crime_type": "theft",
            "crime_date": {"month": "4", "year": "2020", "day": "15"},
            "crime_loc": "Kolkata ",
            "arresting_off_name": " Ram",
            "arrest_date": {"month": "5", "year": "2020", "day": "15"},
            "name_pres_judge": "J.Kabir",
            "public_prosecutor_name": "Altim ",
            "starting_date": {"month": "4", "year": "2020", "day": "20"},
            "expected_completion_date": {"month":"4", "year":"2021", "day":"25"},
            "hearing_slot":-1
        }
    )
    print("Testing Adding Case A(without any assigned hearing date) in DB:")
    print(new_case)
    expected_msg = {"is_added": "1", "cin": "1", "message": "The Case has been added successfully!!"}
    assert json.loads(new_case) == expected_msg

# test add new case with a hearing date assigned

def test_enter_details_into_db2():    
    CourtCase.query.delete()
    new_case = enter_details_into_db(
        {
            "def_name": "A",
            "def_addr": "sdff",
            "crime_type": "theft",
            "crime_date": {"month": "4", "year": "2020", "day": "15"},
            "crime_loc": "Kolkata ",
            "arresting_off_name": " Ram",
            "arrest_date": {"month": "5", "year": "2020", "day": "15"},
            "name_pres_judge": "J.Kabir",
            "public_prosecutor_name": "Altim ",
            "starting_date": {"month": "4", "year": "2020", "day": "20"},
            "expected_completion_date": {"month":"4", "year":"2021", "day":"25"},
            "hearing_slot":"2",
            "hearing_date":{"month": "4", "year": "2020", "day": "21"}
        }
    )
    print("Testing Adding Case A(with a assigned hearing date) in DB:")
    print(new_case)
    expected_msg = {"is_added": "1", "cin": "1", "message": "The Case has been added successfully!!"}
    assert json.loads(new_case) == expected_msg

#test add new case with sequencial assignment of CIN
def test_enter_details_into_db3():
    CourtCase.query.delete()
    new_case = enter_details_into_db(
        {
            "def_name": "A",
            "def_addr": "sdff",
            "crime_type": "theft",
            "crime_date": {"month": "4", "year": "2020", "day": "15"},
            "crime_loc": "Kolkata ",
            "arresting_off_name": " Ram",
            "arrest_date": {"month": "5", "year": "2020", "day": "15"},
            "name_pres_judge": "J.Kabir",
            "public_prosecutor_name": "Altim ",
            "starting_date": {"month": "4", "year": "2020", "day": "20"},
            "expected_completion_date": {"month":"4", "year":"2021", "day":"25"},
            "hearing_slot":"2",
            "hearing_date":{"month": "4", "year": "2020", "day": "21"}
        }
    )
    print("Testing Adding Case A and B sequentially in DB(to check CIN assignment):")
    print(new_case)
    expected_msg = {"is_added": "1", "cin": "1", "message": "The Case has been added successfully!!"}
    assert json.loads(new_case) == expected_msg
    new_case = enter_details_into_db(
        {
            "def_name": "B",
            "def_addr": "sdff",
            "crime_type": "murder",
            "crime_date": {"month": "4", "year": "2020", "day": "15"},
            "crime_loc": "Kolkata ",
            "arresting_off_name": " Ram",
            "arrest_date": {"month": "5", "year": "2020", "day": "15"},
            "name_pres_judge": "J.Kabir",
            "public_prosecutor_name": "Altim ",
            "starting_date": {"month": "4", "year": "2020", "day": "16"},
            "expected_completion_date": {"month":"4", "year":"2021", "day":"20"},
            "hearing_slot":-1
        }
    )
    print(new_case)
    expected_msg = {"is_added": "1", "cin": "2", "message": "The Case has been added successfully!!"}
    assert json.loads(new_case) == expected_msg




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

    #close case C & D
    close = close_case({'cin':3,'case_summary':"closed"})
    # print(close)
    close = close_case({'cin':4,'case_summary':"closed"})
    # print(close)
'''
TESTING SEARCH_BY_KEY FUNCTION
'''

#test search by key for judge
def test_search_by_key_judge():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_key("iop","judge1")
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
    print("Tesing search of keyword 'iop' (present in case 3 and 4) for 'judge1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by key for lawyer
def test_search_by_key_lawyer():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_key("iop","lawyer1")
    expected_output = {
        "due_amt": "200",
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
    print("Tesing search of keyword 'iop' (present in case 3 and 4) for 'lawyer1'")
    print(new_search)
    assert json.loads(new_search) == expected_output


#test search by key for judge when keyword also have pending xases
def test_search_by_key_judge2():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_key("Park Street","judge1")
    expected_output = {
        "confirm": "1",
        "message": "The search was successful!!",
        "cin_list": [
            {"cin": 4,
            "crime_type": "murder",
            "name_pres_judge": "Raghu Sen",
            "start_date": "19-3-2021"}
        ]
    }
    print("Tesing search of keyword 'Park Street' (present in case 1(still pending) and 4) for 'judge1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by key for lawyer when keyword also have pending xases
def test_search_by_key_lawyer2():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_key("Park Street","lawyer1")
    expected_output = {
        "due_amt": "200",
        "confirm": "1",
        "message": "The search was successful!!",
        "cin_list": [
            {"cin": 4,
            "crime_type": "murder",
            "name_pres_judge": "Raghu Sen",
            "start_date": "19-3-2021"}
        ]
    }
    print("Tesing search of keyword 'Park Street' (present in case 1(still pending) and 4) for 'lawyer1'")
    print(new_search)
    assert json.loads(new_search) == expected_output



'''
TESTING SEARCH_BY_ID FUNCTION
'''

#test search by id for judge
def test_search_by_id_judge():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("3","judge1")
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
            "latest_hearing_date": "21-3-2021", 
            "expected_completion_date": "30-3-2021", 
            "crime_loc": "Salt Lake", 
            "arresting_off_name": " DCV", 
            "name_pres_judge": "iop", 
            "pros_name": "SDC", 
            "adj_details": []
            }
        }
    print("Testing search CIN 3 for 'judge1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by id for lawyer
def test_search_by_id_lawyer():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("3","lawyer1")
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
            "latest_hearing_date": "21-3-2021", 
            "expected_completion_date": "30-3-2021", 
            "crime_loc": "Salt Lake", 
            "arresting_off_name": " DCV", 
            "name_pres_judge": "iop", 
            "pros_name": "SDC", 
            "adj_details": []
            }
        }
    print("Testing search CIN 3 for 'lawyer1'")
    print(new_search)
    assert json.loads(new_search) == expected_output


#test search by wrong id for judge
def test_search_by_id_judge2():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("16","judge1")
    expected_output = {"due_amt": "0", "confirm": "0", "message": "Please search for a valid CIN number!!"}
    print("Testing search invalis CIN 16 for 'judge1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by wrong id for lawyer
def test_search_by_id_lawyer2():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("16","lawyer1")
    expected_output = {"due_amt": "0", "confirm": "0", "message": "Please search for a valid CIN number!!"}
    print("Testing search invalid CIN 16 for 'lawyer1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by pending case id for judge
def test_search_by_id_judge3():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("1","judge1")
    expected_output = {"due_amt": "0", "confirm": "0", "message": "This is a pending Case!!"}
    print("Testing search CIN 1(still pending) for 'judge1'")
    print(new_search)
    assert json.loads(new_search) == expected_output

#test search by pending case id for lawyer
def test_search_by_id_lawyer3():
    CourtCase.query.delete()
    User.query.delete()
    SlotList.query.delete()
    create_basic_db()
    new_search = search_by_id("1","lawyer1")
    expected_output = {"due_amt": "0", "confirm": "0", "message": "This is a pending Case!!"}
    print("Testing search CIN 1(still pending) for 'lawyer1'")
    print(new_search)
    assert json.loads(new_search) == expected_output



# if __name__=='__main__':
#     # test_enter_details_into_db1()
#     # test_enter_details_into_db2()
#     # test_enter_details_into_db3()
#     test_search_by_key_judge2()
#     # test_search_by_id_judge()
#     # test_search_by_id_lawyer()
#     # test_search_by_id_judge()
#     # test_search_by_id_lawyer2()