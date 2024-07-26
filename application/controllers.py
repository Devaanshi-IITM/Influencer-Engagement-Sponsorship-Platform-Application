# this is for all our routes
from flask import Flask, render_template,redirect,request
from flask import current_app as app # this refers to app.py we created, to avoid circular import.
from .models import * #import models 


@app.route('/')
def home():
    return render_template('home.html')

#for user login
@app.route('/userlogin', methods = ['GET','POST'])
def user_login():
    if request.method == "POST":
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        influencer = Influencer.query.filter_by(user_name = u_name).first() # i.e.the first entry itself
        sponsor = Sponsor.query.filter_by(user_name = u_name).first()
        admin = Admin.query.filter_by(user_name = u_name).first()
        if influencer:
            if influencer.password == pwd:
                if influencer.role == "influencer":
                    print(influencer)
            return redirect(f'/influencer/{influencer.id}')
        
        elif sponsor:
            if sponsor.password == pwd:
                if sponsor.role == "sponsor":
                    return redirect(f'/sponsor/{sponsor.id}')
        elif admin:
            if admin.password == pwd:
                if admin.role == "admin":
                    return render_template("admin_dash.html", name=admin.user_name)
        else:
            return render_template('login.html', msg="Incorrect username or password")

    return render_template('login.html')


# for user register
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# for influencer register
@app.route('/inf_register', methods=['GET', 'POST'])
def influencer_register():
    if request.method == "POST":
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        fullName = request.form.get("fullName")
        niche = request.form.get("niche")
        platform = request.form.get("platform")
        followers = request.form.get("followers")
        profile_picture = request.form.get("profile_picture")
        this_user = Influencer.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists!"
        else:
            new_user = Influencer(user_name = u_name, password = pwd, niche = niche, search_niche = raw(niche), full_name = fullName, platform = platform, followers = followers, role = "influencer", profile_pic = profile_picture)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')
    return render_template('register_influencer.html')

#for sponsor registration
@app.route('/spon_register', methods=['GET', 'POST'])
def sponsor_register():
    if request.method == "POST":
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        fullName = request.form.get("fullName")
        industry = request.form.get("industry")
        this_user = Sponsor.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists!"
        else:
            new_user = Sponsor(user_name = u_name, password = pwd, full_name = fullName, industry = industry, role="sponsor")
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')
    return render_template('register_sponsor.html')

# fetch sponsor info
def fetch_sponsor_info(id):
    sponsor_info = Sponsor.query.filter_by(id=id).first()
    return sponsor_info

