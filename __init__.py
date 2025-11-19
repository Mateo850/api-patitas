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
        historial_medico_id = data['historial_medico_id']
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
            'historial_medico_id':historial_medico_id,
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
    

#registrar historial medico
@app.route('/registro-historial-medico', methods=['POST'])
def registro_historial_medico():
    try:
        data = request.get_json()
        id_animal= data['id_animal']
        id_refugio =data['id_refugio']
        castrado = data['castrado']
        fecha_revision = data['fecha_revision']
        peso = data['peso']
        enfermedades = data['enfermedades']
        tratamiento = data['tratamiento']
       

        #crear historial medico
 
        ref = db.reference('historialMedico')
        nuevo_hmedico = ref.push()
        nuevo_hmedico.set({
            'castrado': castrado,
            'fecha_revision': fecha_revision,
            'peso': peso,
            'enfermedades':enfermedades,
            'tratamiento': tratamiento,
            
        })

        #actualizar el id del historial en el animal correspondiente

        historial_medico_id = nuevo_hmedico.key
        animal_ref = db.reference('animales/'+id_refugio+'/'+id_animal)

        animal_ref.update({'historial_medico_id':historial_medico_id})


 
        return jsonify({"message": "datos medicos registrado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API historial medico:", e)
        return jsonify({"error": str(e)}), 500


#actualizar historial medico
@app.route('/update-historial-medico', methods=['POST'])
def update_historial_medico():
    try:
        data = request.get_json()
        id_historial= data['id_historial']
        castrado = data['castrado']
        fecha_revision = data['fecha_revision']
        peso = data['peso']
        enfermedades = data['enfermedades']
        tratamiento = data['tratamiento']
     

        #actualizar historial medico
 
        ref = db.reference('historialMedico/'+id_historial)
        ref.update({
            'castrado': castrado,
            'fecha_revision': fecha_revision,
            'peso': peso,
            'enfermedades':enfermedades,
            'tratamiento': tratamiento,
          
        })

 
        return jsonify({"message": "datos medicos registrado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API historial medico:", e)
        return jsonify({"error": str(e)}), 500



#actualizar  animal
@app.route('/update-animal', methods=['POST'])
def update_animal():
    try:
        data = request.get_json()
        id_refugio= data['id_refugio']
        id_animal= data['id_animal']
        
        nombre = data['nombre']
        especie = data['especie']
        sexo = data['sexo']
        historial_medico_id = data['historial_medico_id']
        estado_salud = data['estado_salud']
        raza = data['raza']
        fecha_ingreso = data['fecha_ingreso']
 
        ref = db.reference('animales/'+id_refugio+'/'+id_animal)
        ref.update({
            'nombre': nombre,
            'especie': especie,
            'sexo': sexo,
            'raza':raza,
            'historial_medico_id':historial_medico_id,
            'estado_salud': estado_salud,
            'fecha_ingreso': fecha_ingreso
        })
        
 
        return jsonify({"message": "Animal actualizado correctamente"}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500


#actualizar  animal
@app.route('/delete-animal', methods=['POST'])
def delete_animal():
    try:
        data = request.get_json()
        id_refugio= data['id_refugio']
        id_animal= data['id_animal']
        historial_medico_id = data['historial_medico_id']
        
 
        ref = db.reference('animales/'+id_refugio+'/'+id_animal)
        ref.delete()

        #eliminar historial medico asociado
        if historial_medico_id != "":
            historial_ref = db.reference('historialMedico/'+historial_medico_id)
            historial_ref.delete()
        
 
        return jsonify({"message": "Animal eliminado correctamente"}), 200
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
    

#obtener historial medico
@app.route('/historial-medico/<string:id_historial>', methods=['GET'])
def historial_medico(id_historial):
    try:
        ref = db.reference('historialMedico/'+id_historial)
        data = ref.get()

        if not data:
            return jsonify({"error": "Historial médico no encontrado"}), 404

 
        return jsonify(data), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API obtencion historial medico:", e)
        return jsonify({"error": str(e)}), 500

#obtener lista animales con problemas de peso
@app.route('/animales/<string:id_refugio>', methods=['GET'])
def problemas_peso(id_refugio):
    try:
        ref = db.reference(f'animales/{id_refugio}')
        data = ref.get()

        if not data:
            return jsonify({"animales_bajo_peso": []}), 200

        animales_bajo_peso = []

        
        for id_animal, animal in data.items():
            try:
                peso = float(animal.get("peso", 0))
            except:
                peso = 0

            
            if peso < 8.0:  
                animales_bajo_peso.append({
                    "id": id_animal,
                    "nombre": animal.get("nombre", ""),
                    "especie": animal.get("especie", ""),
                    "raza": animal.get("raza", ""),
                    "peso": peso,
                })

        return jsonify({animales_bajo_peso}), 200
    except Exception as e:
        print("ERROR EN LA EJECUCIÓN DE LA API:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

