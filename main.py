# chat conversation
import json
import pymysql
import requests
import http.client
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")
    print("REQUEST: "+str(request.json))

    #try:
    cursor = connection.cursor()
    
    nombre = str(request.json['nombre'])
    apellido = str(request.json['apellido'])
    rut = str(request.json['rut'])
    genero = str(request.json['genero'])
    email = str(request.json['email'])
    telefono = str(request.json['telefono'])
    carrera = str(request.json['carrera'])
    jornada = str(request.json['jornada'])
    direccion = str(request.json['direccion'])
    region = str(request.json['region'])
    comuna = str(request.json['comuna'])
    tipo_usuario = 'profesional'
    contrasena = 'pass_generica'

    #campus = str(request.json['campus'])
    status = str(request.json['status'])
    especialidad = str(request.json['especialidad'])
    
    fechaNacimiento = datetime.strptime(request.json['fechaNacimiento'], '%d-%m-%Y')
    anoIngresoCarrera = datetime.strptime(request.json['anoIngresoCarrera'], '%d-%m-%Y')
    
    sql_insertar = 'INSERT INTO '+DB_DDBB+'.usuarios'+'''
                    (contrasena, nombre, apellido, rut, fecha_nacimiento, genero, email, telefono, carrera, anoIngresoCarrera, jornada, direccion, region, comuna, tipo_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
    print('INSERT 1:'+sql_insertar)
    print(contrasena, nombre, apellido, rut, fechaNacimiento, genero, email, telefono, carrera, anoIngresoCarrera, jornada, direccion, region, comuna, tipo_usuario)
    cursor.execute(sql_insertar,(contrasena, nombre, apellido, rut, fechaNacimiento, genero, email, telefono, carrera, anoIngresoCarrera, jornada, direccion, region, comuna, tipo_usuario))
    
    #rescatar id profesional
    sql = 'select id from '+DB_DDBB+'.usuarios order by fechamod desc limit 1'
    cursor.execute(sql)
    idd = cursor.fetchone()
    print(str(idd))

    #rescatar id especialidad
    sql = 'select id from '+DB_DDBB+'.especialidades where especialidad="'+especialidad+'";'
    cursor.execute(sql)
    idesp = cursor.fetchone()
    print(str(idesp))

    sql_insertar = 'INSERT INTO '+DB_DDBB+'.especialidad_user'+'''
                    (usuario_id, id_especialidad)
                    VALUES (%s, %s);
                    '''

    print('INSERT 2:'+sql_insertar)
    cursor.execute(sql_insertar,(idd, idesp))
    
    connection.commit()

    retorno = {
        "estado":True,
        "detalle":"success"
    }

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {
    #        "estado":False,
    #        "detalle":"fail!!"
    #    }
    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')