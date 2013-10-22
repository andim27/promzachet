#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#---
#------path = os.path.join(os.path.dirname(__file__), 'index.html')




import wsgiref.handlers
from site_models import *

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data= {'page':'index','mydata':'1'}
        else:
            data= {'page':'index'}
        self.response.out.write(template.render('index.html',data))

class EnterHandler(webapp.RequestHandler):

  def get(self):
    user = users.get_current_user()
    if user:
        user_has_account=1
        user_nick_name=user.nickname()
        ga_url=''
        data= {
           'user':user,
           'user_nick_name':user_nick_name,
           'ga_url':ga_url,
           'page':'enter',
           'mydata':'1'
         }
    else:
        user_has_account=0
        user_nick_name='???'
        ga_url=users.create_login_url(self.request.uri);
        data= {
           'user':user,
           'user_nick_name':user_nick_name,
           'ga_url':ga_url,
           'page':'enter',
         }
    self.response.out.write(template.render('enter.html',data))


class AnketaHandler(webapp.RequestHandler):  
    def get(self):
        user = users.get_current_user()
        if user:    
            user_nick_name=user.nickname()
            user_url='profile.html'
        else:
            user_nick_name='no_name_user'
            user_url=users.create_login_url(self.request.uri);
        data= {'page':'anketa',
               'user_nick_name':user_nick_name,
               'user_url':user_url,
               'mydata':'1'
              }
        self.response.out.write(template.render('anketa.html',data))
    

class SearchHandler(webapp.RequestHandler): 
    def get(self):
        user = users.get_current_user()
        if user:
            data= {'page':'search','mydata':'1'}
        else: 
            data= {'page':'search',}
        self.response.out.write(template.render('search.html',data))

class ContactHandler(webapp.RequestHandler): 
    def get(self):
        key   =self.request.get('k')
        if key:
            data= {'page':'contact','key':key}
        else:
            data= {'page':'contact'} 
        self.response.out.write(template.render('contact.html',data))

class KursHandler(webapp.RequestHandler):
    def get(self):
        data= {'page':'kurs'}
        self.response.out.write(template.render('kurs.html',data))

class ENHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            data= {'page':'en','mydata':'1'}
        else:                
            data= {'page':'en'}
        self.response.out.write(template.render('economic_news.html',data))

class LibHandler(webapp.RequestHandler): 
    def get(self):
        data= {'page':'lib'}
        self.response.out.write(template.render('lib.html',data))

class ProfileHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user: 
            myfirms=Anketa.gql("WHERE owner  = :curuser",curuser=user)
            data= {'page':'profile','myfirms':myfirms,'mydata':'1'}
            self.response.out.write(template.render('profile.html',data))
        else:
            self.redirect('/enter.html')
      


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/index.html',  MainHandler),
                                        ('/enter.html',  EnterHandler),
                                        ('/search.html', SearchHandler),
                                        ('/anketa.html', AnketaHandler),
                                        ('/contact.html',ContactHandler),   
                                        ('/kurs.html',   KursHandler),
                                        ('/economic_news.html',ENHandler),
					('/lib.html',LibHandler),
					('/profile.html',ProfileHandler)					
                                        ],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
