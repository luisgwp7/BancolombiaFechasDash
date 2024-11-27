# Bancolombia comparación de fechas 




### Guía de instalación

Este tutorial te guiará a través de los pasos para instalar los requisitos necesarios para ejecutar el programa.

### Requisitos del sistema

- *Versión de Python*:  
  Debes tener *Python 3.12.4* o superior instalado en tu sistema.

### Librerias de uso

Este proyecto requiere las siguientes librerías de Python:

- pandas
- dash
- dash-bootstrap-components
- plotly
- statistics (biblioteca estándar de Python)
- gdown
- socket (biblioteca estándar de Python)
- fastparquet
- pyarrow
  
### Paso 1: Crear un entorno virtual

Para evitar conflictos entre las versiones de librerías, se recomienda crear un entorno virtual para este proyecto.

1. Abre una terminal o consola de comandos.
2. Navega al directorio donde deseas almacenar el proyecto.
3. Crea un entorno virtual con el siguiente comando:
   ```bash
   python -m venv nombre_del_entorno
   ```
4. Activar el entorno
   En windows:
   
   ```bash
   cd nombre_del_entorno/Scripts/activate
   ```
   Si genera error o no ejecuta, entonces 
   ```bash
   cd nombre_del_entorno/Scripts
   ```
   Y despues, para activar, ejecute
   ```bash
   ./activate.ps1
   ```
5. Instalación de requirements:
   Ubiquese en el archivo requirements.txt
   Después, ejecute
   ```bash
   pip install -r requirements 
   ```

### Paso 2: Ejecución del código.

- Si es Visual Studio Code, puede seleccionar su entorno y ejecutar, ya sea el archivo .py o .ipynb 
- Si es por conda de hacer la instalación del entorno en conda y ejecutar con:
   ```bash
   Python AppBancolombia.py
   ```
### Paso 3: Ejecución del código.

- Si trabaja en jupyter asegurese de seguir el url al final del output para visualizar el dashboard en otra pestaña

 Puede ser algo así:
```bash 
 * Running on http://127.0.0.1:8080
```

- Si trabaja en Python o desde terminal, debe aparecer algo así: 

```bash 
Downloading...
From: https://drive.google.com/uc?id=ID_file_used&export=download
To: C:\Users\suUser\Documents\yourFolder\Bancolombia_FECHAS_dash.parquet
100%|███████████████████████████████████████████████████████████████████████████████████| 59.3M/59.3M [00:39<00:00, 1.51MB/s]
Dash is running on http://127.0.0.1:8080/

 * Serving Flask app 'appbancolombia'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.        
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```
Esto lo llevara a una pesataña de navegador y desde allí podrá usar el dashboard 

## Dashboard 

Al final del ejercicio, debe ver algo como esto: 

![image](https://github.com/user-attachments/assets/1800ac2d-4ba8-45c4-ba85-c1d5e5e2a1cc)




## Nota: 
Si surge un error en la instalación de los requirements, verifique su versión de python. En caso de que el error persista, es posible que deba instalar Microsoft C++ Build Tools, esto debido a la libreria de fastparquet. 

Si surge un error diferente, por favor comunicarse con Luis Guerrero en el siguiente correo: lguerrero@camacol.org.co, para el mantenimiento del código.  
