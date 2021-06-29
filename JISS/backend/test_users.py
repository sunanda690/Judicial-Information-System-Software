
import json
from api.models import User, CourtCase, SlotList
from api.routes import add_lawyer_judge, remove_lawyer_judge,get_user_list  #3 funcs
from api import db, bcrypt
import os
if(os.path.exists('./api/site.db')):
    os.remove('./api/site.db')
if(not os.path.exists('./api/site.db')):
    db.create_all()



'''
TESTING ADD_LAWYER_JUDGE FUNCTION
'''

def test_addlawyer():    
    User.query.delete()
    new_lawyer = add_lawyer_judge(
        {"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    expected_msg = {"add_status": "1", "err_msg": "The account of has been created successfully!!"}
    print("adding lawyer details: {\"usr_type\": \"Lawyer\", \"username\": \"lawyer1\", \"usr_addr\": \"Kol\", \"name\": \"LAW1\", \"password\": \"12345\"}")
    print(new_lawyer)
    assert json.loads(new_lawyer) == expected_msg


# test add invalid  user
def test_addlawyer2():    
    User.query.delete()
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    inv_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    expected_msg = {"add_status":"0","err_msg":"Username Already Exists"}
    print("Trying to add lawyer with username : 'lawyer1' that already exists ")
    print(inv_lawyer)
    assert json.loads(inv_lawyer) == expected_msg

# test add new  user
def test_addjudge():
    User.query.delete()
    new_judge = add_lawyer_judge({"usr_type":"Judge","username":"judge1","usr_addr":"Kol","name":"JUD1","password":"12345"})
    print("adding Judge details: {\"usr_type\": \"Judge\", \"username\": \"judge1\", \"usr_addr\": \"Kol\", \"name\": \"JUD1\", \"password\": \"12345\"}")
    print(new_judge)
    expected_msg = {"add_status":"1", "err_msg":"The account of has been created successfully!!"}
    assert json.loads(new_judge)==expected_msg


# test add invalid judge
def test_addjudge2():
    User.query.delete()
    new_judge = add_lawyer_judge({"usr_type":"Judge","username":"judge1","usr_addr":"Kol","name":"JUD1","password":"12345"})
    inv_judge = add_lawyer_judge({"usr_type":"Judge","username":"judge1","usr_addr":"Kol","name":"JUD1","password":"12345"})
    print("Trying to add judge with username : 'judge1' that already exists ")
    print(inv_judge)
    expected_msg = {"add_status":"0","err_msg":"Username Already Exists"}
    assert json.loads(inv_judge)==expected_msg

'''
TESTING REMOVE_LAWYER_JUDGE FUNCTION
'''
# test remove lawyer
def test_removelawyer():   
    User.query.delete()
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    rmv_lawyer = remove_lawyer_judge({"username": "lawyer1"})   
    print("Trying to remove lawyer with username : 'lawyer1' that exists ")
    print(rmv_lawyer) 
    expected_msg = {"removed_status": "1","err_msg": "Username removed successfully!!"}
    assert json.loads(rmv_lawyer) == expected_msg

# test romoving ivalid lawyer

def test_removelawyer2():    
    User.query.delete()
    rmv_lawyer = remove_lawyer_judge({"username": "xxxxx"})
    print("Trying to remove lawyer with username : 'xxxxx' that does not exist ")
    print(rmv_lawyer) 
    expected_msg = {"removed_status": "0","err_msg": "Sorry!! The username does not exist!!"}
    assert json.loads(rmv_lawyer) == expected_msg

# test removing judge

def test_removejudge():    
    User.query.delete()
    new_Judge = add_lawyer_judge({"usr_type": "Judge", "username": "judge1", "usr_addr": "Kol", "name": "J", "password": "12345"})
    rmv_judge = remove_lawyer_judge({"username": "judge1"})
    print("Trying to remove judge with username : 'judge1' that exists ")
    print(rmv_judge) 
    expected_msg = {"removed_status": "1","err_msg": "Username removed successfully!!"}
    assert json.loads(rmv_judge) == expected_msg



'''
TESTING GET_USER_LIST FUNCTION
'''
def test_getuserlist():
    new_Judge = add_lawyer_judge({"usr_type": "Judge", "username": "judge1", "usr_addr": "Kol", "name": "J", "password": "12345"})
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer1", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    new_Judge = add_lawyer_judge({"usr_type": "Judge", "username": "judge2", "usr_addr": "Bombay", "name": "judUser2", "password": "5689"})
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "xxx", "usr_addr": "Kol", "name": "LAW1", "password": "12345"})
    rmv_judge = remove_lawyer_judge({"username":"xxx"})
    new_lawyer = add_lawyer_judge({"usr_type": "Lawyer", "username": "lawyer2", "usr_addr": "Chennai", "name": "LAW2", "password": "7889"})
    all_users = get_user_list()
    all_users = get_user_list()
    print("The users are:")
    print(all_users)
    expected_output = {
        "usr_list": [
            {"username": "judge1", "name": "J", "usr_type": "Judge"},
            {"username": "lawyer1", "name": "LAW1", "usr_type": "Lawyer"},
            {"username": "judge2", "name": "judUser2", "usr_type": "Judge"},
            {"username": "lawyer2", "name": "LAW2", "usr_type": "Lawyer"}
            ],
            "confirm":"1",
            "message": "Success!! Here is the list of users!!"
    }
    assert json.loads(all_users) == expected_output

if __name__=='__main__':
    print("yfgh")
    test_getuserlist()