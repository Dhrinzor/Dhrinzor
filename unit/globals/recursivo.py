import os

class Utils:

    def crear_archivo(self, archivo, contenido):
        try:
            magiccorp_path = os.path.join("C:\\", "MagicCorp")
            key_file_path = os.path.join(magiccorp_path, archivo)

            # Asegurarse de que la carpeta MagicCorp existe
            if not os.path.exists(magiccorp_path):
                os.makedirs(magiccorp_path)  # Crea la carpeta si no existe
                print(f"Carpeta creada: {magiccorp_path}")

            # Escribir el contenido en license.txt
            with open(key_file_path, "w", encoding="utf-8") as file:
                file.write(contenido)
            print(f"Archivo key.txt creado correctamente en {key_file_path}")

        except Exception as ex:
            raise Exception(f"Error al crear el archivo license.txt: {str(ex)}")