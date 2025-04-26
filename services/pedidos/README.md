# Api Pedidos
## Descripcion
Api de pedidos, contiene los siguientes endpoints
- create_pedido: POST que crea una pedido
- pedido/<pedidoId>: GET que obtiene los datos de un pedido
- pedidos: GET que obtiene los datos de los pedidos
## Entorno local
-- Ejecutar la base de datos
```
docker run --name db-postgres-pedidos-dev \
  -e POSTGRES_USER=user_pedidos_user \
  -e POSTGRES_PASSWORD=user_pedidos_pass \
  -e POSTGRES_DB=pedidos_db \
  -p 5432:5432 \
  -d postgres:13
```
- Instalar las dependencias:
```
pipenv install
```
- Activar el entorno virtual
```
pipenv shell
```
- Ejecutar la aplicacion
```
pipenv run flask --app src.main run --host=0.0.0.0 --port=3000 --debug     
```
## Ejecucion de pruebas
- Activar el entorno local, ejecutar una BD local, y correr el siguiente comando:
```
pipenv run pytest
```
## Despliegue en nube
1. Crear proyecto en GCP (pry-pedidos)
2. Crear un repositorio en "artifact registry" (repositorio-pruebas)
3. En la consola ver los proyectos existentes:```gcloud projects list```
4. En la consola seleccionar el proyecto adecuado: ```gcloud config set project [ID_PROJECT]```

5. Otorgar los permisos necesarios para tener acceso al repositorio:
```
gcloud projects add-iam-policy-binding pry-pedidos \
--member="user:cristianarnulfoariasvargas10b@gmail.com" \
--role="roles/artifactregistry.writer"
```
- Tambien ejecutar este comando
```
gcloud auth configure-docker \
    us-central1-c-docker.pkg.dev
```
6. Compilar el contenedor:
```
docker build -t us-central1-c-docker.pkg.dev/pry-pedidos/repositorio-pruebas/pedidos:latest .
```
7. Subir el contenedor al repositorio:
```
docker push us-central1-c-docker.pkg.dev/pry-pedidos/repositorio-pruebas/pedidos:latest
```
8. Desplegar el servicio, colocar la IP correcta de la BD: 
```
gcloud run deploy api-pedidos \
    --image us-central1-c-docker.pkg.dev/pry-pedidos/repositorio-pruebas/pedidos:latest \
    --platform managed \
    --region us-central1-c \
    --allow-unauthenticated \
    --set-env-vars DATABASE_USER=user_pedidos_user,DATABASE_PASSWORD=user_pedidos_pass,DATABASE_PORT=5432,DATABASE_NAME=pedidos_db,DATABASE_URL=0.0.0.0    
```

9. Otros Comandos
-  Borra el servicio desplegado:
```
gcloud run services delete api-pedidos --region us-central1-c
```
- Borra la imagen desplegada:
```
gcloud artifacts packages delete pedidos --repository=repositorio-pruebas --location=us-central1-c
```
- Borrar los folders "pycache" recursivamente
```
find . -type d -name "__pycache__" -exec rm -rf {} +
```
- Borrar la carpeta donde esta el entorno
```
pipenv --rm
```
- Actualizar el archivo de dependencias
```
pipenv lock
```
- Verificar si las dependencias estan correctas
```
pipenv check
```
- Ver el contenido actual del entorno (similar a pip freeze)
```
pipenv graph
```

