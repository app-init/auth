#!/bin/python3.5

import sys

# preventing __pycache__ from being created
sys.dont_write_bytecode = True

from flask import Flask, redirect, jsonify, make_response, send_file, request, g
from querystring_parser import parser
import urllib

import json
import os
import traceback

# sys.stdout = open("/home/cee-tools/logs/debug.log", "a+")

from werkzeug.contrib.fixers import ProxyFix

# sys.path.append("/home/cee-tools/api/")
# sys.path.append("/home/cee-tools/apps/")

controller_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.abspath(os.path.join(controller_path))

if base_path not in sys.path:
   sys.path.append(base_path)

from views import saml
from middleware import token, json
from views.lib.responses import HttpResponse, HttpResponseBadRequest, HttpResponseInternalServerError

from webplatform_cli.lib.config import Settings
from webplatform_cli.lib.db import Manager

manager = Manager()
settings = Settings(path=base_path, verify=False)

modules = Modules(settings, manager)
# manager = modules.manager

app = Flask(__name__)
# app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)
app.use_x_sendfile = True

@app.before_request
def token_middleware():
   manager.set_hostname(request.host)

   session = token.process_request(request, manager)

   if session != None:
      manager.set_user_uid(session.uid)

   g.settings = settings
   g.session = session

@app.route("/callback/", methods=['POST', 'GET'])
def saml_auth():
   if request.method == 'GET':
      return saml.get(request)
   else:
      return saml.post(request)

@app.route("/metadata")
def metadata():
   protocol = request.headers['X-Forwarded-Proto']
   port = request.headers['X-Nginx-Port']
   host = request.headers['Host'].split(":")[0]

   if "X-Nodejs" in request.headers:
      if "0.0.0.0" in host:
         host = host.replace("0.0.0.0:8080", "localhost")
         if "X-Nodejs-Host" in request.headers:
            host = request.headers['X-Nodejs-Host']

   if port in host:
      base = (protocol, host)
      url = '%s://%s/callback/' % base
   else:
      base = (protocol, host, port)
      url = '%s://%s:%s/callback/' % base

   if len(request.args) > 0:
      is_config = request.args.get("config", False)
      if is_config:
         config_file = open(settings.get_config("flask")['saml-settings'] + "/saml.json")
         config = json.load(config_file)
         config['sp']['assertionConsumerService']['url'] = url
         config_file.close()

         config_file = open(settings.get_config("flask")['saml-settings'] + "/saml-advanced.json")
         advanced_config = json.load(config_file)
         config_file.close()

         return HttpResponse(json.dumps({"config": config, "advanced": advanced_config}, indent=2))

   return saml.metadata(request)