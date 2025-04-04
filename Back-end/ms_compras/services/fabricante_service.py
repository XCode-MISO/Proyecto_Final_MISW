from models.db import db
from models.fabricante import Fabricante

class FabricanteService:
    def crear_fabricante(self, nombre, correo, telefono, empresa):
        nuevo = Fabricante(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            empresa=empresa
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo