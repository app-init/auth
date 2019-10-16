from appinit.lib.db import Manager
from appinit_auth.lib.permissions import PermissionManager
from appinit_backend.lib.modules import Modules

from datetime import datetime, timedelta
import hashlib

class BaseUser:
   def __init__(self, session, db):
      self.db = db
      self.uid = session.uid
      self.session = session
      self.permissions_mgr = PermissionManager(session)

      self.metadata = self.db.users.find_one({"uid": self.uid})

   def get_uid(self):
      return self.uid

   def get_sessions(self):
      return self.session.get_all_sessions()

   # def set_permissions(self, permissions):
   #    self.permissions = permissions

   # def get_permissions(self, app=None):
   #    if app == None:
   #       return self.permissions
   #    else:
   #       if app in self.permissions:
   #          return self.permissions[app]
   #       else:
   #          return []

   # def get_session(self, **kwargs):
   #    return self.session.get_session(**kwargs)

   # def get_all_sessions(self, uid):
   #    return self.session.get_session(uid=uid)

   # def validate_session(self, *args):
   #    return self.session.validate(*args)

   def get_user(self):
      sessions = self.session.get_all_sessions()
      permissions = self.permissions_mgr.list_user_permissions()
      token = self.session.token

      lastUpdated = datetime.utcnow() - timedelta(hours=24)
      update = True

      # Only allow an update when cache hasn't updated in the last 24 hours
      if self.metadata and lastUpdated <= self.metadata['lastUpdated']:
         update = False

      return {
         "sessions": sessions,
         "permissions": permissions,
         "token": token,
         "uid": self.uid,
         "metadata": self.metadata,
         "update": update
      }

   def set_user(self):
      pass

def get_picture(email):
   email = email.encode('utf-8')
   return "https://secure.gravatar.com/avatar/" + hashlib.md5(email).hexdigest() + "?s=100&d=identicon"
