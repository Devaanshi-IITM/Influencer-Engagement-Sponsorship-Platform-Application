# this is for all our routes
from flask import Flask, render_template,redirect,request
from flask import current_app as app # this refers to app.py we created, to avoid circular import.
from .models import * #import models 

# route for home page
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
        if influencer and influencer.password == pwd:
            if influencer.is_flagged == True:
                return "Login denied, you have been flagged by the organization !!" 
            return redirect(f'/influencer/{influencer.id}')
        
        elif sponsor and sponsor.password == pwd:
            if sponsor.is_flagged == True:
                return "Login denied, you have been flagged by the organization !!"
            return redirect(f'/sponsor/{sponsor.id}')
            
        elif admin:
            if admin.password == pwd:
                return redirect(f'/admin/{admin.id}')
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

# set up admin dashboard
@app.route('/admin/<int:admin_id>', methods=['GET', 'POST'])
def admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        #influencer data
        active_inf = Influencer.query.filter_by(is_flagged = False).count()
        flag_inf = Influencer.query.filter_by(is_flagged = True).count()
        total_inf = active_inf + flag_inf

        #sposnors data
        active_spon = Sponsor.query.filter_by(is_flagged = False).count()
        flag_spon = Sponsor.query.filter_by(is_flagged = True).count()
        t_sponsor = active_spon + flag_spon

        # campaign data
        public_camp = Campaign.query.filter(Campaign.visibility == 'public').count()
        pvt_camp = Campaign.query.filter(Campaign.visibility == 'private').count()
        f_camp = Campaign.query.filter_by(is_flagged = True).count()
        total_camp = public_camp + pvt_camp + f_camp

        # ad request data
        pending_req = AdRequest.query.filter(AdRequest.status == 'pending').count()
        accepted_req = AdRequest.query.filter(AdRequest.status == 'accepted').count()
        rejected_req = AdRequest.query.filter(AdRequest.status == 'rejected').count()
        total_req = pending_req + accepted_req + rejected_req

        #flagged user
        total_flagged = flag_inf + flag_spon + f_camp

        return render_template('admin_dash.html', admin = admin, active_inf = active_inf, flag_inf = flag_inf, total_inf = total_inf,
                               active_spon = active_spon, flag_spon = flag_spon, t_sponsor = t_sponsor,
                               public_camp = public_camp, pvt_camp = pvt_camp , f_camp = f_camp, total_camp = total_camp,
                               pending_req = pending_req, accepted_req = accepted_req, rejected_req = rejected_req, total_req = total_req,
                               total_flagged = total_flagged)



# fetch influencers for admin
@app.route('/admin/influencer')
def fetch_influencer_info():
    influencer_info = Influencer.query.filter_by(is_flagged = False).all()
    flagged_influencers = Influencer.query.filter_by(is_flagged = True).all()  
    return render_template('influencers_stat.html', influencers = influencer_info,  flagged_influencers = flagged_influencers)


# fetch sponsor info for admin
@app.route('/admin/sponsor')
def fetch_sponsor_info():
    sponsor_info = Sponsor.query.filter_by(is_flagged = False).all()
    flagged_sponsors = Sponsor.query.filter_by(is_flagged = True).all()
    return render_template ('sponsor_stats.html', sponsors = sponsor_info, flagged_sponsors = flagged_sponsors)

# fetch camapigns info for admin
@app.route('/admin/campaigns')
def fetch_camp_info():
    camapign_info = Campaign.query.filter_by(is_flagged = False).all()
    flagged_camps = Campaign.query.filter_by(is_flagged = True).all()
    return render_template ('campaign_stats.html', campaigns = camapign_info, flagged_campaigns = flagged_camps)

#fetch ad request info for admin
@app.route('/admin/ad_requests')
def fetch_ad_info():
    ad_info = AdRequest.query.all()
    return render_template ('ad_request_stats.html', ads = ad_info)

# allow admin to flag an influencer
@app.route('/admin/flag_influencer/<int:influencer_id>', methods=['POST'])
def flag_influencer( influencer_id):
    if request.method == 'POST':
        influencer = Influencer.query.get(influencer_id)
        influencer.is_flagged = True
        db.session.commit()
        return redirect('/admin/influencer')
    
# allow admin to flag a sponsor
@app.route('/admin/flag_sponsor/<int:sponsor_id>', methods=['POST'])
def flag_sponsor( sponsor_id):
    if request.method == 'POST':
        sponsor = Sponsor.query.get(sponsor_id)
        sponsor.is_flagged = True
        db.session.commit()
        return redirect('/admin/sponsor')
    
