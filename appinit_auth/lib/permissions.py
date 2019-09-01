from appinit.lib.db import Manager

class PermissionManager(object):
   def __init__(self, session):
      self.manager = Manager()
      self.db = self.manager.db('appinit') 
      self.session = session
      # self.settings = settings

   def get_route_uids(self, route, permission):
      route = PermissionsRoute(self.db, route)
      return route.get_uids(permission)

   def list_user_permissions(self):
      user = PermissionsUser(self.db, self.session.uid)
      return user.list_permissions()

   def get_route(self, route=None):
      permissions = self.list_user_permissions()
      
      if route == None:
         return permissions
      else:
         if route in permissions:
            return permissions[route]
         else:
            return []
   
class Permission(object):
   def __init__(self):
      pass

class PermissionsRoute(object):
   def __init__(self, db, route):
      self.route = route
      self.db = db

   # users.permissions.get
   def get_uids(permission):
      pipeline = [
         { "$match": {"route": self.route}},
         { "$unwind": "$permissions" },
         { "$group":
            {
               "_id": "$permissions",
               "uids": {
                  "$addToSet": "$uid",
               },
            }
         },
         { "$match":
            {
               "_id": permission,
            }
         },
      ]

      cursor = self.db.permissions.aggregate(pipeline)

      if cursor != None:
         for i in cursor:
            return i['uids']

      return None

   # permissions.applications.add
   def add(self, uid, permission):
      cursor = self.db.permissions.find_one({
         "route": self.route,
         "uid": uid,
      })

      if cursor is None:
         add_user.call(uid=uid, route=self.route)

      self.db.permissions.update(
         {
            "route": self.route,
            "uid": kwargs["uid"]
         },
         {
            "$push": {
               "permissions": permission
            }
         }
      )

      return get_route.call(route=self.route)

class PermissionsUser(object):
   def __init__(self, db, uid):
      self.uid = uid
      self.db = db
      self.manager = Manager()

   def list_permissions(self):
      permissions = {}

      routes = self.manager.get_route()
      routes.append({"name": "system"})
      for route in routes:

         if route['name'] != "system":
            list_name = route['api']['name'].split("_")
            camel_case = ''.join([list_name[x].title() for x in range(1, len(list_name))])
            name = list_name[0] + camel_case
         else:
            name = route['name']

         permissions[name] = {}

         all_permissions = self.db.permissions.find({"route": route['name']}).distinct("permissions")

         user_permissions = self.db.permissions.find_one({"uid": self.uid, "route": route['name']})

         if user_permissions != None:
            all_true = False
            if user_permissions['route'] == route['name']:
               all_true = "admin" in user_permissions['permissions']

            for p in user_permissions['permissions']:
               key = 'is_' + p
               if all_true:
                  permissions[name][key] = True
               elif p in all_permissions:
                  permissions[name][key] = True
               else:
                  permissions[name][key] = False

      return permissions

class PermissionsModule(object):
   def __init__(self):
      pass