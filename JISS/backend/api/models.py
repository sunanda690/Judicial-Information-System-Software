from datetime import datetime
import datetime
from api import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class CourtCase(db.Model):
    cin = db.Column(db.Integer, primary_key=True)
    defendent_name = db.Column(db.String(100),nullable=False)
    defendent_address = db.Column(db.String(500),nullable=False)
    crime_type = db.Column(db.String(10),nullable=False)
    crime_date = db.Column(db.DateTime,nullable=False)
    crime_location = db.Column(db.String(500),nullable=False)
    arresting_officer_name = db.Column(db.String(100),nullable =False)
    date_of_arrest = db.Column(db.DateTime(),nullable=False)
    judge_name = db.Column(db.String(100),nullable=False)
    public_prosecutor_name = db.Column(db.String(100),nullable=False)
    starting_date = db.Column(db.DateTime(),nullable=False)
    expected_completion_date = db.Column(db.DateTime(),nullable=False)
    hearing_date = db.Column(db.DateTime())#Will be constantly updated with the upcoming hearing date
    hearing_slot = db.Column(db.Integer)#Same for the slot
    hearing_details = db.Column(db.Text)# New Adjournment reasons and summary will be appended to the end of this field
    latest_adjournment_date = db.Column(db.DateTime,nullable=True,default=datetime.datetime(1990,1,1))
    latest_adjournment_slot = db.Column(db.Integer,nullable=True)
    summary = db.Column(db.Text,nullable= True)
    is_closed = db.Column(db.Boolean,default=False)
    def __repr__(self):
        return f"Case Details : '{self.cin}' '{self.hearing_date}' '{self.hearing_slot}'"
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50),nullable = False , unique = True)
    name = db.Column(db.String(100),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    password  = db.Column(db.Text,nullable= False )
    due_amount = db.Column(db.Integer,default=0)
    user_type = db.Column(db.String(10),nullable = False)# One of "Lawyer" "Judge" "Registrar"
    def __repr__(self):
        return f"Name : '{self.name}' Address : '{self.address}' DUE : Rs. '{self.due_amount}'"

class SlotList(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cin = db.Column(db.Integer,nullable=False)
    date_of_hearing = db.Column(db.DateTime(),nullable=False)
    slot_of_hearing = db.Column(db.Integer,nullable=False)#SQLAlchemy does not support checking of constraints. We need to do this ourselves 
    def __repr__(self):
        return f"Hearing Date : '{self.date_of_hearing}||'{self.slot_of_hearing} CIN : '{self.cin}"
