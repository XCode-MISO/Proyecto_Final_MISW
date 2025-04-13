# Api Ventas
## Descripcion
Api de Ventas, contiene los siguientes endpoints
- visit: POST que crea una visita
- client: POST que crea un cliente
## Entorno local
-- Ejecutar la base de datos
```
docker run --name db-postgres-ventas-dev \
  -e POSTGRES_USER=user_ventas_user \
  -e POSTGRES_PASSWORD=user_ventas_pass \
  -e POSTGRES_DB=ventas_db \
  -p 5432:5432 \
  -d postgres:13
```
- Activar el entorno virtual
```
python3 -m venv venv
source venv/bin/activate
```
- Instalar las dependencias:
```
pip install -r requirements.txt
```
- Ejecutar la aplicacion
```
export FLASK_APP="./src/main.py"
flask run -h 0.0.0.0 --port=3000
```
## Ejecucion de pruebas
- Activar el entorno local, ejecutar una BD local, y correr el siguiente comando:
```
pytest --cov-fail-under=70 --cov=src
pytest src/tests/commands/test.py --cov-fail-under=70 --cov=src
```
## Despliegue en nube
1. Crear proyecto en GCP (pry-ventas)
2. Crear un repositorio en "artifact registry" (repositorio-pruebas)
3. En la consola ver los proyectos existentes:```gcloud projects list```
4. En la consola seleccionar el proyecto adecuado: ```gcloud config set project [ID_PROJECT]```

5. Otorgar los permisos necesarios para tener acceso al repositorio:
```
gcloud projects add-iam-policy-binding pry-ventas \
--member="user:emersonchaparroampa@gmail.com" \
--role="roles/artifactregistry.writer"
```
- Tambien ejecutar este comando
```
gcloud auth configure-docker \
    us-central1-docker.pkg.dev
```
6. Compilar el contenedor:
```
docker build -t us-central1-docker.pkg.dev/pry-ventas/repositorio-pruebas/ventas:latest .
```
7. Subir el contenedor al repositorio:
```
docker push us-central1-docker.pkg.dev/pry-ventas/repositorio-pruebas/ventas:latest
```
8. Desplegar el servicio, colocar la IP correcta de la BD: 
```
gcloud run deploy api-ventas \
    --image us-central1-docker.pkg.dev/pry-ventas/repositorio-pruebas/ventas:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DB_USER=user_ventas_user,DB_PASSWORD=user_ventas_pass,DB_PORT=5432,DB_NAME=ventas_db,DB_HOST=0.0.0.0    
```

9. Otros Comandos
-  Borra el servicio desplegado:
```
gcloud run services delete api-ventas --region us-central1
```
- Borra la imagen desplegada:
```
gcloud artifacts packages delete ventas --repository=repositorio-pruebas --location=us-central1
```
- Borrar los folders "pycache" recursivamente
```
find . -type d -name "__pycache__" -exec rm -rf {} +
```
- Borrar la carpeta donde esta el entorno
```
rm -r ./venv
```
- Actualizar el archivo de dependencias
```
pip freeze > requirements.txt
```
- Verificar si las dependencias estan correctas
```
pip check
```



