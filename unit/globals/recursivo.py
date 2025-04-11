import os

class Utils:

    def crear_archivo(self, archivo, contenido):
        try:
            magiccorp_path = os.path.join("C:\\", "MagicCorp")
            file_path = os.path.join(magiccorp_path, archivo)

            # Asegurarse de que la carpeta MagicCorp existe
            if not os.path.exists(magiccorp_path):
                os.makedirs(magiccorp_path)  # Crea la carpeta si no existe
                print(f"Carpeta creada: {magiccorp_path}")

            # Escribir el contenido en el archivo especificado
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(contenido)
            print(f"Archivo {archivo} creado correctamente en {file_path}")

        except Exception as ex:
            raise Exception(f"Error al crear el archivo {archivo}: {str(ex)}")

    def buscar_parametro(self, archivo, parametro):
        """
        Busca un parámetro específico en un archivo .txt.
        
        :param archivo: Nombre del archivo a buscar.
        :param parametro: El parámetro que se desea buscar (por ejemplo, "Tipo de instalación").
        :return: El valor del parámetro si se encuentra, o None si no.
        """
        try:
            magiccorp_path = os.path.join("C:\\", "MagicCorp")
            file_path = os.path.join(magiccorp_path, archivo)

            # Asegurarse de que el archivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"El archivo {archivo} no existe en la ruta {file_path}.")

            # Leer el archivo línea por línea
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Verificar si la línea contiene el parámetro buscado
                    if parametro in line:
                        # Retornar el valor después del ":"
                        return line.split(":")[1].strip()

            # Si no se encontró el parámetro, devolver None
            print(f"Parámetro '{parametro}' no encontrado en {archivo}.")
            return None

        except Exception as ex:
            raise Exception(f"Error al buscar el parámetro '{parametro}' en {archivo}: {str(ex)}")
    
    def leer_nombre_negocio_desde_key():
        """Lee el nombre del negocio desde el archivo key.txt."""
        key_file_path = r"C:\MagicCorp\key.txt"
        try:
            if not os.path.exists(key_file_path):
                raise FileNotFoundError(f"El archivo key.txt no existe en {key_file_path}.")
            with open(key_file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if "Negocio:" in line:
                        return line.split(":")[1].strip()
            raise ValueError("No se encontró el parámetro 'Negocio' en el archivo key.txt.")
        except Exception as e:
            print(f"Error al leer el nombre del negocio desde key.txt: {str(e)}")
            return None

