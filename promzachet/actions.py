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

# -*- condig: utf-8 -*-

import wsgiref.handlers
#import site_models
from google.appengine.api import mail 
from datetime import datetime, date, time
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from site_models import *

           
def getBaseData(actHand,user):
    dolg_type     = int(actHand.request.get('dolg_type'))
    if dolg_type:
        items_1 = Dolg_iam.all().filter("dolg_type =", dolg_type)
        items_2 = Dolg_me.all().filter("dolg_type =", dolg_type)        
        data={'a_key':'-1','items_1':items_1,'items_2':items_2,' cur_anketa_key':'-1'} 
        actHand.response.out.write(template.render('profile_ds.tp',data))
        pass 

def getProfileData(actHand,user):
    my_firm_key   = actHand.request.get('my_firm_key')
    my_firm       = actHand.request.get('firm_name')
    dolg_kind     = int(actHand.request.get('dolg_kind'))                              
    #anketa_firm = Anketa.gql("WHERE firm_name=:f_name AND owner=:cur_user", f_name=my_firm, cur_user=user)
    if my_firm_key and my_firm_key != '-1':
        #cur_anketa_key=db.Key(my_firm_key)
        #cur_anketa_key=db.get(db.Key(my_firm_key))
        cur_anketa_key=db.get(my_firm_key)
        #actHand.response.out.write(cur_anketa_key)
    else:
        if my_firm =="-1":
            anketa_firm = Anketa.all().filter("owner =",user)
            cur_anketa_key = anketa_firm.get()
        else:
            anketa_firm = Anketa.all().filter("firm_name =",my_firm).filter("owner =",user)
            cur_anketa_key = anketa_firm.get()
    #actHand.response.out.write(cur_anketa_key) 
    if cur_anketa_key:                                      
        if dolg_kind == 1:
            if my_firm =="-1":
                items = Dolg_me.all().filter("owner =", user)
            else:
                items = Dolg_me.all().filter("anketa_key =", cur_anketa_key)                
        if dolg_kind == 2:
            if my_firm =="-1":
                items = Dolg_iam.all().filter("owner =", user)
            else:
                items = Dolg_iam.all().filter("anketa_key =", cur_anketa_key)
        if dolg_kind == 3:
            if my_firm =="-1":
                items = Dolg_give.all().filter("owner =", user)
            else:
                items = Dolg_give.all().filter("anketa_key =", cur_anketa_key)                
        data={'a_key':str(cur_anketa_key.key()),'items':items,' cur_anketa_key':cur_anketa_key} 
        actHand.response.out.write(template.render('profile_ds.tp',data))
    else:
        data="[{'error':'1','mes':'No data'}]" 
        actHand.response.out.write(data)                                        
                
def delProfileData(rec_key):
    rec=db.get(db.Key(rec_key))
    if rec:
        rec.delete()
                  
