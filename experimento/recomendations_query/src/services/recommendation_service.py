import os
import json
import time
from google.cloud import pubsub_v1
from src.models import db, Recommendation

def update_or_create_recommendation(data):
    """
    Actualiza o crea una Recommendation con los datos proporcionados.
    Requiere un Application Context activo si vas a usar db.session.
    """
    job_id = data.get('job_id')
    final_state = data.get('final_state')
    final_recommendation = data.get('final_recommendation')
    recommendation_data = data.get('recommendation_data')
    identified_objects = data.get('identified_objects')  # Nuevo campo

    if not job_id or final_state is None or final_recommendation is None:
        raise ValueError("Datos insuficientes para crear/actualizar la recomendación.")

    rec = Recommendation.query.get(job_id)
    if rec:
        rec.final_state = final_state
        rec.final_recommendation = final_recommendation
        rec.recommendation_data = recommendation_data
        rec.identified_objects = identified_objects
    else:
        rec = Recommendation(
            job_id=job_id,
            final_state=final_state,
            final_recommendation=final_recommendation,
            recommendation_data=recommendation_data,
            identified_objects=identified_objects
        )
        db.session.add(rec)
    db.session.commit()
    return rec

def create_pending_recommendation(job_id):
    """
    Crea una Recommendation en estado pending si no existe, o la devuelve si ya está creada.
    """
    rec = Recommendation.query.get(job_id)
    if not rec:
        rec = Recommendation(
            job_id=job_id,
            final_state="pending",
            final_recommendation="",
            recommendation_data={},
            identified_objects=[]  # Inicialmente vacío
        )
        db.session.add(rec)
        db.session.commit()
    return rec


def process_message(app, received_message):
    """
    1. Lee el mensaje (job_id, video_uri, metadata).
    2. Crea o actualiza la Recommendation en estado 'pending' (fase 1).
    3. Genera la recomendación final con heurísticas (fase 2).
    4. Actualiza la Recommendation con final_state='processed' y final_recommendation.
    """
    try:
        data_str = received_message.message.data.decode("utf-8")
        print(f"Mensaje recibido: {data_str}", flush=True)
        data_json = json.loads(data_str)

        job_id = data_json.get("job_id")
        if not job_id:
            print("El mensaje no contiene job_id", flush=True)
            received_message.ack()
            return

        # Fase 1: Creamos el registro 'pending' si no existe
        with app.app_context():
            create_pending_recommendation(job_id)
            print(f"Procesado job_id: {job_id} en estado 'pending'", flush=True)

        # Fase 2: Generar recomendación final
        video_metadata = data_json.get("metadata", {})  # El block devuelto por la Video Intelligence
        final_recommendation, identified_objects = generate_store_recommendation(video_metadata)

        # Fase 3: Actualizar Recommendation con final_state='processed', recommendation_data=video_metadata y final_recommendation
        updated_data = {
            "job_id": job_id,
            "final_state": "processed",
            "final_recommendation": final_recommendation,
            "recommendation_data": video_metadata,
            "identified_objects": identified_objects
        }

        with app.app_context():
            rec = update_or_create_recommendation(updated_data)
            print(f"Recomendación final guardada para job_id={job_id}", flush=True)
            print(f"Texto:\n{final_recommendation}", flush=True)

        received_message.ack()

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}", flush=True)
        # Si no ack, Pub/Sub lo reintentará.



def pull_messages(app):
    """
    Extrae mensajes en un bucle infinito y llama a process_message pasando la app.
    """
    project_id = os.environ.get("GCP_PROJECT")
    subscription_name = os.environ.get("PULL_SUBSCRIPTION")
    if not project_id or not subscription_name:
        print("No se definieron GCP_PROJECT o PULL_SUBSCRIPTION", flush=True)
        return

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    print(f"Iniciando pull en la suscripción: {subscription_path}", flush=True)

    while True:
        try:
            response = subscriber.pull(subscription=subscription_path, max_messages=10, timeout=30)
            if not response.received_messages:
                print("No hay mensajes, esperando 5 seg...", flush=True)
                time.sleep(5)
                continue
            for rmsg in response.received_messages:
                process_message(app, rmsg)
        except Exception as e:
            print(f"Error en pull: {e}", flush=True)
            time.sleep(5)





