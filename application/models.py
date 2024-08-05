# dot means that module will search for db object in the databse in application not in root folder.
from .database import db 


# Admin data table
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    full_name = db.Column(db.String, nullable = False)
    role = db.Column(db.String, default = "admin") 


#Influencer table
class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    niche = db.Column(db.String, nullable = False)
    search_niche  = db.Column(db.String)
    full_name = db.Column(db.String, nullable = False)
    platform = db.Column(db.String, nullable = False)
    followers = db.Column(db.String)
    role = db.Column(db.String, nullable = False)
    profile_pic  = db.Column(db.String)
    is_flagged = db.Column(db.Boolean, default = False)
    

#Sponsor table
class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    full_name = db.Column(db.String, nullable = False)
    industry = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False)
    is_flagged = db.Column(db.Boolean, default = False)
    

#campaign table   
class Campaign(db.Model):
    __tablename__ = 'campaign'
    camp_id = db.Column(db.Integer, primary_key = True)
    camp_name = db.Column(db.String, nullable = False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'))
    category = db.Column(db.String, nullable = False)
    search_category =db.Column(db.String, nullable = False) # for influencer to search relevant campaigns
    s_date = db.Column(db.String, nullable = False)
    e_date = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, nullable = False)
    visibility = db.Column(db.String, default = 'public') 
    description = db.Column(db.String)
    is_completed = db.Column(db.Boolean,  default =  False) 
    is_flagged = db.Column(db.Boolean, default = False)
    sponsor = db.relationship('Sponsor', backref='campaign') #pseudo col
    

#ad_request table
class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    request_id = db.Column(db.Integer, primary_key = True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.camp_id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    niche = db.Column(db.String, nullable = False)
    requirements = db.Column(db.String, nullable = False)
    payment_amt = db.Column(db.String, default = 1000)
    status = db.Column(db.String, default = "pending")
    end_date = db.Column(db.String, nullable = False)
    request_type = db.Column(db.String, nullable = False)
    is_accepted = db.Column(db.Boolean,  default =  False)
    campaign = db.relationship('Campaign', backref='ad_requests')
    sponsor = db.relationship('Sponsor', backref='ad_requests')  # pseudo
    infrequests = db.relationship('Infrequest', backref='ad_request')

# eatablish relation betwwen ad request and inluencer via a table
class Infrequest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable = False)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.request_id'), nullable = True)
    status = db.Column(db.String, default = "pending")
    is_accepted = db.Column(db.Boolean,  default =  False)
    influencer = db.relationship('Influencer', backref = 'ad_requests', lazy = True)
    ad_requests = db.relationship('AdRequest', backref = 'influencer', lazy = True)

    
  