class ActionsHandler(webapp.RequestHandler):
            
    def post(self):
        user = users.get_current_user()
        f_name=''
        act = self.request.get('action')
        if act == 'search_data':
            getBaseData(self,user);
            return 
        if act == 'contact':
            mes_whom   =self.request.get('mes_whom')
            mes_subj   =self.request.get('mes_subj')
            mes_txt    =self.request.get('mes_txt')
            dolg_key   =self.request.get('dolg_key')
            if dolg_key:
                dolg_key_str=dolg_key
            else:
                dolg_key_str="";    
            if user:
                nickname =user.nickname()
                emailuser=user.email()                
            else:
                nickname='Anomim_User'
                emailuser='a2772@mail.ru'
            email=emailuser
            sender = 'a2772@mail.ru'
            subject = 'Message from Promzachet site'
            body = \
            'This is mess from %s,\n\n' % nickname + \
            'his email is\n\n' + \
            '<%s>\n' % emailuser+\
            '----------------------\n'+mes_txt+'\n'+\
            'dolg key='+dolg_key_str
            mail.send_mail( sender=sender, to=email, subject=subject, body=body )
            data={'lang':'info_saved'}
            self.response.out.write(template.render('mes_out.tp',data))
            return 
        if not user:
            out_str="{'mes':'<br>Your are not registered user!'}"
        else:             
            
             f_name   =self.request.get('firm_name')
             t_mob    =self.request.get('tel_mob')
             
             if act == 'del_item':
                 del_key=self.request.get('del_key')
                 delProfileData(del_key)
                 getProfileData(self,user);
                 #out_str="{'error':'1','mes':'deleted'}"
                 #self.response.out.write(out_str)
                 return
             if act == 'profile_prop':
                 dolg_key  =str(self.request.get('dolg_key'))
                 dolg_base =int(self.request.get('dolg_base'))
                 error_state='1';
                 if dolg_base ==1:
                     #base_name='Dolg_me'
                     Dolg_me.setProp(dolg_key,user,self.request)
                     getProfileData(self,user);
                     #base_table = Dolg_me.all().filter("anketa_key =",dolg_key).filter("owner =",user)
                 if dolg_base ==2:
                     #base_name='Dolg_iam'
                     Dolg_iam.setProp(dolg_key,user,self.request)
                     getProfileData(self,user);
                     pass
                 if dolg_base ==3:
                     base_name='Dolg_give'
                 if not dolg_base in [1,2,3]:
                     error_state='-1'    
                     out_str="[{'error':'"+error_state+"'}]"
                     self.response.out.write(out_str)
                 return
             if act == 'profile_data':
                 getProfileData(self,user);
                 return                                    
             #----------------------B:Check for cur anketa by firm_name and Tel mob--------------       
             #----query=Anketa.all().filter('firm_name=', f_name.strip()).filter('owner=', user)
             query=Anketa.gql("WHERE firm_name  = '"+f_name+"' AND tel_mob = '"+t_mob+"'")      
             if query.count() <= 0:
                 a_firm="for a new firm:"
                 #------------------B:create new anketa if needed-----------               
                 acur= Anketa()
                 acur.firm_name=f_name
                 acur.owner=user
                 acur.tel_mob=t_mob
                 acur.put()
                 cur_anketa_key=acur.key()
                 #------------------E:create new anketa if needed-----------
             else:
                 a_firm="for this firm:"
                 #------------------------Find existing firm--------              
                 for a in query:
                     if a.firm_name == f_name:
                         cur_anketa_key=a.key()
                         break
                 #----------------------E:Check for cur anketa--------------                                        
                 #logging.debug("Anketa created") 
             if act == 'dolg_me':             
                 dme= Dolg_me()
                 dme.anketa_key=cur_anketa_key
                 dme.dolg_status =int(str(self.request.get('dolg_status')))
                 dme.dolgnik_name=self.request.get('dolgnik_name')
                 dme.dolg_type   =int(str(self.request.get('dolg_type')) )
                 dme.dolg_name   =self.request.get('dolg_name')
                 dme.dolg_sum    =float(self.request.get('dolg_sum'))
                 dme.dolg_valuta =int(str(self.request.get('dolg_valuta')))
                 dme.dolg_date   =datetime.strptime(self.request.get('dolg_date'), "%d.%m.%Y")
                 dme.owner=user
                 dme.put()          
                 pass       
             if act == 'dolg_iam':
                 diam= Dolg_iam()
                 diam.anketa_key=cur_anketa_key
                 diam.dolg_status =int(str(self.request.get('dolg_status')))
                 diam.dolgnik_name=self.request.get('dolgnik_name')
                 diam.dolg_type   =int(str(self.request.get('dolg_type')) )
                 diam.dolg_name   =self.request.get('dolg_name')
                 diam.dolg_sum    =float(self.request.get('dolg_sum'))
                 diam.dolg_valuta =int(str(self.request.get('dolg_valuta')))
                 diam.dolg_date   =datetime.strptime(self.request.get('dolg_date'), "%d.%m.%Y")
                 diam.owner=user
                 diam.put()
                 pass
             if act == 'dolg_give':
                 dgive= Dolg_give()
                 dgive.anketa_key  =cur_anketa_key
                 dgive.dolg_type   =int(str(self.request.get('dolg_type')) )
                 dgive.dolg_name   =self.request.get('dolg_name')
                 dgive.dolg_sum    =float(self.request.get('dolg_sum'))
                 dgive.dolg_valuta =int(str(self.request.get('dolg_valuta')))
                 dgive.owner=user
                 dgive.put()
                 pass
        data={'lang':'saved'}
        self.response.out.write(template.render('mes_out.tp',data))

   
    
def main():
    application = webapp.WSGIApplication([('/action', ActionsHandler),                                         
                                         ],
                                        debug=True)  
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()
