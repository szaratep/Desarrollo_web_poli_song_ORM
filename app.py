# app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import *

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)  # habilita migraciones (Alembic)

    # -------- Health --------
    @app.get("/api/health")
    def health():
        return {"ok": True}

    # =====================================================
    #                  USUARIOS CRUD
    # =====================================================
    @app.post("/api/usuarios")
    def create_usuarios():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()

        # Verificar si es lista o un solo objeto
        if isinstance(data, dict):
            data = [data]  # lo convertimos en lista para manejar ambos casos igual

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro en formato JSON"), 400

        usuarios_creados = []

        # Validar todos antes de insertar
        for i, item in enumerate(data, start=1):
            nombre = item.get("nombre")
            contrasena = item.get("contrasena")

            if not nombre or not contrasena:
                return jsonify(
                    error=f"El registro #{i} no tiene todos los campos requeridos ('nombre', 'contrasena')"
                ), 400

            u = Usuario(nombre=nombre, contrasena=contrasena)
            usuarios_creados.append(u)

        # Si todos son válidos, se insertan de una vez
        try:
            db.session.add_all(usuarios_creados)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar en la base de datos: {str(e)}"), 500

        return jsonify([u.to_dict() for u in usuarios_creados]), 201


    @app.get("/api/usuarios")
    def list_usuarios():
        usuarios = Usuario.query.order_by(Usuario.id_usuario.desc()).all()
        return jsonify([u.to_dict() for u in usuarios])

    @app.get("/api/usuarios/<int:id_usuario>")
    def get_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        return jsonify(u.to_dict())

    @app.patch("/api/usuarios/<int:id_usuario>")
    def update_usuario(id_usuario):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        u = Usuario.query.get_or_404(id_usuario)
        data = request.get_json() or {}
        if "nombre" in data and data["nombre"]:
            u.nombre = data["nombre"]
        if "contrasena" in data and data["contrasena"]:
            u.contrasena = data["contrasena"]
        db.session.commit()
        return jsonify(u.to_dict())

    @app.delete("/api/usuarios/<int:id_usuario>")
    def delete_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        db.session.delete(u)
        db.session.commit()
        return jsonify(ok=True)

    # =====================================================
    #                  TELEFONOS CRUD
    # =====================================================
    @app.post("/api/telefonos")
    def create_telefonos():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        telefonos = []
        for i, item in enumerate(data, start=1):
            telefono = item.get("telefono")
            id_us = item.get("id_us")

            if not telefono or not id_us:
                return jsonify(
                    error=f"El registro #{i} no tiene los campos requeridos ('telefono', 'id_us')"
                ), 400

            telefonos.append(Telefono(telefono=telefono, id_us=id_us))

        try:
            db.session.add_all(telefonos)
            db.session.commit()
            return jsonify([t.to_dict() for t in telefonos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar teléfonos: {str(e)}"), 500

    @app.get("/api/telefonos")
    def list_telefonos():
        telefonos = Telefono.query.all()
        return jsonify([t.to_dict() for t in telefonos])

    @app.get("/api/telefonos/<string:telefono>")
    def get_telefono(telefono):
        t = Telefono.query.get_or_404(telefono)
        return jsonify(t.to_dict())

    @app.patch("/api/telefonos/<string:telefono>")
    def update_telefono(telefono):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        t = Telefono.query.get_or_404(telefono)
        data = request.get_json() or {}
        if "id_us" in data and data["id_us"]:
            t.id_us = data["id_us"]
        db.session.commit()
        return jsonify(t.to_dict())

    @app.delete("/api/telefonos/<string:telefono>")
    def delete_telefono(telefono):
        t = Telefono.query.get_or_404(telefono)
        db.session.delete(t)
        db.session.commit()
        return jsonify(ok=True)

    # =====================================================
    #                  CORREOS CRUD
    # =====================================================
    @app.post("/api/correos")
    def create_correos():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        correos = []
        for i, item in enumerate(data, start=1):
            correo = item.get("correo")
            id_us = item.get("id_us")

            if not correo or not id_us:
                return jsonify(
                    error=f"El registro #{i} no tiene los campos requeridos ('correo', 'id_us')"
                ), 400

            correos.append(Correo(correo=correo, id_us=id_us))

        try:
            db.session.add_all(correos)
            db.session.commit()
            return jsonify([c.to_dict() for c in correos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar correos: {str(e)}"), 500


    @app.get("/api/correos")
    def list_correos():
        correos = Correo.query.all()
        return jsonify([c.to_dict() for c in correos])

    @app.get("/api/correos/<string:correo>")
    def get_correo(correo):
        c = Correo.query.get_or_404(correo)
        return jsonify(c.to_dict())
    #comentari de prueba

    @app.patch("/api/correos/<string:correo>")
    def update_correo(correo):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        c = Correo.query.get_or_404(correo)
        data = request.get_json() or {}
        if "id_us" in data and data["id_us"]:
            c.id_us = data["id_us"]
        db.session.commit()
        return jsonify(c.to_dict())

    @app.delete("/api/correos/<string:correo>")
    def delete_correo(correo):
        c = Correo.query.get_or_404(correo)
        db.session.delete(c)
        db.session.commit()
        return jsonify(ok=True)

    # =====================================================
    #                  VALORACIONES CRUD
    # =====================================================
    @app.post("/api/valoraciones")
    def create_valoraciones():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        valoraciones = []
        for i, item in enumerate(data, start=1):
            id_pedido = item.get("id_pedido")
            id_us = item.get("id_us")
            descripcion = item.get("descripcion")

            # Validar campos obligatorios (no nulos)
            if not id_pedido or not id_us:
                return jsonify(
                    error=f"El registro #{i} no tiene los campos requeridos ('id_pedido', 'id_us')"
                ), 400

            valoraciones.append(
                Valoracion(id_pedido=id_pedido, id_us=id_us, descripcion=descripcion)
            )

        try:
            db.session.add_all(valoraciones)
            db.session.commit()
            return jsonify([v.to_dict() for v in valoraciones]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar valoraciones: {str(e)}"), 500

    @app.get("/api/valoraciones")
    def list_valoraciones():
        vals = Valoracion.query.all()
        return jsonify([v.to_dict() for v in vals])

    @app.get("/api/valoraciones/<int:id_val>")
    def get_valoracion(id_val):
        v = Valoracion.query.get_or_404(id_val)
        return jsonify(v.to_dict())

    @app.patch("/api/valoraciones/<int:id_val>")
    def update_valoracion(id_val):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        v = Valoracion.query.get_or_404(id_val)
        data = request.get_json() or {}
        if "descripcion" in data and data["descripcion"]:
            v.descripcion = data["descripcion"]
        if "id_pedido" in data and data["id_pedido"]:
            v.id_pedido = data["id_pedido"]
        if "id_us" in data and data["id_us"]:
            v.id_us = data["id_us"]
        db.session.commit()
        return jsonify(v.to_dict())

    @app.delete("/api/valoraciones/<int:id_val>")
    def delete_valoracion(id_val):
        v = Valoracion.query.get_or_404(id_val)
        db.session.delete(v)
        db.session.commit()
        return jsonify(ok=True)
    
    @app.post("/api/discomp3")
    def create_discomp3():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        discos= []
        for i, item in enumerate(data, start=1):
            nombre = item.get("nombre")
            duracion = item.get("duracion")
            tamano = item.get("tamano")
            precio = item.get("precio")
            id_item = item.get("id_item")

            # Validar campos obligatorios (no nulos)
            if not all([nombre, duracion, tamano, precio, id_item]):
                return jsonify(
                   error=f"El registro #{i} no tiene todos los campos requeridos ('nombre', 'duracion', 'tamano', 'precio', 'id_item')"
                ), 400

            discos.append(
                DiscoMp3(nombre=nombre, duracion=duracion, tamano=tamano,precio=precio,id_item=id_item)
            )

        try:
            db.session.add_all(discos)
            db.session.commit()
            return jsonify([v.to_dict() for v in discos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar el discomp3: {str(e)}"), 500

    @app.get("/api/discomp3")
    def list_discos():
        vals = DiscoMp3.query.all()
        return jsonify([v.to_dict() for v in vals])    
    
    @app.get("/api/discomp3/<int:id_discoMp3>")
    def get_discomp3(id_discoMp3):
        d = DiscoMp3.query.get_or_404(id_discoMp3)
        return jsonify(d.to_dict())
    
    @app.patch("/api/discomp3/<int:id_discoMp3>")
    def update_discomp3(id_discoMp3):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        d = DiscoMp3.query.get_or_404(id_discoMp3)
        data = request.get_json() or {}
        if "nombre" in data and data["nombre"]:
            d.nombre = data["nombre"]
        if "duracion" in data and data["duracion"]:
            d.duracion = data["duracion"]
        if "tamano" in data and data["tamano"]:
            d.tamano = data["tamano"]
        if "precio" in data and data["precio"]:
            d.precio=data["precio"]
        if "id_item" in data and data["id_item"]:
            d.id_item=data["id_item"]
        db.session.commit()
        return jsonify(d.to_dict())

    @app.delete("/api/discomp3/<int:id_discoMp3>")
    def delete_discomp3(id_discoMp3):
        d = DiscoMp3.query.get_or_404(id_discoMp3)
        db.session.delete(d)
        db.session.commit()
        return jsonify(ok=True)
    
        

    

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

#prueba de comentario 

# #codigo de ejemplo profesor
#     # -------- Compras (CRUD) --------
#     @app.post("/api/users/<int:user_id>/compras")
#     def create_compra(user_id):
#         if not request.is_json:
#             return jsonify(error="Se requiere JSON"), 415
#         User.query.get_or_404(user_id)
#         data = request.get_json() or {}
#         if not all(k in data for k in ("item", "cantidad", "valor")):
#             return jsonify(error="Campos 'item', 'cantidad', 'valor' son obligatorios"), 400
#         c = Compra(
#             item=data["item"],
#             cantidad=int(data["cantidad"]),
#             valor=float(data["valor"]),
#             user_id=user_id,
#         )
#         db.session.add(c)
#         db.session.commit()
#         return jsonify(c.to_dict()), 201

#     @app.get("/api/compras")
#     def list_compras():
#         items = Compra.query.order_by(Compra.id.desc()).all()
#         return jsonify([c.to_dict() for c in items])

#     @app.get("/api/users/<int:user_id>/compras")
#     def list_compras_by_user(user_id):
#         User.query.get_or_404(user_id)
#         items = Compra.query.filter_by(user_id=user_id).order_by(Compra.id.desc()).all()
#         return jsonify([c.to_dict() for c in items])

#     @app.get("/api/compras/<int:compra_id>")
#     def get_compra(compra_id):
#         c = Compra.query.get_or_404(compra_id)
#         return jsonify(c.to_dict())

#     @app.patch("/api/compras/<int:compra_id>")
#     def update_compra(compra_id):
#         if not request.is_json:
#             return jsonify(error="Se requiere JSON"), 415
#         c = Compra.query.get_or_404(compra_id)
#         data = request.get_json() or {}
#         if "item" in data and data["item"]:
#             c.item = data["item"]
#         if "cantidad" in data and data["cantidad"] is not None:
#             c.cantidad = int(data["cantidad"])
#         if "valor" in data and data["valor"] is not None:
#             c.valor = float(data["valor"])
#         db.session.commit()
#         return jsonify(c.to_dict())

#     @app.delete("/api/compras/<int:compra_id>")
#     def delete_compra(compra_id):
#         c = Compra.query.get_or_404(compra_id)
#         db.session.delete(c)
#         db.session.commit()
#         return jsonify(ok=True)

