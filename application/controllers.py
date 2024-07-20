# this is for all our routes
from flask import Flask, render_template,redirect,request
from flask import current_app as app # this refers to app.py we created, to avoid circular import.
from .models import * #import models 


@app.route('/')
def home():
    return "<h2>Welcome to app</h2>"

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
                return render_template("Influencer_dash.html", name = influencer.user_name)
            else:
                return render_template('login.html', msg= "incorrect paasword")
        elif sponsor:
            if sponsor.password == pwd:
                return redirect(f'/sponsor/{sponsor.id}')
                #return render_template("sponsor_dash.html", name = sponsor.user_name)
            else:
                return render_template('login.html', msg= "incorrect paasword")
        elif admin:
            if admin.password == pwd:
                return render_template("admin_dash.html", name = admin.user_name)
            else:
                return render_template('login.html', msg= "incorrect paasword")
        else:
            return render_template('login.html', msg= "user does not exist!!")       
    return render_template('login.html')


# for user register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        fullName = request.form.get("fullName")
       
        this_user = Admin.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists! as admin"
            this_user = Influencer.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists! as influencer"
            this_user = Sponsor.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists! as sponsor"
        else:
            new_user = Sponsor(user_name = u_name, password = pwd, fullName = fullName, type = "general", role="Sponsor")
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')
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
        this_user = Influencer.query.filter_by(user_name = u_name).first()
        if this_user:
            return "user already exists!"
        else:
            new_user = Influencer(user_name = u_name, password = pwd, niche = niche, full_name = fullName, platform = platform, role = "influencer")
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

# end point for sponsor (managing camapigns etc.)
@app.route('/sponsor/<int:sponsor_id>', methods=['GET', 'POST'])
def sponsor_dash(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor:
        campaigns = sponsor.campaign 
        print(f"Campaigns for sponsor {sponsor.id}: {campaigns}") #for debugging
    else:
        campaigns = []        
    return render_template("sponsor_dash.html", s_name = sponsor, campaigns = campaigns )




#allow aponsor to delete campaign
@app.route('/sponsor/<int:sponsor_id>/campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(sponsor_id, campaign_id):
    
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        return 'error - Sponsor not found'
    
    
    campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id=sponsor_id).first()
    if not campaign:
        return 'error -- Campaign not found or does not belong to the sponsor', 
    else: 
        db.session.delete(campaign)
        db.session.commit()
    return redirect(f'/sponsor/{sponsor.id}')
    return render_template("sponsor_dash.html", s_name = sponsor, campaigns = sponsor.campaign )

#allow sponsor to edit campaign
@app.route('/sponsoredit/<int:sponsor_id>/campaign/<int:campaign_id>', methods=['GET','POST'])
def edit_campaign(sponsor_id, campaign_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        return 'error - Sponsor not found'
    campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id=sponsor_id).first()
    if not campaign:
        return 'error -- Campaign not found or does not belong to the sponsor', 
    else: 
        if request.method == 'GET':
            return render_template('new_camp.html', s_name = sponsor, campaign_id = campaign_id, shouldUpdate= True )
        
        if request.method == 'POST':
            camp_name = request.form.get("camp_name")
            category = request.form.get("category")
            s_date = request.form.get("s_date")
            e_date = request.form.get("e_date")
            budget = request.form.get("budget")
            visibility = request.form.get("visibility")
            description = request.form.get("describe")
        #my_camp = Campaign(camp_name = camp_name, sponsor_id = sponsor.id, camp_id = campaign_id, category = category, s_date = s_date, e_date = e_date, budget = budget, visibility = visibility, description = description)
            #db.session.add(my_camp)
            db.session.commit()
            return redirect(f'/sponsor/{sponsor.id}')
        return render_template('new_camp.html', s_name = sponsor)


#create new campaign on clicking the button
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
        new_camp = Campaign(camp_name = camp_name, sponsor_id = sponsor.id, category = category, s_date = s_date, e_date = e_date, budget = budget, visibility = visibility, description = description)
        db.session.add(new_camp)
        db.session.commit()
        return redirect(f'/sponsor/{sponsor.id}')
    return render_template('new_camp.html', s_name = sponsor)

# allow sponsor to create an ad_request
@app.route('/sponsorad/<int:sponsor_id>/campaign/<int:campaign_id>', methods = ['GET','POST'])
def create_adRequest(sponsor_id, campaign_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if request.method == 'GET':
        return render_template('create_ad.html', s_name = sponsor, campaign_id = campaign_id )
    campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id = sponsor_id)

    if request.method == 'POST':
        niche = request.form.get("niche")
        requirements = request.form.get("requirements")
        payment_amt = request.form.get("payment_amt")
        status = request.form.get("status")
        my_req = Ad_Request(influencer_id = 1, campaign_id= campaign_id, niche = niche, requirements = requirements, payment_amt = payment_amt, status =status)
        db.session.add(my_req)
        db.session.commit()
        return redirect(f'/sponsor/{sponsor.id}')
    return render_template('create_ad.html', s_name = sponsor)



#search functionality for sponsor
@app.route('/search')
def text_search():
    search_word = request.args.get('search_word')
    search_word = "%" + search_word + "%"
    #print(search_word)
    full_name = Influencer.query.filter(Influencer.full_search_name.like(search_word)).all()
    return render_template('srch_influencer.html',full_name = full_name)


    


