import os
import firebase_admin
from flask import Flask, json, request, jsonify
from firebase_admin import  credentials,db, auth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



#cred = credentials.Certificate("Key.json")

 
#firebase_admin.initialize_app(cred, {
#    'databaseURL': 'https://admin-patitas-default-rtdb.firebaseio.com/'})

firebase_key = os.environ.get("FIREBASE_KEY")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app( cred, {
    'databaseURL': 'https://admin-patitas-default-rtdb.firebaseio.com/'})



#registrar funcion de prueba

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()

        name = data['name']
        email = data['email']


        ref = db.reference('prueba')
        new_email_ref = ref.push()
        new_email_ref.set({
            'name': name,
            'email': email
        })
        
        return jsonify({"message": "datos de prueba agregados correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCION DE LA API: {e}")
        return jsonify({"error": str(e)}), 500
    
#registrar nuevo usuario
@app.route('/register', methods=['POST'])
def user_register():
    try:
        data = request.get_json()
        print(data)

        
        email = data['email']
        password = data['password']


        auth.create_user(
            email=email,
            password=password
        )


        print("USUARIO CREADO CORRECTAMENTE: {user.uid}")
        return jsonify({"message": "usuario agregado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCION DE LA API: ",e)
        return jsonify({"error": str(e)}), 500

#registrar nuevo animal
@app.route('/registro-animal', methods=['POST'])
def registro_animal():
    try:
        data = request.get_json()
        id_refugio= data['id_refugio']
        nombre = data['nombre']
        especie = data['especie']
        sexo = data['sexo']
        estado_salud = data['estado_salud']
        raza = data['raza']
        fecha_ingreso = data['fecha_ingreso']
 
        ref = db.reference('animales/'+id_refugio)
        nuevo_animal_ref = ref.push()
        nuevo_animal_ref.set({
            'nombre': nombre,
            'especie': especie,
            'sexo': sexo,
            'raza':raza,
            'estado_salud': estado_salud,
            'fecha_ingreso': fecha_ingreso
        })
 
        return jsonify({"message": "Animal registrado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500

#registrar nuevo refugio
@app.route('/registro-refugio', methods=['POST'])
def registro_refugio():
    try:
        data = request.get_json()
        nombre = data['nombre']
        direccion = data['direccion']
        id_usuario = data['id_usuario']
      
 
        ref = db.reference('refugios')
        nuevo_refugio_ref = ref.push()
        nuevo_refugio_ref.set({
            'id_usuario': id_usuario,
            'nombre': nombre,
            'direccion': direccion,
            
        })
 
        return jsonify({"message": "refugio registrado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500
    
#obtener datos animales
@app.route('/animales/<string:id_refugio>', methods=['GET'])
def obtener_animales(id_refugio):
    try:
        ref = db.reference('animales/'+id_refugio)
        data = ref.get()
        return jsonify(data), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500
    
#obntener refugios asociados
@app.route('/refugios/<string:id_user>', methods=['GET'])
def obtener_refugios(id_user):
    try:
        ref = db.reference('refugios')
        data = ref.get()
        refugios_usuario= {}
        
        for key_refugio, datos in data.items():
            if datos.get('id_usuario') == id_user:
                refugios_usuario[key_refugio]= datos
                print(key_refugio, '=', datos)

        return jsonify(refugios_usuario), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500
    

#obtener informacion de un usuario
@app.route('/usuarios/<string:id_user>', methods=['GET'])
def obtener_usuario(id_user):
    try:
        usuario = auth.get_user(uid=id_user)
        data ={
            'uid': usuario.uid,
            'email': usuario.email,

        }
        
        return jsonify(data), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
