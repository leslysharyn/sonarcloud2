import json
from unittest import TestCase
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token
from nose.tools import assert_list_equal, assert_true
from faker import Faker
from faker.generator import random

from app import app, db
import os





class TestOferta(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        db.session.begin_nested()
        self.user_id = self.data_factory.random_number(digits=2)
        self.token = create_access_token(identity=self.user_id)

    
    def tearDown(self):
        db.session.rollback()

    @patch("vistas.vistas.validate_token")
    def test_crear_oferta(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id

        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_ofertas= "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_ofertas,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)
        respuesta_al_crear_oferta = json.loads(solicitud_nueva_oferta.get_data())
        user_id_nueva_oferta = respuesta_al_crear_oferta["userId"]

        self.assertEqual(solicitud_nueva_oferta.status_code, 201)
        self.assertEqual(user_id_nueva_oferta, self.user_id)
    
    @patch("vistas.vistas.validate_token")
    def test_crear_oferta_faltando_parametros(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_ofertas= "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_ofertas,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)

        self.assertEqual(solicitud_nueva_oferta.status_code, 400)

    @patch("vistas.vistas.validate_token")
    def test_crear_oferta_valores_no_esperados(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": -25
        }

        endpoint_ofertas= "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_ofertas,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)

        self.assertEqual(solicitud_nueva_oferta.status_code, 412)


    @patch("vistas.vistas.validate_token")
    def test_obtener_oferta_por_id(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        description = self.data_factory.text(25)
        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": description,
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_carreras = "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_carreras,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)
        respuesta_al_crear_oferta = json.loads(solicitud_nueva_oferta.get_data())
        
        id_nueva_oferta = respuesta_al_crear_oferta["id"]

        endpoint_oferta_por_id = "/offers/{}".format(id_nueva_oferta)
        solicitud_oferta_por_id = self.client.get(endpoint_oferta_por_id, headers=headers)
        respuesta_oferta_por_id = json.loads(solicitud_oferta_por_id.get_data())
        res_description = respuesta_oferta_por_id["description"]

        self.assertEqual(solicitud_oferta_por_id.status_code, 200)
        self.assertEqual(res_description, description)

    @patch("vistas.vistas.validate_token")
    def test_obtener_oferta_por_id_no_existente(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        description = self.data_factory.text(25)
        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": description,
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_carreras = "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_carreras,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)
        respuesta_al_crear_oferta = json.loads(solicitud_nueva_oferta.get_data())
        
        id_nueva_oferta = respuesta_al_crear_oferta["id"]

        endpoint_oferta_por_id = "/offers/{}".format(id_nueva_oferta + self.data_factory.random_number(digits=12) )
        solicitud_oferta_por_id = self.client.get(endpoint_oferta_por_id, headers=headers)

        self.assertEqual(solicitud_oferta_por_id.status_code, 404)
    
    @patch("vistas.vistas.validate_token")
    def test_obtener_oferta_por_id_valor_no_valido(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        endpoint_oferta_por_id = "/offers/{}".format(self.data_factory.text(5))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_oferta_por_id = self.client.get(endpoint_oferta_por_id, headers=headers)

        self.assertEqual(solicitud_oferta_por_id.status_code, 400)

    @patch("vistas.vistas.validate_token")
    def test_obtener_mis_ofertas(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        nueva_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_carreras = "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_carreras,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)
        respuesta_al_crear_oferta = json.loads(solicitud_nueva_oferta.get_data())

        id_oferta_creada = respuesta_al_crear_oferta["id"]

        another_oferta = {
            "postId": self.data_factory.random_number(digits=2),
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        self.client.post(endpoint_carreras,
                                                   data=json.dumps(another_oferta),
                                                   headers=headers)
        
        res_oferta = None
        endpoint_mis_ofertas = "/offers?filter=me"
        solicitud_mis_ofertas = self.client.get(endpoint_mis_ofertas, headers=headers)
        respuesta_mis_ofertas = json.loads(solicitud_mis_ofertas.get_data())

        for oferta in respuesta_mis_ofertas:
            if oferta["id"] == id_oferta_creada:
                res_oferta = oferta["id"]
                break
        
        self.assertEqual(solicitud_mis_ofertas.status_code, 200)
        self.assertEqual(res_oferta, id_oferta_creada)
        self.assertGreaterEqual(len(respuesta_mis_ofertas), 2)

    @patch("vistas.vistas.validate_token")
    def test_obtener_ofertas_por_post(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        postId = self.data_factory.random_number(digits=2)
        nueva_oferta = {
            "postId": postId,
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        endpoint_carreras = "/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_oferta = self.client.post(endpoint_carreras,
                                                   data=json.dumps(nueva_oferta),
                                                   headers=headers)
        respuesta_al_crear_oferta = json.loads(solicitud_nueva_oferta.get_data())

        offerid_oferta_creada = respuesta_al_crear_oferta["id"]

        another_oferta = {
            "postId": postId,
            "description": self.data_factory.text(25),
            "size": "SMALL",
            "fragile": True,
            "offer": self.data_factory.random_number(digits=5)
        }

        self.client.post(endpoint_carreras,
                          data=json.dumps(another_oferta),
                           headers=headers)
        
        endpoint_mis_ofertas = f"/offers?post={postId}"
        solicitud_mis_ofertas = self.client.get(endpoint_mis_ofertas, headers=headers)
        respuesta_mis_ofertas = json.loads(solicitud_mis_ofertas.get_data())

        
        self.assertEqual(solicitud_mis_ofertas.status_code, 200)
        self.assertGreaterEqual(len(respuesta_mis_ofertas), 2)
    
    @patch("vistas.vistas.validate_token")
    def test_obtener_ofertas_por_post_valor_no_esperado(self, mock_validate_token):
        mock_validate_token.return_value = self.user_id
        postId = self.data_factory.text(5)
        endpoint_mis_ofertas = f"/offers?post={postId}"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        solicitud_mis_ofertas = self.client.get(endpoint_mis_ofertas, headers=headers)
        self.assertEqual(solicitud_mis_ofertas.status_code, 400)

