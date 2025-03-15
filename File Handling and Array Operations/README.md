# FileProcessor - Manejo y Análisis de Archivos en Python

FileProcessor es una aplicación en Python creada para leer archivos, analizar y realizar diferentes calculos por archivo. 
Permite listar archivos en carpetas, analizar archivos CSV, y procesar imágenes médicas en formato DICOM.  

## Características

- Listar el contenido de una carpeta y mostrar detalles de los archivos.  

- Leer archivos CSV, calcular estadísticas y generar reportes.  

- Analizar archivos DICOM, extraer información clave y convertir imágenes a PNG.  

- Manejo logs automáticos.  

## **Librerías Utilizadas**
La aplicación usa las siguientes librerías de Python:  

- **pydicom**
- **numpy**
- **Pillow**
- **Pandas**

Para instalarlas se usado el comando:

pip install pydicom numpy pillow pandas

Para correr el codigo se corre de esta manera:

python file_processor.py