# end point for sponsor (managing camapigns etc.)
@app.route('/sponsor/<int:sponsor_id>', methods=['GET', 'POST'])
def sponsor_dash(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor:
        campaigns = sponsor.campaign 
        #print(f"Campaigns for sponsor {sponsor.id}: {campaigns}") #for debugging
    else:
        campaigns = []        
    return render_template("sponsor_dash.html", s_name = sponsor, campaigns = campaigns )


# allow aponsor to delete campaign
@app.route('/sponsor/<int:sponsor_id>/campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(sponsor_id, campaign_id):
    
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        return 'error - Sponsor not found'
     
    campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id=sponsor_id).first()
    if not campaign:
        return 'error - Campaign not found or does not belong to the sponsor', 
    else: 
        db.session.delete(campaign)
        db.session.commit()
    return redirect(f'/sponsor/{sponsor.id}')

# allow sponsor to edit campaign
@app.route('/sponsor/edit/<int:sponsor_id>/campaign/<int:campaign_id>', methods=['GET', 'POST'])
def edit_campaign(sponsor_id, campaign_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        return "Sponsor not found"

    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return "No campaign found"

    if request.method == 'POST':
        campaign.camp_name = request.form.get("camp_name")
        campaign.category = request.form.get("category")
        campaign.s_date = request.form.get("s_date")
        campaign.e_date = request.form.get("e_date")
        campaign.budget = request.form.get("budget")
        campaign.visibility = request.form.get("visibility")
        campaign.description = request.form.get("describe")
        db.session.commit()
        return redirect(f'/sponsor/{sponsor_id}')
    return render_template('edit_camp.html', s_name=sponsor, campaign=campaign)


# allows sponsor to create new campaign
@app.route('/new_campaign/<int:sponsor_id>', methods = ['GET','POST'])
def new_campaign(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if request.method == 'POST':
        camp_name = request.form.get("camp_name")
        category = request.form.get("category")
        s_date = request.form.get("s_date")
        e_date = request.form.get("e_date")
        budget = request.form.get("budget")
        visibility = request.form.get("visibility")
        description = request.form.get("describe")
        new_camp = Campaign(camp_name = camp_name, sponsor_id = sponsor.id, category = category, search_category =  raw(category) ,s_date = s_date, e_date = e_date, budget = budget, visibility = visibility, description = description)
        db.session.add(new_camp)
        db.session.commit()
        return redirect(f'/sponsor/{sponsor.id}')
    return render_template('new_camp.html', s_name = sponsor)
       # search_category is for search functionality implementation


# allow sponsor to create an ad_request
@app.route('/sponsorad/<int:sponsor_id>/campaign/<int:campaign_id>', methods = ['GET','POST'])
def create_adRequest(sponsor_id, campaign_id):
   
    sponsor = Sponsor.query.get(sponsor_id)
    if request.method == 'GET':
        return render_template('create_ad.html', s_name = sponsor, campaign_id = campaign_id )
    
    if request.method == 'POST':
        niche = request.form.get("niche")
        requirements = request.form.get("requirements")
        payment_amt = request.form.get("payment_amt")
        status = request.form.get("status")
        end_date = request.form.get("end_date")
        influencer = Influencer.query.filter_by(niche=niche).first()
        print(influencer)
        if influencer:
            my_req = AdRequest(influencer_id=influencer.id, campaign_id=campaign_id, niche=niche, requirements=requirements,payment_amt=payment_amt, status=status, end_date = end_date)
            print(my_req)
            db.session.add(my_req)
            db.session.commit()
            return redirect(f'/sponsor/{sponsor.id}')
        else:
            error_msg = "No influencer with the specified niche."    
            #redirect to error page   
        
        return redirect(f'/sponsor/{sponsor.id}')
    


# convert a text into lower case, will use this function for searching functionalitiy
def raw(text):
    split_list = text.split() ## ---> will give me a list splitted by space
    search_word = ''
    for word in split_list:
        search_word += word.lower()
    return search_word

#search functionality for sponsor
@app.route('/inf_search')
def text_search():
    srch_word = request.args.get('srch_word') # takes data when data is coming from url
    srch_word = "%"+raw(srch_word)+"%"
    srch_name = '%'+srch_word.lower()+'%'
    srch_platform = '%'+srch_word.lower()+'%'
    srch_followers = '%'+srch_word.lower()+'%'
    i_niche =  Influencer.query.filter(Influencer.search_niche.like(srch_word)).all() # can also use ilike instead of like to make search case insensitive
    i_name = Influencer.query.filter(Influencer.full_name.like(srch_name)).all()
    i_platfrom = Influencer.query.filter(Influencer.platform.like(srch_platform)).all()
    i_followers = Influencer.query.filter(Influencer.followers.like(srch_followers)).all()
    search_results = i_niche + i_name + i_platfrom + i_followers
    return render_template('sponsor_srch_result.html', search_results = search_results )

#search functionality for influencer
@app.route('/search')
def search():
    srch_word = request.args.get('srch_word') # takes data when data is coming from url
    srch_word = "%"+raw(srch_word)+"%"   
    srch_type = "%"+srch_word.lower()+"%"
    srch_cat =  Campaign.query.filter(Campaign.search_category.like(srch_word)).all() # can also use ilike instead of like to make search case insensitive
    srch_type = Campaign.query.filter(Campaign.visibility.like(srch_type), Campaign.visibility == 'public').all()
    search_results = srch_cat + srch_type
    return render_template('campaign_srch.html', search_results = search_results )
    
    

#end point for influencer dashboard
@app.route('/influencer/<int:influencer_id>', methods=['GET', 'POST'])
def influencer_dash(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        ad_requests = influencer.ad_requests  # fetches all request associated with influencer
        print(ad_requests)
    else:
        ad_requests = []

    return render_template("influencer_dash.html", influencer = influencer, ad_requests=ad_requests)

    
# allow influencer to reject an ad_request
@app.route('/influencer/<int:influencer_id>/reject_ad_request/<int:request_id>', methods=['POST'])
def reject_ad_request(influencer_id, request_id):
    if request.method == 'POST':
        influencer = Influencer.query.get(influencer_id)
        print(influencer)
        if influencer:
            ad_request = AdRequest.query.filter_by(request_id = request_id, influencer_id = influencer_id).first()
            ad_request.status = 'rejected'
            ad_request.is_accepted = False
            db.session.commit()
            return redirect(f'/influencer/{influencer_id}')
    
# allow influencer to accept an ad_request
@app.route('/influencer/accept/<int:influencer_id>/ad_request/<int:request_id>', methods=['POST'])
def accept_ad_request(influencer_id, request_id):
    influencer = Influencer.query.get(influencer_id) #look for influencer by his id
    if not influencer:
        return "Influencer not found"
    
    ad_request = AdRequest.query.filter_by(request_id = request_id, influencer_id = influencer_id).first() # look for ad request and influencer.
    if not ad_request:
        return "Ad request not found"
    
    ad_request.status = 'accepted'
    ad_request.is_accepted = True
    db.session.commit()
    return redirect(f'/influencer/{influencer_id}')
    
    

# allow influlencer to update his/her profile
@app.route('/influencer/update/<int:influencer_id>', methods=['GET', 'POST'])
def update_profile(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    if not influencer:
        return "Influencer not found"

    if request.method == 'POST':
        influencer.user_name = request.form.get("u_name")
        influencer.password = request.form.get("pwd")
        influencer.niche = request.form.get("niche")
        influencer.full_name = request.form.get("fullName")
        influencer.platfrom = request.form.get("platfrom")
        influencer.followers = request.form.get("followers")
        influencer.profile_pic = request.form.get("profile_picture")
        
        db.session.commit()
        return redirect(f'/influencer/{influencer_id}')
    return render_template('update_influencer_profile.html', influencer=influencer)