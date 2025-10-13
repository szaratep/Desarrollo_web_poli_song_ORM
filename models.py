# models.py
from db import db

class Usuario(db.Model):
    __tablename__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

    telefonos = db.relationship("Telefono", backref="usuario", cascade="all, delete-orphan")
    correos = db.relationship("Correo", backref="usuario", cascade="all, delete-orphan")
    valoraciones = db.relationship("Valoracion", backref="usuario", cascade="all, delete-orphan")
    pedidos = db.relationship("Pedido", backref="usuario", cascade="all, delete-orphan")
    recopilaciones = db.relationship("Recopilacion", backref="usuario", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id_usuario": self.id_usuario, "nombre": self.nombre, "contrasena": self.contrasena}


class Telefono(db.Model):
    __tablename__ = "telefono"
    telefono = db.Column(db.String(20), primary_key=True)
    id_us = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)

    def to_dict(self):
        return {"telefono": self.telefono, "id_us": self.id_us}


class Correo(db.Model):
    __tablename__ = "correo"
    correo = db.Column(db.String(120), primary_key=True)
    id_us = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)

    def to_dict(self):
        return {"correo": self.correo, "id_us": self.id_us}


class Pedido(db.Model):
    __tablename__ = "pedido"
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_us = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_pedido = db.Column(db.Date)
    estado = db.Column(db.String(50))
    medio_pago = db.Column(db.String(50))
    id_item = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)

    valoraciones = db.relationship("Valoracion", backref="pedido", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "id_us": self.id_us,
            "fecha_pedido": self.fecha_pedido,
            "estado": self.estado,
            "medio_pago": self.medio_pago,
            "id_item": self.id_item,
        }


class Valoracion(db.Model):
    __tablename__ = "valoracion"
    id_val = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedido.id_pedido"), nullable=False)
    id_us = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    descripcion = db.Column(db.String(300))

    def to_dict(self):
        return {
            "id_val": self.id_val,
            "id_pedido": self.id_pedido,
            "id_us": self.id_us,
            "descripcion": self.descripcion,
        }


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    tipo_item = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)

    # Relaciones con tipos de ítems
    vinilos = db.relationship("Vinilo", backref="item", cascade="all, delete-orphan")
    discos_mp3 = db.relationship("DiscoMp3", backref="item", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo_item": self.tipo_item,
            "cantidad": self.cantidad,
        }


class Vinilo(db.Model):
    __tablename__ = "vinilo"
    id_vinilo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    artista = db.Column(db.String(100))
    anio_salida = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id_cancion"))
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id"))
    id_item = db.Column(db.Integer, db.ForeignKey("item.id"))

    canciones = db.relationship("ViniloCancion", backref="vinilo", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_vinilo": self.id_vinilo,
            "nombre": self.nombre,
            "artista": self.artista,
            "anio_salida": self.anio_salida,
            "precio_unitario": self.precio_unitario,
            "id_cancion": self.id_cancion,
            "id_proveedor": self.id_proveedor,
        }


class DiscoMp3(db.Model):
    __tablename__ = "discoMp3"
    id_discoMp3 = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    duracion = db.Column(db.Time)
    tamano = db.Column(db.Numeric)
    precio = db.Column(db.Float)
    id_item = db.Column(db.Integer, db.ForeignKey("item.id"))  # ← 🔧 agregado

    canciones = db.relationship("DiscoMp3Cancion", backref="discoMp3", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_discoMp3": self.id_discoMp3,
            "nombre": self.nombre,
            "duracion": str(self.duracion),
            "tamano": float(self.tamano),
            "precio": self.precio,
            "id_item": self.id_item,
        }


class Cancion(db.Model):
    __tablename__ = "cancion"
    id_cancion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    duracion = db.Column(db.Time)
    tamano = db.Column(db.Numeric)

    vinilos = db.relationship("ViniloCancion", backref="cancion", cascade="all, delete-orphan")
    discos = db.relationship("DiscoMp3Cancion", backref="cancion", cascade="all, delete-orphan")
    recopilaciones = db.relationship("RecopilacionCancion", backref="cancion", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_cancion": self.id_cancion,
            "nombre": self.nombre,
            "duracion": str(self.duracion),
            "tamano": float(self.tamano),
        }


class ViniloCancion(db.Model):
    __tablename__ = "viniloCancion"
    id_vinilo = db.Column(db.Integer, db.ForeignKey("vinilo.id_vinilo"), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id_cancion"), primary_key=True)


class DiscoMp3Cancion(db.Model):
    __tablename__ = "discoMp3Cancion"
    id_discoMp3 = db.Column(db.Integer, db.ForeignKey("discoMp3.id_discoMp3"), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id_cancion"), primary_key=True)


class Proveedor(db.Model):
    __tablename__ = "proveedor"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    correos = db.relationship("CorreoProveedor", backref="proveedor", cascade="all, delete-orphan")
    telefonos = db.relationship("TelefonoProveedor", backref="proveedor", cascade="all, delete-orphan")
    vinilos = db.relationship("Vinilo", backref="proveedor", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}


class CorreoProveedor(db.Model):
    __tablename__ = "correo_proveedor"
    correo = db.Column(db.String(120), primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id"))

    def to_dict(self):
        return {"correo": self.correo, "id_proveedor": self.id_proveedor}


class TelefonoProveedor(db.Model):
    __tablename__ = "telefono_proveedor"
    telefono = db.Column(db.String(20), primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id"))

    def to_dict(self):
        return {"telefono": self.telefono, "id_proveedor": self.id_proveedor}


class Recopilacion(db.Model):
    __tablename__ = "recopilacion"
    id_recopilacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    id_us = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"))
    publica = db.Column(db.Boolean)

    canciones = db.relationship("RecopilacionCancion", backref="recopilacion", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id_recopilacion": self.id_recopilacion,
            "nombre": self.nombre,
            "id_us": self.id_us,
            "publica": self.publica,
        }


class RecopilacionCancion(db.Model):
    __tablename__ = "recopilacionCancion"
    id_recopilacion = db.Column(db.Integer, db.ForeignKey("recopilacion.id_recopilacion"), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id_cancion"), primary_key=True)
