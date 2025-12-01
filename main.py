import os
import pymongo
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Si usas MongoDB Atlas, reemplaza esta cadena con la que te da la web.
# Ejemplo Atlas: "mongodb+srv://usuario:password@cluster.mongodb.net/..."
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "biblioteca_personal"
COLLECTION_NAME = "libros"


class GestorBibliotecaMongo:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

            # Verificamos la conexión pidiendo información del servidor
            self.client.server_info()

            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            print("✅ Conexión a MongoDB exitosa.")

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Error crítico: No se pudo conectar a MongoDB.")
            print(f"Detalle: {e}")
            print("Asegúrate de que el servicio de MongoDB esté corriendo.")
            exit()

    def agregar_libro(self, titulo, autor, genero, estado):
        documento = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }
        result = self.collection.insert_one(documento)
        return result.inserted_id is not None

    def listar_libros(self):
        return list(self.collection.find())

    def buscar_libros(self, termino):
        regex = {"$regex": termino, "$options": "i"}

        filtro = {
            "$or": [
                {"titulo": regex},
                {"autor": regex},
                {"genero": regex}
            ]
        }
        return list(self.collection.find(filtro))

    def actualizar_libro(self, id_str, nuevos_datos):
        try:
            obj_id = ObjectId(id_str)

            datos_a_actualizar = {k: v for k, v in nuevos_datos.items() if v}

            if not datos_a_actualizar:
                return False

            resultado = self.collection.update_one(
                {"_id": obj_id},
                {"$set": datos_a_actualizar}
            )
            return resultado.modified_count > 0

        except Exception as e:
            print(f"Error en ID o actualización: {e}")
            return False

    def eliminar_libro(self, id_str):
        try:
            obj_id = ObjectId(id_str)
            resultado = self.collection.delete_one({"_id": obj_id})
            return resultado.deleted_count > 0
        except Exception:
            print("ID inválido.")
            return False

def mostrar_tabla(libros):
    if not libros:
        print("\n(No se encontraron libros)")
        return

    print("\n" + "=" * 100)
    # Ajustamos el ancho porque el ID de Mongo es largo (24 caracteres)
    print(f"{'ID (ObjectId)':<26} | {'TÍTULO':<25} | {'AUTOR':<20} | {'GÉNERO':<12} | {'ESTADO':<10}")
    print("-" * 100)

    for doc in libros:
        # Convertimos ObjectId a string para mostrarlo
        doc_id = str(doc.get('_id', 'N/A'))
        print(
            f"{doc_id:<26} | {doc.get('titulo', ''):<25} | {doc.get('autor', ''):<20} | {doc.get('genero', ''):<12} | {doc.get('estado', ''):<10}")
    print("=" * 100 + "\n")


def menu_principal():
    gestor = GestorBibliotecaMongo()

    while True:
        print("\n--- 🍃 GESTOR DE BIBLIOTECA (MongoDB) ---")
        print("1. Agregar nuevo libro")
        print("2. Ver todos los libros")
        print("3. Buscar libro")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            print("\n--- Agregar Libro ---")
            t = input("Título: ")
            a = input("Autor: ")
            g = input("Género: ")
            e = "Leído" if input("¿Leído? (s/n): ").lower() == 's' else "No leído"

            if gestor.agregar_libro(t, a, g, e):
                print("✅ Documento insertado correctamente.")

        elif opcion == '2':
            libros = gestor.listar_libros()
            mostrar_tabla(libros)

        elif opcion == '3':
            termino = input("\nIngrese término de búsqueda: ")
            libros = gestor.buscar_libros(termino)
            mostrar_tabla(libros)

        elif opcion == '4':
            print("\n--- Actualizar Libro ---")
            mostrar_tabla(gestor.listar_libros())
            id_str = input("Copie y pegue el ID exacto del libro: ").strip()

            print("(Deje vacío para mantener el valor actual)")
            cambios = {
                "titulo": input("Nuevo título: "),
                "autor": input("Nuevo autor: "),
                "genero": input("Nuevo género: "),
            }
            estado_opt = input("Nuevo estado (s/n, vacío saltar): ").lower()
            if estado_opt == 's':
                cambios["estado"] = "Leído"
            elif estado_opt == 'n':
                cambios["estado"] = "No leído"

            if gestor.actualizar_libro(id_str, cambios):
                print("✅ Libro actualizado.")
            else:
                print("⚠️ No se realizaron cambios (ID incorrecto o sin datos nuevos).")

        elif opcion == '5':
            print("\n--- Eliminar Libro ---")
            mostrar_tabla(gestor.listar_libros())
            id_str = input("Copie y pegue el ID a eliminar: ").strip()
            if input("¿Confirmar eliminación? (s/n): ").lower() == 's':
                if gestor.eliminar_libro(id_str):
                    print("✅ Documento eliminado.")
                else:
                    print("❌ No se encontró el documento.")

        elif opcion == '6':
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    menu_principal()