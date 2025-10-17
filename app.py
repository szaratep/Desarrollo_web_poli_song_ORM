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


    # =====================================================
    #                  DiscoMp3 CRUD
    # =====================================================
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
    
       
# =====================================================
#                 VINILO CRUD
# =====================================================
    

    @app.post("/api/vinilo")
    def create_vinilo():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        vinilos = []
        for i, item in enumerate(data, start=1):
            nombre = item.get("nombre")
            artista = item.get("artista")
            anio_salida = item.get("anio_salida")
            precio_unitario = item.get("precio_unitario")
            id_cancion = item.get("id_cancion")
            id_proveedor = item.get("id_proveedor")
            id_item = item.get("id_item")

            # Validar campos obligatorios
            if not all([nombre, artista, anio_salida, precio_unitario, id_cancion, id_proveedor, id_item]):
                return jsonify(
                    error=f"El registro #{i} no tiene todos los campos requeridos ('nombre', 'artista', 'anio_salida', 'precio_unitario', 'id_cancion', 'id_proveedor', 'id_item')"
                ), 400

            vinilos.append(
                Vinilo(
                    nombre=nombre,
                    artista=artista,
                    anio_salida=anio_salida,
                    precio_unitario=precio_unitario,
                    id_cancion=id_cancion,
                    id_proveedor=id_proveedor,
                    id_item=id_item
                )
            )

        try:
            db.session.add_all(vinilos)
            db.session.commit()
            return jsonify([v.to_dict() for v in vinilos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar el vinilo: {str(e)}"), 500


    @app.get("/api/vinilo")
    def list_vinilos():
        vals = Vinilo.query.all()
        return jsonify([v.to_dict() for v in vals])


    @app.get("/api/vinilo/<int:id_vinilo>")
    def get_vinilo(id_vinilo):
        v = Vinilo.query.get_or_404(id_vinilo)
        return jsonify(v.to_dict())


    @app.patch("/api/vinilo/<int:id_vinilo>")
    def update_vinilo(id_vinilo):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        v = Vinilo.query.get_or_404(id_vinilo)
        data = request.get_json() or {}

        if "nombre" in data and data["nombre"]:
            v.nombre = data["nombre"]
        if "artista" in data and data["artista"]:
            v.artista = data["artista"]
        if "anio_salida" in data and data["anio_salida"]:
            v.anio_salida = data["anio_salida"]
        if "precio_unitario" in data and data["precio_unitario"]:
            v.precio_unitario = data["precio_unitario"]
        if "id_cancion" in data and data["id_cancion"]:
            v.id_cancion = data["id_cancion"]
        if "id_proveedor" in data and data["id_proveedor"]:
            v.id_proveedor = data["id_proveedor"]
        if "id_item" in data and data["id_item"]:
            v.id_item = data["id_item"]

        db.session.commit()
        return jsonify(v.to_dict())


    @app.delete("/api/vinilo/<int:id_vinilo>")
    def delete_vinilo(id_vinilo):
        v = Vinilo.query.get_or_404(id_vinilo)
        db.session.delete(v)
        db.session.commit()
        return jsonify(ok=True)

    # --------------------------
    # CRUD PEDIDO
    # --------------------------
    @app.post("/api/pedido")
    def create_pedido():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        pedidos = []
        for i, item in enumerate(data, start=1):
            id_us = item.get("id_us")
            fecha_pedido = item.get("fecha_pedido")
            estado = item.get("estado")
            medio_pago = item.get("medio_pago")
            id_item = item.get("id_item")

            # Validar campos obligatorios
            if not all([id_us, fecha_pedido, estado, medio_pago, id_item]):
                return jsonify(
                    error=f"El registro #{i} no tiene todos los campos requeridos ('id_us', 'fecha_pedido', 'estado', 'medio_pago', 'id_item')"
                ), 400

            pedidos.append(
                Pedido(
                    id_us=id_us,
                    fecha_pedido=fecha_pedido,
                    estado=estado,
                    medio_pago=medio_pago,
                    id_item=id_item
                )
            )

        try:
            db.session.add_all(pedidos)
            db.session.commit()
            return jsonify([p.to_dict() for p in pedidos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar el pedido: {str(e)}"), 500


    @app.get("/api/pedido")
    def list_pedidos():
        vals = Pedido.query.all()
        return jsonify([p.to_dict() for p in vals])


    @app.get("/api/pedido/<int:id_pedido>")
    def get_pedido(id_pedido):
        p = Pedido.query.get_or_404(id_pedido)
        return jsonify(p.to_dict())


    @app.patch("/api/pedido/<int:id_pedido>")
    def update_pedido(id_pedido):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        p = Pedido.query.get_or_404(id_pedido)
        data = request.get_json() or {}

        if "id_us" in data and data["id_us"]:
            p.id_us = data["id_us"]
        if "fecha_pedido" in data and data["fecha_pedido"]:
            p.fecha_pedido = data["fecha_pedido"]
        if "estado" in data and data["estado"]:
            p.estado = data["estado"]
        if "medio_pago" in data and data["medio_pago"]:
            p.medio_pago = data["medio_pago"]
        if "id_item" in data and data["id_item"]:
            p.id_item = data["id_item"]

        db.session.commit()
        return jsonify(p.to_dict())


    @app.delete("/api/pedido/<int:id_pedido>")
    def delete_pedido(id_pedido):
        p = Pedido.query.get_or_404(id_pedido)
        db.session.delete(p)
        db.session.commit()
        return jsonify(ok=True)
    
    # =====================================================
    #              DISCO MP3 - CANCIÓN CRUD
    # =====================================================
    @app.post("/api/discomp3cancion")
    def create_discomp3cancion():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        relaciones = []
        for i, item in enumerate(data, start=1):
            id_discoMp3 = item.get("id_discoMp3")
            id_cancion = item.get("id_cancion")

            if not id_discoMp3 or not id_cancion:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('id_discoMp3', 'id_cancion')"), 400

            relaciones.append(DiscoMp3Cancion(id_discoMp3=id_discoMp3, id_cancion=id_cancion))

        try:
            db.session.add_all(relaciones)
            db.session.commit()
            return jsonify([{"id_discoMp3": r.id_discoMp3, "id_cancion": r.id_cancion} for r in relaciones]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar DiscoMp3-Canción: {str(e)}"), 500

    @app.get("/api/discomp3cancion")
    def list_discomp3cancion():
        relaciones = DiscoMp3Cancion.query.all()
        return jsonify([{"id_discoMp3": r.id_discoMp3, "id_cancion": r.id_cancion} for r in relaciones])

    @app.delete("/api/discomp3cancion/<int:id_discoMp3>/<int:id_cancion>")
    def delete_discomp3cancion(id_discoMp3, id_cancion):
        r = DiscoMp3Cancion.query.get_or_404((id_discoMp3, id_cancion))
        db.session.delete(r)
        db.session.commit()
        return jsonify(ok=True)


    # =====================================================
    #                     ITEMS CRUD
    # =====================================================
    @app.post("/api/items")
    def create_items():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        items = []
        for i, item in enumerate(data, start=1):
            tipo_item = item.get("tipo_item")
            cantidad = item.get("cantidad")

            if not tipo_item or cantidad is None:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('tipo_item', 'cantidad')"), 400

            items.append(Item(tipo_item=tipo_item, cantidad=cantidad))

        try:
            db.session.add_all(items)
            db.session.commit()
            return jsonify([i.to_dict() for i in items]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar items: {str(e)}"), 500

    @app.get("/api/items")
    def list_items():
        items = Item.query.all()
        return jsonify([i.to_dict() for i in items])

    @app.get("/api/items/<int:id>")
    def get_item(id):
        i = Item.query.get_or_404(id)
        return jsonify(i.to_dict())

    @app.patch("/api/items/<int:id>")
    def update_item(id):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        i = Item.query.get_or_404(id)
        data = request.get_json() or {}

        if "tipo_item" in data and data["tipo_item"]:
            i.tipo_item = data["tipo_item"]
        if "cantidad" in data and data["cantidad"] is not None:
            i.cantidad = data["cantidad"]

        db.session.commit()
        return jsonify(i.to_dict())

    @app.delete("/api/items/<int:id>")
    def delete_item(id):
        i = Item.query.get_or_404(id)
        db.session.delete(i)
        db.session.commit()
        return jsonify(ok=True)


    # =====================================================
    #              RECOPILACIÓN - CANCIÓN CRUD
    # =====================================================
    @app.post("/api/recopilacioncancion")
    def create_recopilacioncancion():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        relaciones = []
        for i, item in enumerate(data, start=1):
            id_recopilacion = item.get("id_recopilacion")
            id_cancion = item.get("id_cancion")

            if not id_recopilacion or not id_cancion:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('id_recopilacion', 'id_cancion')"), 400

            relaciones.append(RecopilacionCancion(id_recopilacion=id_recopilacion, id_cancion=id_cancion))

        try:
            db.session.add_all(relaciones)
            db.session.commit()
            return jsonify([{"id_recopilacion": r.id_recopilacion, "id_cancion": r.id_cancion} for r in relaciones]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar Recopilación-Canción: {str(e)}"), 500

    @app.get("/api/recopilacioncancion")
    def list_recopilacioncancion():
        relaciones = RecopilacionCancion.query.all()
        return jsonify([{"id_recopilacion": r.id_recopilacion, "id_cancion": r.id_cancion} for r in relaciones])

    @app.delete("/api/recopilacioncancion/<int:id_recopilacion>/<int:id_cancion>")
    def delete_recopilacioncancion(id_recopilacion, id_cancion):
        r = RecopilacionCancion.query.get_or_404((id_recopilacion, id_cancion))
        db.session.delete(r)
        db.session.commit()
        return jsonify(ok=True)


    # =====================================================
    #                 VINILO - CANCIÓN CRUD
    # =====================================================
    @app.post("/api/vinilocancion")
    def create_vinilocancion():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        relaciones = []
        for i, item in enumerate(data, start=1):
            id_vinilo = item.get("id_vinilo")
            id_cancion = item.get("id_cancion")

            if not id_vinilo or not id_cancion:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('id_vinilo', 'id_cancion')"), 400

            relaciones.append(ViniloCancion(id_vinilo=id_vinilo, id_cancion=id_cancion))

        try:
            db.session.add_all(relaciones)
            db.session.commit()
            return jsonify([{"id_vinilo": r.id_vinilo, "id_cancion": r.id_cancion} for r in relaciones]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar Vinilo-Canción: {str(e)}"), 500

    @app.get("/api/vinilocancion")
    def list_vinilocancion():
        relaciones = ViniloCancion.query.all()
        return jsonify([{"id_vinilo": r.id_vinilo, "id_cancion": r.id_cancion} for r in relaciones])

    @app.delete("/api/vinilocancion/<int:id_vinilo>/<int:id_cancion>")
    def delete_vinilocancion(id_vinilo, id_cancion):
        r = ViniloCancion.query.get_or_404((id_vinilo, id_cancion))
        db.session.delete(r)
        db.session.commit()
        return jsonify(ok=True)
    # =====================================================
    #                  PROVEEDOR CRUD
    # =====================================================
    @app.post("/api/proveedores")
    def create_proveedores():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro JSON"), 400

        proveedores = []
        for i, item in enumerate(data, start=1):
            nombre = item.get("nombre")
        if not nombre:
            return jsonify(error=f"El registro #{i} no tiene el campo requerido ('nombre')"), 400
        proveedores.append(Proveedor(nombre=nombre))

        try:
            db.session.add_all(proveedores)
            db.session.commit()
            return jsonify([p.to_dict() for p in proveedores]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar proveedores: {str(e)}"), 500


    @app.get("/api/proveedores")
    def list_proveedores():
        proveedores = Proveedor.query.all()
        return jsonify([p.to_dict() for p in proveedores])


    @app.get("/api/proveedores/<int:id>")
    def get_proveedor(id):
        p = Proveedor.query.get_or_404(id)
        return jsonify(p.to_dict())


    @app.patch("/api/proveedores/<int:id>")
    def update_proveedor(id):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        p = Proveedor.query.get_or_404(id)
        data = request.get_json() or {}
        if "nombre" in data and data["nombre"]:
            p.nombre = data["nombre"]
        db.session.commit()
        return jsonify(p.to_dict())


    @app.delete("/api/proveedores/<int:id>")
    def delete_proveedor(id):
        p = Proveedor.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify(ok=True)
    # =====================================================
    #              CORREO - PROVEEDOR CRUD
    # =====================================================
    @app.post("/api/correos_proveedor")
    def create_correos_proveedor():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        correos = []
        for i, item in enumerate(data, start=1):
            correo = item.get("correo")
            id_proveedor = item.get("id_proveedor")
            if not correo or not id_proveedor:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('correo', 'id_proveedor')"), 400
            correos.append(CorreoProveedor(correo=correo, id_proveedor=id_proveedor))

        try:
            db.session.add_all(correos)
            db.session.commit()
            return jsonify([c.to_dict() for c in correos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar correos_proveedor: {str(e)}"), 500


    @app.get("/api/correos_proveedor")
    def list_correos_proveedor():
        correos = CorreoProveedor.query.all()
        return jsonify([c.to_dict() for c in correos])


    @app.get("/api/correos_proveedor/<string:correo>")
    def get_correo_proveedor(correo):
        c = CorreoProveedor.query.get_or_404(correo)
        return jsonify(c.to_dict())


    @app.patch("/api/correos_proveedor/<string:correo>")
    def update_correo_proveedor(correo):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        c = CorreoProveedor.query.get_or_404(correo)
        data = request.get_json() or {}
        if "id_proveedor" in data and data["id_proveedor"]:
            c.id_proveedor = data["id_proveedor"]
        db.session.commit()
        return jsonify(c.to_dict())


    @app.delete("/api/correos_proveedor/<string:correo>")
    def delete_correo_proveedor(correo):
        c = CorreoProveedor.query.get_or_404(correo)
        db.session.delete(c)
        db.session.commit()
        return jsonify(ok=True)
    # =====================================================
    #             TELEFONO - PROVEEDOR CRUD
    # =====================================================
    @app.post("/api/telefonos_proveedor")
    def create_telefonos_proveedor():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415

        data = request.get_json()
        if isinstance(data, dict):
            data = [data]

        telefonos = []
        for i, item in enumerate(data, start=1):
            telefono = item.get("telefono")
            id_proveedor = item.get("id_proveedor")
            if not telefono or not id_proveedor:
                return jsonify(error=f"El registro #{i} no tiene los campos requeridos ('telefono', 'id_proveedor')"), 400
            telefonos.append(TelefonoProveedor(telefono=telefono, id_proveedor=id_proveedor))

        try:
            db.session.add_all(telefonos)
            db.session.commit()
            return jsonify([t.to_dict() for t in telefonos]), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Error al insertar telefonos_proveedor: {str(e)}"), 500


    @app.get("/api/telefonos_proveedor")
    def list_telefonos_proveedor():
        telefonos = TelefonoProveedor.query.all()
        return jsonify([t.to_dict() for t in telefonos])


    @app.get("/api/telefonos_proveedor/<string:telefono>")
    def get_telefono_proveedor(telefono):
        t = TelefonoProveedor.query.get_or_404(telefono)
        return jsonify(t.to_dict())


    @app.patch("/api/telefonos_proveedor/<string:telefono>")
    def update_telefono_proveedor(telefono):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        t = TelefonoProveedor.query.get_or_404(telefono)
        data = request.get_json() or {}
        if "id_proveedor" in data and data["id_proveedor"]:
            t.id_proveedor = data["id_proveedor"]
        db.session.commit()
        return jsonify(t.to_dict())


    @app.delete("/api/telefonos_proveedor/<string:telefono>")
    def delete_telefono_proveedor(telefono):
        t = TelefonoProveedor.query.get_or_404(telefono)
        db.session.delete(t)
        db.session.commit()
        return jsonify(ok=True)
    
    return app
      
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

