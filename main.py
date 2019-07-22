from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import template
import os
import webapp2
from datetime import datetime
import pytz

class Page(webapp2.RequestHandler):
    values = {
        'urls':{
                'index':'/',
                'about':'/about-us',
                'contact':'/contact',
                'bp':'/business-permit',
                'ud':'/upload-docs',
                'as':'/application-sent'
            },
    }

    def get_page(self,htmlfile,template_values):
        path = os.path.join(os.path.dirname(__file__), htmlfile)
        self.response.out.write(template.render(path, self.values))

class BPForms(ndb.Model):
    application_type = ndb.StringProperty()
    amendments = ndb.StringProperty()
    transfer = ndb.StringProperty()
    mode_of_payment = ndb.StringProperty()
    type_of_organization = ndb.StringProperty()
    type_of_organization2 = ndb.StringProperty()
    type_of_organization3 = ndb.StringProperty()
    ctc_number = ndb.StringProperty()
    tin_number = ndb.StringProperty()
    dti_sec_cda_reg_num = ndb.StringProperty()
    dor = ndb.StringProperty()
    name_of_tax_payer = ndb.StringProperty()
    business_name = ndb.StringProperty()
    name_of_pres = ndb.StringProperty()
    tradename= ndb.StringProperty()
    complete_business_address = ndb.StringProperty()
    complete_owners_address = ndb.StringProperty()
    contact_number = ndb.StringProperty()
    business_area = ndb.StringProperty()
    place_of_business = ndb.StringProperty()
    monthly_rental = ndb.StringProperty()
    num_of_manager = ndb.StringProperty()
    num_of_supervisor = ndb.StringProperty()
    num_of_cashier = ndb.StringProperty()
    num_of_rankandfile = ndb.StringProperty()
    num_of_elevators = ndb.StringProperty()
    num_of_escalators = ndb.StringProperty()
    num_of_airconditioner = ndb.StringProperty()
    num_of_cctvs = ndb.StringProperty()
    lessor_name = ndb.StringProperty()
    billboard_area = ndb.StringProperty()
    billboard_light = ndb.StringProperty()
    lessor_address = ndb.StringProperty()
    email_address = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    status = ndb.StringProperty()
    date_created = ndb.DateTimeProperty()
    # date_created = ndb.DateTimeProperty(auto_now_add=True)
    # date_created = ndb.StringProperty()

class LandingPage(Page):
    def get(self):
        self.get_page('index.html',self.values)

class AboutUs(Page):
    def get(self):
        self.get_page('about-us.html',self.values)

class Contact(Page):
    def get(self):
        self.get_page('contact.html',self.values)

class ApplicationSent(Page):
    def get(self):
        self.get_page('application-sent.html',self.values)

class BusinessPermit(Page):
    def get(self):
        self.get_page('business-permit.html',self.values) 

    def post(self):
        form = BPForms()
        form.application_type = self.request.get('form_apptype')
        form.amendments = self.request.get('form_amend')
        form.transfer = self.request.get('form_transfer')
        form.mode_of_payment = self.request.get('form_mop')
        form.type_of_organization = self.request.get('form_too')
        form.type_of_organization2 = self.request.get('form_too2')
        form.type_of_organization3 = self.request.get('form_too3')
        form.ctc_number = self.request.get('form_ctc')
        form.tin_number = self.request.get('form_tin')
        form.dti_sec_cda_reg_num = self.request.get('form_dti')
        form.dor = self.request.get('form_dor')
        form.name_of_tax_payer = self.request.get('form_notp')
        form.business_name = self.request.get('form_bn')
        form.name_of_pres = self.request.get('form_nopres')
        form.tradename= self.request.get('form_tn')
        form.complete_business_address = self.request.get('form_cba')
        form.complete_owners_address = self.request.get('form_coa')
        form.contact_number = self.request.get('form_contact')
        form.business_area = self.request.get('form_ba')
        form.place_of_business = self.request.get('form_pob')
        form.monthly_rental = self.request.get('form_mr')
        form.num_of_manager = self.request.get('form_noofm')
        form.num_of_supervisor = self.request.get('form_noofs')
        form.num_of_cashier = self.request.get('form_noofc')
        form.num_of_rankandfile = self.request.get('form_noofrf')
        form.num_of_elevators = self.request.get('form_noofel')
        form.num_of_escalators = self.request.get('form_noofes')
        form.num_of_airconditioner = self.request.get('form_noofac')
        form.num_of_cctvs = self.request.get('form_noofcctv')
        form.lessor_name = self.request.get('form_lessorname')
        form.billboard_area = self.request.get('form_areabb')
        form.billboard_light = self.request.get('form_lights')
        form.lessor_address = self.request.get('form_lessorad')
        form.email_address = self.request.get('form_email')
        form.phone_number = self.request.get('form_phone')
        form.date_created = datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT-8')).replace(tzinfo=None)
        form_key = form.put()
        form = form_key.get()
        url_string = form_key.urlsafe()
        # self.redirect('/admin-Dashboard') 

class AdminProfile(Page):
    def get(self):
        self.get_page('dashboard.html',self.values)
    
class AdminPending(Page):
    def get(self):
        form = BPForms.query().fetch()
        self.values["ID"] = form
        self.get_page('pending.html',self.values)
    
    def post(self):
        what = self.request.get('this')
        form_id = self.request.get('edit_id')

        if what == "1":
            self.redirect('/admin-pending=%s' %form_id) 
        elif what == "2":
            form_key = ndb.Key(urlsafe=form_id)
            deleteThis = form_key.get()
            deleteThis.key.delete()
            self.redirect('/admin-pending')

class UserStatus(Page):
    def get(self,key):
        form_key = ndb.Key(urlsafe=key)
        form = form_key.get()
        self.values["form"] = form
        self.get_page('status.html',self.values)

class UserDelete(Page):
    def get(self,key):
        form_key = ndb.Key(urlsafe=key)
        deleteThis = form_key.get()
        deleteThis.key.delete()
        self.redirect('/admin-pending') 

app = webapp2.WSGIApplication([
    ('/', LandingPage),
    ('/about-us', AboutUs),
    ('/business-permit', BusinessPermit),
    ('/contact', Contact),
    ('/application-sent',ApplicationSent),
    ('/admin',AdminProfile),
    ('/admin-pending',AdminPending),
    ('/admin-pending=(.*)',UserStatus),
    ('/admin-delete=(.*)',UserDelete),

], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()