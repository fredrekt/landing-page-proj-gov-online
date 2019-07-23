from BPForm import BPForms, ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import template
import os
import webapp2
import pytz
from datetime import datetime
import time

class Page(webapp2.RequestHandler):
    values = {}
    def get_page(self,htmlfile,template_values):
        path = os.path.join(os.path.dirname(__file__), htmlfile)
        self.response.out.write(template.render(path, self.values))

class AdminProfile(Page):
    def get(self):
        self.get_page('dashboard.html',self.values)
    
class AdminPending(Page):
    def get(self):
        form = BPForms.query(BPForms.status == 'Pending').fetch()
        self.values["ID"] = form
        self.values["url"] = "adp"
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
            time.sleep(0.1)
            self.redirect('/admin-pending')

class AdminDenied(Page):
    def get(self):
        form = BPForms.query(BPForms.status == 'Denied').fetch()
        self.values["ID"] = form
        self.values["url"] = "add"
        self.get_page('denied.html',self.values)
    
    def post(self):
        form_id = self.request.get('edit_id')
        form_key = ndb.Key(urlsafe=form_id)
        deleteThis = form_key.get()
        deleteThis.key.delete()
        time.sleep(0.1)
        self.redirect('/admin-denied')

class AdminApproved(Page):
    def get(self):
        form = BPForms.query(BPForms.status == 'Approved').fetch()
        self.values["ID"] = form
        self.values["url"] = "ada"
        self.get_page('approved.html',self.values)
    
    def post(self):
        form_id = self.request.get('edit_id')
        self.redirect('/admin-pending=%s' %form_id) 

class UserStatus(Page):
    def get(self,key):
        form_key = ndb.Key(urlsafe=key)
        form = form_key.get()
        self.values["form"] = form
        self.get_page('status.html',self.values)
    
    def post(self,key):
        form_key = ndb.Key(urlsafe=key)
        form = form_key.get()
        form.status = self.request.get('decision')
        form.put()
        time.sleep(0.1)
        self.redirect('/admin-pending')

app = webapp2.WSGIApplication([
    ('/admin',AdminProfile),
    ('/admin-pending',AdminPending),
    ('/admin-pending=(.*)',UserStatus),
    ('/admin-approved',AdminApproved),
    ('/admin-denied',AdminDenied),

], debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()