def generate_store_recommendation(analysis_metadata: dict) -> (str, list):
    """
    Genera una recomendación de distribución de artículos en la tienda basada en heurísticas 
    aplicadas a las etiquetas devueltas por la Video Intelligence API. 
    Retorna una cadena de texto con sugerencias.
    """

    # Extraer etiquetas
    labels = set()

    # segmentLabelAnnotations
    for annotation in analysis_metadata.get("segmentLabelAnnotations", []):
        entity_desc = annotation["entity"]["description"].lower()
        labels.add(entity_desc)
        # Podríamos ver categoryEntities, segments, etc. si es relevante

    # shotLabelAnnotations
    for annotation in analysis_metadata.get("shotLabelAnnotations", []):
        entity_desc = annotation["entity"]["description"].lower()
        labels.add(entity_desc)

    identified_objects = list(labels)
    # Ejemplo de heurísticas con más variedad
    # Podrías adaptarlo a los dominios que necesites (alimentos, ropa, electrónica, etc.)
    suggestions = []

    # Sugerencias centradas en 'food', 'beverage', 'cleaning', etc.
    if any(lbl in labels for lbl in ["food", "snack", "beverage"]):
        suggestions.append("Ubicar los alimentos y bebidas cerca de la entrada para compras impulsivas.")
    if any(lbl in labels for lbl in ["cleaning", "housekeeping"]):
        suggestions.append("Dedicar un pasillo exclusivo para productos de limpieza con señalización clara.")
    if any(lbl in labels for lbl in ["electronics", "software", "media", "computer", "tutorial", "editing"]):
        suggestions.append("Crear una zona de demostración de productos multimedia/electrónicos en el centro.")

       # Heurísticas para productos de canasta familiar
    if any(x in labels for x in ["groceries", "food", "cereal", "bread", "milk", "fruit", "vegetable"]):
        suggestions.append("Resalta la sección de productos de canasta familiar en un área de fácil acceso, para facilitar compras impulsivas.")

    # Heurísticas para productos de aseo y limpieza
    if any(x in labels for x in ["cleaning", "detergent", "soap", "sanitizer", "hygiene", "aseo"]):
        suggestions.append("Ubica productos de limpieza y aseo en un pasillo exclusivo y bien señalizado.")

    # Heurísticas para bebidas
    if any(x in labels for x in ["beverage", "drink", "soda", "juice", "water"]):
        suggestions.append("Promociona bebidas en zonas de alto tráfico, cerca de la entrada y las cajas.")

    # Heurísticas para snacks
    if any(x in labels for x in ["snack", "chips", "cookies", "candy"]):
        suggestions.append("Coloca snacks y pequeños alimentos en áreas estratégicas para fomentar compras impulsivas.")

    # Heurísticas para productos para bebés
    if any(x in labels for x in ["diaper", "baby", "infant", "toddler"]):
        suggestions.append("Designa una sección especial para productos para bebés, cerca de las áreas familiares.")

    # Heurísticas para cuidado personal
    if any(x in labels for x in ["personal care", "shampoo", "toothpaste", "cosmetics", "lotion"]):
        suggestions.append("Agrupa productos de cuidado personal en una zona cómoda y de fácil acceso.")

    # Heurísticas para estacionalidad
    if any(x in labels for x in ["summer", "winter", "holiday", "festival"]):
        suggestions.append("Considera promociones estacionales y destaca productos de temporada en áreas específicas.")

  # Productos de limpieza
    if any(lbl in labels for lbl in ["cleaning", "housekeeping"]):
        suggestions.append("Dedicar un pasillo exclusivo para productos de limpieza con señalización clara.")

    # Electrónica / Electrodomésticos básicos
    if any(lbl in labels for lbl in ["electronics", "computer", "tv", "radio", "appliance", "electrodoméstico"]):
        suggestions.append("Crear una zona de demostración para electrónica y electrodomésticos básicos en un área central.")

    # Cosméticos
    if any(lbl in labels for lbl in ["cosmetics", "makeup", "skincare"]):
        suggestions.append("Destinar una sección exclusiva para cosméticos, con buena iluminación y espejos.")

    # Ropa
    if any(lbl in labels for lbl in ["clothing", "apparel", "fashion", "garment", "dress"]):
        suggestions.append("Organizar la sección de ropa en áreas temáticas y con buena visibilidad.")

    # Relojería
    if any(lbl in labels for lbl in ["watch", "jewelry", "reloj", "accesorio"]):
        suggestions.append("Reservar un espacio elegante para relojería y accesorios de lujo.")

    # Multimedia y software (heurística anterior)
    if any(lbl in labels for lbl in ["software", "media", "tutorial", "editing"]):
        suggestions.append("Crear una zona interactiva para demostraciones de multimedia y software.")
    # Otras heurísticas
    if "document" in labels or "text" in labels:
        suggestions.append("Incluir un punto de exhibición de artículos de papelería cerca de la zona de cajas.")

    # Si no se detectaron etiquetas relevantes, sugerir un layout estándar
    if not suggestions:
        suggestions.append("No se identificó una categoría clara.")

    # Unir las sugerencias en un string final
    final_recommendation = "\n".join(f"- {sug}" for sug in suggestions)

    return final_recommendation, identified_objects


