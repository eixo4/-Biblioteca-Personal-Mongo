# Biblioteca Personal con MongoDB 🍃

Gestor de biblioteca migrado a una base de datos **NoSQL** orientada a documentos.

## ⚙️ Requisitos Previos

1.  **Python 3.x**
2.  **MongoDB Community Server** instalado localmente O una cuenta en **MongoDB Atlas**.

## 🛠️ Instalación de MongoDB (Local)

### Windows
1. Descarga el instalador "MSI" desde [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community).
2. Ejecuta el instalador. Te recomiendo instalar **MongoDB Compass** (interfaz gráfica) cuando te dé la opción.
3. El servidor se iniciará automáticamente en `localhost:27017`.

### Docker (Opción Rápida)
Si tienes Docker, solo ejecuta:
```bash
docker run -d -p 27017:27017 --name mi-mongo mongo:latest
```

## 🚀 Configuración y Ejecución

1.  **Instalar dependencias Python:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar conexión (Opcional):**
    Por defecto, el programa busca una base de datos local. Si usas **MongoDB Atlas**, edita la variable `MONGO_URI` en `main.py`:

    ```python
    MONGO_URI = "mongodb+srv://tu_usuario:tu_pass@cluster.mongodb.net/..."
    ```

3.  **Ejecutar:**

    ```bash
    python main.py
    ```

## 📄 Estructura del Documento JSON

Los libros se almacenan en la colección `libros` con este formato:

```json
{
  "_id": ObjectId("6566f1..."),  // Generado automáticamente por Mongo
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "genero": "Realismo Mágico",
  "estado": "Leído"
}
```

### 📁 Estructura del Proyecto

```
biblioteca_mongo/
│
├── main.py           # Código principal
├── requirements.txt  # Dependencias
└── README.md         # Instrucciones de instalación MongoDB
```
