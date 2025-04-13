from models.db import db
from models.fabricante import Fabricante
import csv
import io
import re

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
    
    
    @staticmethod
    def upload_fabricantes_from_file(file_content: str):
        """
        Procesa el contenido CSV y realiza la inserción masiva de fabricantes.
        Se requiere que el CSV tenga la siguiente cabecera:
            nombre,empresa,telefono,correo_electronico
        Se acepta también que en lugar de "correo_electronico" se use "correo".
        
        Realiza validaciones:
         - Se verifica que la cabecera contenga los campos requeridos.
         - Se valida que cada fila tenga valores para todos los campos.
         - Se insertan las filas válidas y se omiten las que tengan errores, retornando
           un listado de errores con el número de fila y detalle del error.
           
        Retorna un diccionario con el número de registros insertados y los errores encontrados.
        """
        # Definimos los campos requeridos y sus posibles alias
        required_fields = {
            "nombre": ["nombre"],
            "empresa": ["empresa"],
            "telefono": ["telefono"],
            "correo_electronico": ["correo_electronico", "correo"]
        }

        inserted = 0
        errors = []

        # Crear el lector CSV a partir del contenido (cadena)
        csv_reader = csv.reader(io.StringIO(file_content))
        try:
            header = next(csv_reader)
        except StopIteration:
            return {"inserted": inserted, "errors": ["El archivo está vacío."]}

        # Normalización de la cabecera
        normalized_header = [h.strip().lower().replace(" ", "_") for h in header]

        # Si la cabecera tiene "correo" pero no "correo_electronico", lo reemplazamos
        if "correo" in normalized_header and "correo_electronico" not in normalized_header:
            normalized_header = ["correo_electronico" if h == "correo" else h for h in normalized_header]

        # Verificar que cada campo requerido tenga al menos uno de sus alias en la cabecera
        missing_fields = []
        for field, aliases in required_fields.items():
            if not any(alias in normalized_header for alias in aliases):
                missing_fields.append(field)
        if missing_fields:
            return {
                "inserted": inserted,
                "errors": [f"Falta(s) campo(s) en la cabecera: {', '.join(missing_fields)}"]
            }

        # Crear un diccionario que mapea cada campo requerido al índice correspondiente
        field_indices = {}
        for field, aliases in required_fields.items():
            for alias in aliases:
                if alias in normalized_header:
                    field_indices[field] = normalized_header.index(alias)
                    break

        # Procesar cada fila (a partir de la cabecera)
        line_num = 1  # La cabecera es la línea 1
        for row in csv_reader:
            line_num += 1
            # Verificar que la fila tenga al menos tantas columnas como la cabecera
            if len(row) < len(normalized_header):
                errors.append(f"Fila {line_num}: Número insuficiente de campos.")
                continue

            row_data = {}
            row_has_error = False
            for field in required_fields.keys():
                # Extraemos el valor correspondiente y quitamos espacios
                value = row[field_indices[field]].strip() if field_indices[field] < len(row) else ""
                if not value:
                    errors.append(f"Fila {line_num}: El campo '{field}' es obligatorio.")
                    row_has_error = True
                row_data[field] = value

            # Si hay error en la fila, no se inserta
            if row_has_error:
                continue

            # Intentamos insertar el registro en la base de datos
            try:
                from models.fabricante import Fabricante
                fabricante = Fabricante(
                    nombre=row_data["nombre"],
                    correo=row_data["correo_electronico"],
                    telefono=row_data["telefono"],
                    empresa=row_data["empresa"]
                )
                db.session.add(fabricante)
                db.session.commit()
                inserted += 1
            except Exception as e:
                db.session.rollback()
                errors.append(f"Fila {line_num}: Error al insertar: {str(e)}")
        return {"inserted": inserted, "errors": errors}