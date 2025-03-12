import os
import logging
from datetime import datetime

class FileProcessor:

    def __init__(self, base_path: str, log_file: str):
        # Directorio raiz para los archivos
        self.base_path = base_path
        # Se indica el archivo de log
        self.logger = self.set_logger(log_file)

    """ Configuración del logger """
    def set_logger(self, log_file: str):
        # Configuración del logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Escribimos los logs
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formato del log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger
    
    """Lista los archivos y carpetas dentro de la ruta dada."""
    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        # Ruta de la carpeta
        folder_path = os.path.join(self.base_path, folder_name)
        # Verificar si la carpeta existe
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            # Escribimos un log indicando que la carpeta no existe
            self.logger.error(f"The folder '{folder_path}' does not exist.")
            # Imprimimos un mensaje de error
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        # Se lista los archivos y carpetas que se encuentran dentro de la ruta
        items = os.listdir(folder_path)
        # Se imprime la cantidad de elementos de la carpeta
        print(f"\n The folder'{folder_name}' contains: {len(items)} elements:")

        # Se recorre la lista de elementos
        for item in items:
            # Se obtiene la ruta completa del elemento
            item_path = os.path.join(folder_path, item)
            # Se crea una variable que verifica si el elemento es un archivo o una carpeta
            item_type = "Folder" if os.path.isdir(item_path) else "File"

            # Se valida si el usuario solicita informacion extra
            if details:
                # Se obtiene el tamaño del archivo y se canvierte a MB
                size = os.path.getsize(item_path) / (1024 * 1024)
                # Se obtiene la fecha y hora de la ultima modificacion
                time = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
                # Se imprime el tipo de archivo, el nombre del archivo, el tamaño y la ultima modificacion
                print(f"{item_type}: {item} - {size:.2f} MB - Última modificación: {time}")
            else:
                # Se imprime el tipo de archivo y el nombre del archivo
                print(f"{item_type}: {item}")
                
# Código de prueba
if __name__ == "__main__":
    # Crea una instancia de la clase FileProcessor
    processor = FileProcessor(".", "logs.txt")
    # Se llama el metodo list_folder_contents y se le envia el nombre de la carpeta que se desea listar y si se desean detalles
    processor.list_folder_contents("sample_folder", details=True)  # Cambia "sample_folder" por una carpeta existente