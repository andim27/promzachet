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




import wsgiref.handlers
from datetime import datetime, date, time
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Anketa(db.Model):
    owner     = db.UserProperty()
    firm_name = db.StringProperty()
    tel_mob   = db.StringProperty()
    created   = db.DateTimeProperty(auto_now_add=True)
    #dolg_me_key   = db.ReferenceProperty()
    #dolg_iam_key  = db.ReferenceProperty()
    #dolg_give_key = db.ReferenceProperty()

class Dolg_me(db.Model):
    anketa_key   = db.ReferenceProperty()
    dolg_status  = db.IntegerProperty()
    dolgnik_name = db.StringProperty()
    dolg_type    = db.IntegerProperty() 
    dolg_name    = db.StringProperty()
    dolg_sum     = db.FloatProperty()
    dolg_valuta  = db.IntegerProperty()
    dolg_date    = db.DateTimeProperty()
    owner        = db.UserProperty()
    
    @staticmethod
    def setProp(dolg_key,user,request):
        rec=db.get(db.Key(dolg_key))
        rec.dolg_status =int(str(request.get('dolg_status')))
        rec.dolgnik_name=request.get('dolgnik_name')
        rec.dolg_type   =int(str(request.get('dolg_type')) )
        rec.dolg_name   =request.get('dolg_name')
        rec.dolg_sum    =float(request.get('dolg_sum'))
        rec.dolg_valuta =int(str(request.get('dolg_valuta')))
        rec.dolg_date   =datetime.strptime(request.get('dolg_date'), "%d.%m.%Y")
        rec.owner=user
        rec.put()
        return      
       

class Dolg_iam(db.Model):
    anketa_key   = db.ReferenceProperty()
    dolg_status  = db.IntegerProperty()
    dolgnik_name = db.StringProperty()
    dolg_type    = db.IntegerProperty() 
    dolg_name    = db.StringProperty()
    dolg_sum     = db.FloatProperty()
    dolg_valuta  = db.IntegerProperty()
    dolg_date    = db.DateTimeProperty()
    owner        = db.UserProperty()
    
    @staticmethod
    def setProp(dolg_key,user,request):
        rec=db.get(db.Key(dolg_key))        
        rec.dolg_status =int(str(request.get('dolg_status')))
        rec.dolgnik_name=request.get('dolgnik_name')
        rec.dolg_type   =int(str(request.get('dolg_type')) )
        rec.dolg_name   =request.get('dolg_name')
        rec.dolg_sum    =float(request.get('dolg_sum'))
        rec.dolg_valuta =int(str(request.get('dolg_valuta')))
        rec.dolg_date   =datetime.strptime(request.get('dolg_date'), "%d.%m.%Y")
        rec.owner=user
        rec.put()
        return  
    

class Dolg_give(db.Model):
    anketa_key   = db.ReferenceProperty()
    dolg_type    = db.IntegerProperty()
    dolg_name    = db.StringProperty()
    dolg_sum     = db.FloatProperty()
    dolg_valuta  = db.IntegerProperty()
    owner        = db.UserProperty()
