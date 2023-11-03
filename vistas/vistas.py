from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import db, Oferta, OfertaSchema, OfertaSchemaGet
from dotenv import load_dotenv
from os import getenv
import json
import requests
import logging


oferta_schema = OfertaSchema()

oferta_schema_get = OfertaSchemaGet()
def set_env():
    load_dotenv()
    global USERS_PATH
    USERS_PATH = getenv("USERS_PATH")

logging.basicConfig(level=logging.DEBUG)
set_env()

def validate_token(request):
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        token = bearer.split()[1]
        current_app.logger.info('%s token',str(token))
        endpoint_user= str("http://" + USERS_PATH + "/users/me")
        headers_users = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(str(token))}
        comprobar_auth = requests.get(endpoint_user, headers=headers_users)
        current_app.logger.info('%s statuscode',comprobar_auth.status_code)
        if comprobar_auth.status_code != 200:
            return "Invalid Token"  
        datos_user= comprobar_auth.json()
        user_id = datos_user["id"]
        current_app.logger.info('%s userid',user_id)
        return user_id

        
class VistaOferta(Resource):

    def post(self):
        my_json_request = request.json
        id = validate_token(request)
        try:
            user_id = int(id)
        except ValueError:
            return {'message': 'Invalid Token'}, 401
        try:
             my_json_request["userId"] = user_id
             # Validate request body against schema data types
             result = oferta_schema.load(my_json_request)
        except ValidationError as err:
            for item in err.messages.items():
                if item[1][0] == "Missing data for required field.":
                    return {'message': 'Missing fields'}, 400
            return f'{err.messages}' , 412
                
       
        nueva_oferta = Oferta(postId = my_json_request["postId"],
                                userId = user_id,
                                description = my_json_request["description"],
                                size = my_json_request["size"],
                                fragile = my_json_request["fragile"],
                                offer = my_json_request["offer"])
        db.session.add(nueva_oferta)
        db.session.commit()


        return oferta_schema.dump(nueva_oferta), 201

    

    def get(self):
        id = validate_token(request)
        try:
            user_id = int(id)
        except ValueError:
            return {'message': 'Invalid Token'}, 401
        post = request.args.get('post')
        filter = request.args.get('filter')
        if  post is not None:
            try:
                post = int(post)
                if  post <= 0:
                    return {'message': 'Invalid post id'}, 400
            except ValueError:
                return {'message': 'Invalid post id'}, 400
        if filter is not None:
            if filter != "me":
                return {'message': 'Invalid filter'}, 400
        if post is None and filter == "me":
            return oferta_schema_get.dump(Oferta.query.filter(Oferta.userId == user_id).all(), many=True)
        else:
            if post is not None and filter == "me":
                return oferta_schema_get.dump(Oferta.query.filter(Oferta.userId == user_id, Oferta.postId == post).all(), many=True)
            else:
                if post is None and filter is None:
                        return oferta_schema_get.dump(Oferta.query.all(), many=True)    
                else:
                    if post is not None and filter != "me":
                        return oferta_schema_get.dump(Oferta.query.filter(Oferta.postId == post).all(), many=True)

                       
class VistaOfertaById(Resource):

    def get(self, id):
        id_token = validate_token(request)
        try:
            user_id = int(id_token)
        except ValueError:
            return {'message': 'Invalid Token'}, 401
        try:
            id = int(id)
            if  id <= 0:
                return {'message': 'Invalid id'}, 400
        except ValueError:
            return {'message': 'Invalid id'}, 400
        oferta = Oferta.query.filter(Oferta.id == id).first()
        if oferta is None:
            return {'message': 'Offer not found'}, 404
        return oferta_schema_get.dump(oferta), 200
    
class Health(Resource):
    def get(self):
        return "pong", 200