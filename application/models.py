# dot means that module will search for db object in the databse in application not in root folder.
from .database import db 


# Admin data table
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(), primary_key = True)
    user_name = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    full_name = db.Column(db.String(), nullable = False)
    role = db.Column(db.String()) 


#Influencer table
class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer(), primary_key = True)
    user_name = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    niche = db.Column(db.String(), nullable = False)
    full_name = db.Column(db.String(), nullable = False)
    platform = db.Column(db.String(), nullable = False)
    followers = db.Column(db.String())
    role = db.Column(db.String())
    

#Sponsor table
class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    id = db.Column(db.Integer(), primary_key = True)
    user_name = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    full_name = db.Column(db.String(), nullable = False)
    industry = db.Column(db.String(), nullable = False)
    role = db.Column(db.String())
    campaign = db.relationship("Campaign", backref = "creator")  #psudo column for us to retrive data internally


#campaign table   
class Campaign(db.Model):
    __tablename__ = 'campaign'
    camp_id = db.Column(db.Integer(), primary_key = True)
    camp_name = db.Column(db.String(), nullable = False)
    sponsor_id = db.Column(db.Integer(), db.ForeignKey('sponsor.id'))
    category = db.Column(db.String(), nullable = False)
    s_date = db.Column(db.String(), nullable = False)
    e_date = db.Column(db.String(), nullable = False)
    budget = db.Column(db.Integer(), nullable = False)
    visibility = db.Column(db.String(), default = "public")
    description = db.Column(db.String())
    
    
#ad_request table
class Ad_Request(db.Model):
    __tablename__ = 'ad_request'
    request_id = db.Column(db.Integer(), primary_key = True)
    campaign_id = db.Column(db.Integer(), db.ForeignKey('campaign.camp_id'), nullable=False)
    influencer_id = db.Column(db.Integer(), db.ForeignKey('influencer.id'), nullable=False)
    niche = db.Column(db.String(), nullable = False)
    requirements = db.Column(db.String(), nullable = False)
    payment_amt = db.Column(db.Integer(), default = 1000)
    status = db.Column(db.String(), default = "pending")
    


    
  


