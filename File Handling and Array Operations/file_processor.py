import os
import logging
import pandas as pd
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
        print(f"\n The folder '{folder_name}' contains: {len(items)} elements:")

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

    """ Funcion enfocada en leer un archivo CSV """
    def read_csv(self, filename: str, report_path: str = None, summary: bool = False) -> None:
        # Ruta de la carpeta
        file_path = os.path.join(self.base_path, filename)

        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            # Escribimos un log indicando que el archivo no existe
            self.logger.error(f"The file SCV '{file_path}' does not exist.")
            # Imprimimos un mensaje de error indicando que el archivo no existe
            print(f"Error: The file SCV '{filename}' does not exist.")
            return
        
        # Verificamos que el archivo sea de tipo csv
        if not filename.lower().endswith('.csv'):
            # Escribimos un log indicando que el archivo no es de tipo csv
            self.logger.error(f"The file '{file_path}' does not a CSV type.")
            # Imprimimos un mensaje de error indicando que el archivo no es de tipo csv
            print(f"Error: The file '{file_path}' does not a CSV type.")
            return

        try:
            # Leemos el archivo CSV
            df = pd.read_csv(file_path)

            # Mostramos el nombre del archivo
            print(f"\n File Name CSV: {filename}")
            # Mostramos la cantidad de columnas y sus nombres
            print(f"\n Columns: {df.shape[1]} -> {list(df.columns)}")
            # Mostramos la cantidad de filas
            print(f" Rows: {df.shape[0]}")

            # Indicamos que las columnas son numéricas
            numeric_cols = df.select_dtypes(include=["number"])
            # Validamos que haya columnas numéricas
            if not numeric_cols.empty:
                try:

                    # Almacenamos estadísticas de media y desviación estandard
                    stats = numeric_cols.describe().loc[["mean", "std"]] 
                    print("\n Numeric Columns: ")
                    print(f"\n {stats}")

                    # Se valida si hay ruta para crear el reporte
                    if report_path:
                        # Se crea o se ingresa a la ruta del reporte
                        report_file = os.path.join(self.base_path, report_path)
                        # Se genera el reporte de estadísticas en un archivo txt con formato CSV y tabulaciones
                        stats.to_csv(report_file, sep="\t")
                        # Informamos al usuario que se ha generado el reporte
                        print(f"\n Report saved in: {report_file}")
                        
                except Exception as error:
                    # Almacenamos en el log el error
                    self.logger.error(f"Error when trying to calculate numeric columns, check the file: {str(error)}")
                    # Imprimimos el error
                    print(f"Error when trying to calculate numeric columns, check the file: {str(error)}")


            # Verificamos si se desea realizar un resumen, si es verdadero se analisarán las columnas no numéricas
            if summary:
                # Indicamos que las columnas no son numéricas
                non_numeric_cols = df.select_dtypes(exclude=["number"])
                # Validamos que haya columnas no numéricas
                if not non_numeric_cols.empty:
                    # Informamos que el analisis de columnas no numericas
                    print("\n Non-Numeric Summary:")
                    # Recorremos las columnas
                    for col in non_numeric_cols:
                        # Asignamos el valor total de las columnas
                        column_no_numeric = df[col].nunique()
                        # Imprimimos la cantidad de valores unicos
                        print(f"\n Name: Unique Values: = {column_no_numeric}")

        except pd.errors.EmptyDataError:
            # Almacenamos en el log el error
            self.logger.error(f"The file '{file_path}' is empty or is invalid: {str(error)}")
            # Imprimimos el error
            print(f" The file '{file_path}' is empty or is invalid: {str(error)}")
            
        except pd.errors.ParserError:
            # Almacenamos el error en el log
            self.logger.error(f"Error when trying to analize the file '{file_path}'. Wrong Format.")
            print(f" Error when trying to analize the file '{file_path}'. Check the Format.")

        except Exception as error:
            # Almacenamos en el log el error
            self.logger.error(f"Error reading CSV '{file_path}': {str(error)}")
            # Imprimimos el error
            print(f" Error readig the file: {str(error)}")
                
# Código de prueba
if __name__ == "__main__":
    # Crea una instancia de la clase FileProcessor
    processor = FileProcessor(".", "logs.txt")
    # Se llama el metodo list_folder_contents y se le envia el nombre de la carpeta que se desea listar y si se desean detalles
    processor.list_folder_contents("", details=True)  # Cambia "sample_folder" por una carpeta existente
    # Se llama al metodo read_csv, se envia el nombre del archivo y si se desea guardar el reporte
    processor.read_csv("sample-02-csv.csv", report_path="averages_and_standard_deviations.txt", summary=True)