# allow admin to flag a campaign
@app.route('/admin/flag_campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign( campaign_id ):
    if request.method == 'POST':
        campaign = Campaign.query.get(campaign_id)
        campaign.is_flagged = True
        db.session.commit()
        return redirect('/admin/campaigns')

#--------------------------------------------------------------------------------------------------------------------#
# end point for sponsor (managing camapigns etc.)
@app.route('/sponsor/<int:sponsor_id>', methods=['GET', 'POST'])
def sponsor_dash(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor:
        campaigns = sponsor.campaign 
        ads = AdRequest.query.filter_by(sponsor_id = sponsor_id).all()
        #print(f"Campaigns for sponsor {sponsor.id}: {campaigns}") #for debugging
        for ad in ads:
            ad.campaign_name = Campaign.query.get(ad.campaign_id).camp_name
    else:
        campaigns = [] 
        ads = []       
    return render_template("sponsor_dash.html", s_name = sponsor, campaigns = campaigns, ads = ads )

# allow aponsor to delete campaign
@app.route('/sponsor/<int:sponsor_id>/campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(sponsor_id, campaign_id):
    
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        return 'error - Sponsor not found'
     
    campaign = Campaign.query.filter_by(camp_id=campaign_id, sponsor_id=sponsor_id).first()
    if campaign:
        ad_req = AdRequest.query.filter_by(campaign_id = campaign_id).delete()
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
    
    campaign = Campaign.query.get(campaign_id)
        
    if request.method == 'POST':
        if campaign.is_flagged == True:
            return " This campaign is flagged !! you can not create ad request for it."
        
        niche = request.form.get("niche").strip().lower()
        requirements = request.form.get("requirements")
        payment_amt = request.form.get("payment_amt")
        status = request.form.get("status")
        end_date = request.form.get("end_date")
        request_type = campaign.visibility
        my_req = AdRequest(campaign_id=campaign_id, sponsor_id = sponsor_id, niche=niche, requirements=requirements,payment_amt=payment_amt, status=status, end_date = end_date, request_type = request_type)
        db.session.add(my_req)
        db.session.flush()

        if request_type == 'public':
            influencers = Influencer.query.all()
            for influencer in influencers:
                infrequest = Infrequest(influencer_id = influencer.id, ad_request_id = my_req.request_id, status = "pending", is_accepted = False)

            db.session.add(infrequest)
            db.session.commit()

        elif request_type == 'private':
            influencers = Influencer.query.filter(Influencer.niche == my_req.niche).all()
            for influencer in influencers:
                infrequest = Infrequest(influencer_id = influencer.id, ad_request_id = my_req.request_id, status = "pending", is_accepted = False)

            db.session.add(infrequest)
            db.session.commit()

        return redirect(f'/sponsor/{sponsor.id}')

# allow sponsor to edit an ad request
@app.route('/sponsor/<int:sponsor_id>/edit/ad_request/<int:request_id>', methods=['GET', 'POST'])
def edit_ad_request(sponsor_id, request_id):
    sponsor = Sponsor.query.get(sponsor_id)    
    ad_request = AdRequest.query.get(request_id)
    
    if ad_request.sponsor_id != sponsor_id:
        return " You can not edit this request "

    if request.method == 'POST':
        ad_request.niche = request.form.get("niche")
        ad_request.requirements = request.form.get("requirements")
        ad_request.payment_amt = request.form.get("payment_amt")
        ad_request.status = request.form.get("status")
        ad_request.end_date = request.form.get("end_date")

        db.session.commit()
        return redirect(f'/sponsor/{sponsor_id}')
    return render_template('edit_ad_request.html', s_name=sponsor, ad = ad_request)

# allow sponsor delete an ad request
@app.route('/sponsor/<int:sponsor_id>/delete/ad_request/<int:request_id>', methods=['POST'])
def delete_ad_request(sponsor_id, request_id):
    sponsor = Sponsor.query.get(sponsor_id)     
    ad_request = AdRequest.query.filter_by(sponsor_id=sponsor_id, request_id = request_id).first()
    db.session.delete(ad_request)
    db.session.commit()
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



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
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
       public_req = AdRequest.query.filter(AdRequest.request_type == 'public').all()
       pvt_req = AdRequest.query.filter(AdRequest.request_type == 'private', AdRequest.niche == influencer.niche).all()
       #print(pvt_req)
       ad_requests = public_req + pvt_req
       #print(ad_requests)
    else:
        ad_requests = []

    return render_template("influencer_dash.html", influencer = influencer, ad_requests = ad_requests)

    
# allow influencer to reject an ad_request
@app.route('/influencer/<int:influencer_id>/reject_ad_request/<int:request_id>', methods=['POST'])
def reject_ad_request(influencer_id, request_id):
    if request.method == 'POST':
        inf_req = Infrequest.query.filter_by(influencer_id = influencer_id, ad_request_id = request_id).first()
        inf_req.status = 'rejected'
        
        ad_request = AdRequest.query.get(request_id)
        ad_request.status = "rejected"
        db.session.commit()

        return redirect(f'/influencer/{influencer_id}')
    
# allow influencer to accept an ad_request
@app.route('/influencer/accept/<int:influencer_id>/ad_request/<int:request_id>', methods=['POST'])
def accept_ad_request(influencer_id, request_id):
    inf_req = Infrequest.query.filter_by(influencer_id = influencer_id, ad_request_id = request_id).first()
    if not inf_req:
        return "No ad request found"
    inf_req.status = 'accepted'
    inf_req.is_accepted = True
    
    ad_request = AdRequest.query.get(request_id)
    ad_request.status = "accepted"
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