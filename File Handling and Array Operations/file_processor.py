import os
import logging
from typing import List, Optional, Tuple
import pandas as pd
import pydicom
import numpy as np
from pydicom.pixel_data_handlers.util import apply_voi_lut
from PIL import Image
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

    """ Funcion enfocada en eleer archivos DICOM """
    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        # Obtenemos la ruta del archivo
        file_path = os.path.join(self.base_path, filename)

        # Validamos si existe el archivo
        if not os.path.exists(file_path):
            # Escribimos en el log, que el archivo que se intenta buscar no existe
            self.logger.error(f"The File '{filename}' does not exist.")
            # Imprimimos el error para el usuario
            print(f"The file '{filename}' does not exist.")
            return
        
        if not file_path.lower().endswith('.dcm'):
            # Escribimos en el log, que el archivo no es de type dcm
            self.logger.error(f"The File '{filename}' is not DCM type.")
            # Imprimimos el error para el usuario
            print(f"The File '{filename}' is not DCM type.")
            return

        try:
            # Leemos el archivo cdm
            dc_file = pydicom.dcmread(file_path)

            # Almacenamos la informacion necesario
            patient_name = dc_file.get("PatientName", "Unknowless")
            study_date = dc_file.get("StudyDate", "Unknowless")
            format_date = datetime.strptime(study_date, "%Y%m%d").strftime("%Y-%m-%d") if study_date != "Unknowless" else "0000-00-00"
            modality = dc_file.get("Modality", "Unknowless")

            # Titulo 
            print("\n DICOM Analisys")
            # Informacion del archivo esencial
            print(f" Patient Name: {patient_name}")
            print(f" Study Date: {format_date}")
            print(f" Modality: {modality}")

            # Se valida si se enviaron etiquetas exactas a buscar
            if tags:
                # Recorremos la lista de etiquetas que se quieren buscar
                for tag in tags:
                    # Convertimos las etiquetas a hexagonales (Los tomaba como enteros)
                    hex_tag = f"({tag[0]:04X}, {tag[1]:04X})"
                    # Se toma la informacion de la etiqueta señalada
                    element_taked = dc_file.get(tag, "Nothing")
                    # Se toma el valor exacto, sin tomar nada del alrededor
                    value = element_taked.value if hasattr(element_taked, "value") else element_taked
                    # Se imprime informacion solicitada al usuario
                    print(f" Tag {hex_tag}: {value}")

            # Validamos si se desea extraer la imagen
            if extract_image:
                # Almacenamos NumberOfFrames si llega a existir en el archivo, si no existe el valor por defecto es None
                quan_frames = getattr(dc_file, "NumberOfFrames", None)
                # Validamos la variable anterior para validar si es una o varias imagenes
                if quan_frames is None:
                    # Se valida  la cantidad de pexels dentro del array para deliverar si son 1 o varias imagenes
                    quan_frames = 1 if len(dc_file.pixel_array.shape) == 2 else dc_file.pixel_array.shape[0]
                # Se valida si contiene datos de imagen
                if "PixelData" in dc_file:
                    try: 
                        if quan_frames == 1:
                            # Creamos la ruta de la imagen
                            image_path = os.path.join(self.base_path, filename.replace(".dcm", ".png"))
                            # Llamamos al metodo para convertir la informacion de la imagen con PILLOW
                            self._save_single_image(dc_file, image_path)
                            # Se informa a usuario
                            print(f" Extracted image saved to {image_path}")
                        else: 
                            # Creamos la ruta de la imagen
                            image_path = os.path.join(self.base_path, filename.replace(".dcm", ".png"))
                            # Llamamos al metodo para convertir la informacion de la imagen con PILLOW
                            self._dicom_to_image(dc_file, image_path, quan_frames)
                            # Se informa a usuario
                            print(f" Extracted image saved to {image_path}")
                    except Exception as error:
                        # Se escribe un log indicandon que no se encontro imagen en los datos
                        self.logger.error(f"Error occurred while creating the image.")
                        # Se imprime al usuario que no existe imagen en al archivo
                        print(f"Error: An error occurred while creating the image.")

                else:
                    # Se escribe un log indicandon que no se encontro imagen en los datos
                    self.logger.error(f"The File '{file_path}' has no Pixel Data.")
                    # Se imprime al usuario que no existe imagen en al archivo
                    print(f"Error: '{filename}'has no image.")

        except pydicom.errors.InvalidDicomError:
            self.logger.error(f"The File '{file_path}' is not a DICOM valid.")
            print(f"Error: '{filename}' is not a DICOM valid.")

        except Exception as error:
            # Excribimos el error por el cual fallo
            self.logger.error(f"Error reading the dcm file: {error}")
            # Mensaje al usuario
            print(f" Error reading the dcm file: {error}")


    """ Funcion enfocada en crear una sola imagen que proviene del archivo origen """
    def _save_single_image(self, dicom_file, output_path):
        # Se convierte el dicom a un array de datos flotantes
        array = dicom_file.pixel_array.astype(np.float32)
        # Se aplica el VOI LUT al dicom (La informacion de la imagen)
        array = apply_voi_lut(array, dicom_file)
        # Normalizamos los datos de la imagen
        array = (array - array.min()) / (array.max() - array.min()) * 255
        # Convertimos los datos a entero
        image = Image.fromarray(array.astype(np.uint8))
        # Guardamos la imagen
        image.save(output_path)

    """ Funcion enfocada en crear un collage de imagen que proviene del archivo origen """
    def _dicom_to_image(self, dicom_file, output_path, num_frames):
        # Se convierte el dicom a un array de datos flotantes
        frames = dicom_file.pixel_array.astype(np.float32)
        # Se aplica el VOI LUT al dicom (La informacion de la imagen)
        frames = np.array([apply_voi_lut(frame, dicom_file) for frame in frames])
        # Normalizamos los datos de la imagen
        frames = (frames - frames.min()) / (frames.max() - frames.min()) * 255
        # Convertimos los datos a entero
        frames = frames.astype(np.uint8)
        # Se calcula el tamaño de la cuadrícula para el collage
        grid_size = int(np.ceil(np.sqrt(num_frames)))
        # Se asigna el tamaño de la imagen
        img_size = frames.shape[1]
        # Se crea el collage de imagenes en escalas de grises
        collage = Image.new("L", (grid_size * img_size, grid_size * img_size))
        # Se recorre la cantidad de frames
        for i in range(num_frames):
            x = (i % grid_size) * img_size
            y = (i // grid_size) * img_size
            # Se crea la imagen con Pillow
            img = Image.fromarray(frames[i])
            # Se pega la imagen en el collage
            collage.paste(img, (x, y))

        # Guardamos la imagen
        collage.save(output_path)
                
# Código de prueba
if __name__ == "__main__":
    # Crea una instancia de la clase FileProcessor
    processor = FileProcessor(".", "logs.txt")
    # Se llama el metodo list_folder_contents y se le envia el nombre de la carpeta que se desea listar y si se desean detalles
    processor.list_folder_contents("", details=True)
    # Se llama al metodo read_csv, se envia el nombre del archivo y si se desea guardar el reporte
    processor.read_csv("sample-02-csv.csv", report_path="averages_and_standard_deviations.txt", summary=True)
    # Se llama al metodo read_dicom, se envia el nombre del archivo, las etiquitas y si se desea extraer la imagen
    processor.read_dicom(
        filename="sample-02-dicom-2.dcm",
        tags=[(0x0010, 0x0010), (0x0008, 0x0060)],
        extract_image=True
    )