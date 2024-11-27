# Librerias
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from statistics import mean
import gdown
import socket


#----------------------------------------------------------------------------------------------------
# File to use: https://drive.google.com/file/d/1H2tXm2IisTHBlszjIohY_e2DEP6hAWkN/view?usp=drive_link 
# This file will be upgraded every month 
#----------------------------------------------------------------------------------------------------

file_id = "1H2tXm2IisTHBlszjIohY_e2DEP6hAWkN"
url = f"https://drive.google.com/uc?id={file_id}&export=download"
output = "Bancolombia_FECHAS_dash.parquet"
gdown.download(url, output, quiet=False)

# Leer el archivo parquet
bancolombia_fechas_join = pd.read_parquet(output)


# Iniciar Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# Listas las opciones para filtros y parámetros en el dashboard 
tamanio_constructora_options = [{'label': size, 'value': size} for size in bancolombia_fechas_join['Tamaño constructora'].unique() if pd.notna(size)]
segmento_options = [{'label': seg, 'value': seg} for seg in bancolombia_fechas_join['Segmento'].unique() if pd.notna(seg)]
regional_options = [{'label': reg, 'value': reg} for reg in bancolombia_fechas_join['regional'].unique() if pd.notna(reg)]
ciudad_options = [{'label': ciudad, 'value': ciudad} for ciudad in bancolombia_fechas_join['ciudad'].unique() if pd.notna(ciudad)]
corte_options = [{'label': corte, 'value': corte} for corte in bancolombia_fechas_join['corte'].unique() if pd.notna(corte)]

app.layout = html.Div(
    style={
        'padding': '20px',  
        'margin': '20px',   
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',  
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  
    },
    children=[
        html.Div([
            html.H3("______________________________________________________________________________________________________"),
            html.H3("¿Desea filtrar la base de datos?"),
            html.P(
                children=[
                    html.Strong("Uso: "),  
                    "Si su selección fue no, la programación solo tendrá en cuenta la sección de parámetros. "
                    "Caso contrario, tendrá en cuenta la sección de filtros y de parámetros."
                ]
            ),
            html.Label("¿Desea filtrar?"),
            dcc.Dropdown(
                id='variable_filtro',
                options=[{'label': 'Si', 'value': 'si'}, {'label': 'No', 'value': 'no'}]
            ),
            # Fila 1: Filtros y Parámetros
            html.Div(className='row', children=[
                # Columna de filtros
                html.Div(className='col', children=[
                    html.H3("_____________________________________________"),
                    html.H3("Sección de filtros"),
                    html.P(
                        children=[
                            html.Strong("Uso: "),  
                            "Debe seleccionar la variable que quiere filtrar. Por ejemplo, 'Tamaño constructora'. Note que "
                            "hay varios filtros entre las opciones, sin embargo, solo el de la variable por filtrar afectará el gráfico."
                        ]
                    ),
                    html.Label("Variable por filtrar:"),
                    dcc.Dropdown(
                        id='variable_por_filtra',
                        options=[
                            {'label': 'Segmento', 'value': 'Segmento'},
                            {'label': 'Tamaño constructora', 'value': 'Tamaño constructora'},
                            {'label': 'regional', 'value': 'regional'},
                            {'label': 'ciudad', 'value': 'ciudad'}
                        ]
                    ),
                    html.Label("Tamaño constructora:"),
                    dcc.Dropdown(id='filtro_tamaño_constructora', options=tamanio_constructora_options),
                    html.Label("Segmento:"),
                    dcc.Dropdown(id='filtro_segmento', options=segmento_options),
                    html.Label("Región:"),
                    dcc.Dropdown(id='filtro_region', options=regional_options),
                    html.Label("Ciudad:"),
                    dcc.Dropdown(id='filtro_ciudad', options=ciudad_options),
                ]),
                # Columna de parámetros
                html.Div(className='col', children=[
                    html.H3("_____________________________________________"),
                    html.H3("Sección de parámetros"),
                    html.P(
                        children=[
                            html.Strong("Uso: "),  
                            "La variable de comparación representará el eje Y del gráfico, es decir, por qué variable quiere desglosar la información."
                        ]
                    ),
                    html.Label("Variable comparación:"),
                    dcc.Dropdown(
                        id='variable_comparacion',
                        options=[
                            {'label': 'Proyecto', 'value': 'Proyecto'},
                            {'label': 'Constructora', 'value': 'Constructora'},
                            {'label': 'regional', 'value': 'regional'},
                            {'label': 'ciudad', 'value': 'ciudad'},
                            {'label': 'Tamaño constructora', 'value': 'Tamaño constructora'},
                            {'label': 'Segmento', 'value': 'Segmento'}
                        ]
                    ),
                    html.Label("Fecha comparación:"),
                    dcc.Dropdown(
                        id='fecha_comparacion',
                        options=[
                            {'label': 'Fecha inicio venta', 'value': 'Fecha inicio venta'},
                            {'label': 'Fecha inicio construccion', 'value': 'Fecha inicio construccion'},
                            {'label': 'Fecha terminacion construccion', 'value': 'Fecha terminacion construccion'},
                            {'label': 'Fecha entrega', 'value': 'Fecha entrega'}
                        ]
                    ),
                    html.Label("Corte:"),
                    dcc.Dropdown(id='corte', options=corte_options),
                    html.Label("Corte anterior:"),
                    dcc.Dropdown(id='corte_anterior', options=corte_options),
                    html.Label("Alerta:"),
                    dcc.Input(id='alerta', type='number'),
                    html.Label("Bajo:"),
                    dcc.Input(id='bajo', type='number'),
                ]),
            ]),
            # Fila 2: detalles de la selección 
            html.Div(id='output-details', className='row', children=[
                html.H3("______________________________________________________________________________________________________"),
                html.H3("Detalles de Análisis"),
                html.Div(id='total-datos'),
                html.Div(id='promedio-variacion1'),
                html.Div(id='promedio-variacion2'),
                html.Div(id='nota'),
            ]),
            # Fila 3: Gráficos
            html.H3("______________________________________________________________________________________________________"),
            html.H3("Gráficos"),
            html.Div(className='row', children=[
                dcc.Graph(id='bar_fig'),
            ]),
            html.Div(className='row', children=[
                dcc.Graph(id='hist_fig'),
            ])
        ])
    ]
)
# Callback para actualizar los gráficos basados en los filtros y parámetros seleccionados
# @app.route('/')
@app.callback(
    [Output('bar_fig', 'figure'), 
     Output('hist_fig', 'figure'),
     Output('total-datos', 'children'),
     Output('promedio-variacion1', 'children'),
     Output('promedio-variacion2', 'children'),
     Output('nota', 'children')],
    [
        Input('variable_filtro', 'value'),
        Input('variable_por_filtra', 'value'),
        Input('filtro_tamaño_constructora', 'value'),
        Input('filtro_segmento', 'value'),
        Input('filtro_region', 'value'),
        Input('filtro_ciudad', 'value'),
        Input('variable_comparacion', 'value'),
        Input('fecha_comparacion', 'value'),
        Input('corte', 'value'),
        Input('corte_anterior', 'value'),
        Input('alerta', 'value'),
        Input('bajo', 'value')
    ]
)
def update_graphs(variable_filtro, variable_por_filtra, filtro_tamano, filtro_segmento, filtro_region, filtro_ciudad, 
                  variable_comparacion, fecha_comparacion, corte, corte_anterior, alerta, bajo):

    try:

        if variable_filtro == 'si':

            bancolombia_comparacion = bancolombia_fechas_join.copy()
        
            if variable_por_filtra == 'regional':
              bancolombia_comparacion = bancolombia_comparacion[bancolombia_comparacion[variable_por_filtra] == filtro_region]
            elif variable_por_filtra == 'Tamaño constructora':
              bancolombia_comparacion = bancolombia_comparacion[bancolombia_comparacion[variable_por_filtra] == filtro_tamano]
            elif variable_por_filtra == 'Segmento':
              bancolombia_comparacion = bancolombia_comparacion[bancolombia_comparacion[variable_por_filtra] == filtro_segmento]
            else:
              print("Por favor seleccione un filtro por variable que sea válido. Verifique que el string de la variable esté bien escrito")
              print("Recuerde que las variables a filtrar son: 'regional', 'Tamaño constructora',  'Segmento'")
        
            df_hoy = bancolombia_comparacion[bancolombia_comparacion['corte'] == corte]
            # Se toman fechas que no estén proyectadas
            num_date = float(df_hoy.num_date.unique()[0])
            df_hoy = df_hoy[df_hoy[fecha_comparacion] <= num_date]
        
            df_antes = bancolombia_comparacion[bancolombia_comparacion['corte'] == corte_anterior]
            # Se toman fechas superiores al corte
            num_date = float(df_antes.num_date.unique()[0])
            df_antes= df_antes[df_antes[fecha_comparacion] > num_date]
        
        
            df_merged = pd.merge(
                df_hoy[[variable_comparacion, 'idetapa', fecha_comparacion]],
                df_antes[[variable_comparacion, 'idetapa', fecha_comparacion]],
                on=[variable_comparacion, 'idetapa'],
                suffixes=(f'_{corte}', f'_{corte_anterior}')
            )
        
            df_merged[f'{fecha_comparacion}_{corte}'] = pd.to_datetime(df_merged[f'{fecha_comparacion}_{corte}'], format='%Y%m%d', errors='coerce')
            df_merged[f'{fecha_comparacion}_{corte_anterior}'] = pd.to_datetime(df_merged[f'{fecha_comparacion}_{corte_anterior}'], format='%Y%m%d', errors='coerce')
        
        
            df_merged['variacion_dias'] = (df_merged[f'{fecha_comparacion}_{corte}'] - df_merged[f'{fecha_comparacion}_{corte_anterior}']).dt.days
            df_merged['variacion_meses'] = df_merged['variacion_dias']//30
        
            df_avg_variacion = df_merged.groupby(variable_comparacion)['variacion_meses'].mean().reset_index()
        
            df_avg_variacion = df_avg_variacion.dropna(subset=['variacion_meses'])
        
            df_avg_variacion = df_avg_variacion.sort_values(by=['variacion_meses'], ascending=False)
        
            # Crear columna de colores basada en condiciones
            df_avg_variacion['Indicador'] = df_avg_variacion['variacion_meses'].apply(
                lambda x: 'Alerta!' if x > int(alerta) else ('medio' if x >= int(bajo) else 'bajo')
            )
            print(f'Total datos analizados según el filtro y condiciones : {df_avg_variacion.shape[0]}')
            total_datos = f'Total datos analizados según el filtro y condiciones: {df_avg_variacion.shape[0]}'
            
            promedio_variacion1 = f'Promedio de variación 1: {round(mean(df_avg_variacion["variacion_meses"]), 2)} meses'
            
            detalles_df = df_avg_variacion.copy()
            detalles_df = detalles_df[detalles_df['variacion_meses'] > 0]
            
            promedio_variacion2 = f'Promedio de variación 2*: {round(mean(detalles_df["variacion_meses"]), 2)} meses'
            nota = 'Nota*: No tiene en cuenta aquellos que su variación fue cero o menor a cero'
            
    
        else:
            bancolombia_comparacion = bancolombia_fechas_join.copy()
        
            df_hoy = bancolombia_comparacion[bancolombia_comparacion['corte'] == corte]
            # Se toman fechas que no estén proyectadas
            num_date = float(df_hoy.num_date.unique()[0])
            df_hoy = df_hoy[df_hoy[fecha_comparacion] <= num_date]
        
            df_antes = bancolombia_comparacion[bancolombia_comparacion['corte'] == corte_anterior]
            # Se toman fechas superiores al corte
            num_date = float(df_antes.num_date.unique()[0])
            df_antes= df_antes[df_antes[fecha_comparacion] > num_date]
        
        
            df_merged = pd.merge(
                df_hoy[[variable_comparacion, 'idetapa', fecha_comparacion]],
                df_antes[[variable_comparacion, 'idetapa', fecha_comparacion]],
                on=[variable_comparacion, 'idetapa'],
                suffixes=(f'_{corte}', f'_{corte_anterior}')
            )
        
            df_merged[f'{fecha_comparacion}_{corte}'] = pd.to_datetime(df_merged[f'{fecha_comparacion}_{corte}'], format='%Y%m%d', errors='coerce')
            df_merged[f'{fecha_comparacion}_{corte_anterior}'] = pd.to_datetime(df_merged[f'{fecha_comparacion}_{corte_anterior}'], format='%Y%m%d', errors='coerce')
        
        
            df_merged['variacion_dias'] = (df_merged[f'{fecha_comparacion}_{corte}'] - df_merged[f'{fecha_comparacion}_{corte_anterior}']).dt.days
            df_merged['variacion_meses'] = df_merged['variacion_dias']//30
        
            df_avg_variacion = df_merged.groupby(variable_comparacion)['variacion_meses'].mean().reset_index()
        
            df_avg_variacion = df_avg_variacion.dropna(subset=['variacion_meses'])
        
            df_avg_variacion = df_avg_variacion.sort_values(by=['variacion_meses'], ascending=False)
        
            # Crear columna de colores basada en condiciones
            df_avg_variacion['Indicador'] = df_avg_variacion['variacion_meses'].apply(
                lambda x: 'Alerta!' if x > int(alerta) else ('medio' if x >= int(bajo) else 'bajo')
            )
        
            print(f'Total datos analizados según el filtro y condiciones : {df_avg_variacion.shape[0]}')
            total_datos = f'Total datos analizados según el filtro y condiciones: {df_avg_variacion.shape[0]}'
            
            promedio_variacion1 = f'Promedio de variación 1: {round(mean(df_avg_variacion["variacion_meses"]), 2)} meses'
            
            detalles_df = df_avg_variacion.copy()
            detalles_df = detalles_df[detalles_df['variacion_meses'] > 0]
            
            promedio_variacion2 = f'Promedio de variación 2*: {round(mean(detalles_df["variacion_meses"]), 2)} meses'
            nota = 'Nota*: No tiene en cuenta aquellos que su variación fue cero o menor a cero'
            
        
        bar_fig = px.bar(
              df_avg_variacion,
              y=variable_comparacion,
              x='variacion_meses',
              labels={variable_comparacion: variable_comparacion, 'variacion_meses': 'Promedio Variación en Meses'},
              title=f"{variable_comparacion} con Variación en {fecha_comparacion} por Etapas ({corte} vs {corte_anterior})",
              color='Indicador',  # Asigna colores basados en la columna 'color'
              color_discrete_map={
                  'Alerta!': '#ba181b',
                  'medio': '#f7b801',
                  'bajo': '#affc41'
              }
          );
        
        bar_fig.update_layout(
              bargap=0.1,
              width=1500,
              height=800
          );
        
        
        # Gráfico_distribucion
        variacion_counts = df_merged['variacion_meses'].value_counts().sort_index()
        df_variacion = pd.DataFrame({'variacion_meses': variacion_counts.index, 'count': variacion_counts.values})
        
        hist_fig = px.histogram(
              df_variacion,
              x="variacion_meses",
              y="count",
              nbins=40,
              title=f"Distribución de variación en meses en {variable_comparacion}",
          );
        
        hist_fig.update_layout(
              xaxis_title="Variación en meses",
              yaxis_title="Frecuencia",
              bargap=0.1,
              width=1500,
              height=800
          );

    except Exception as e:
        bar_fig = {}
        hist_fig = {}
        total_datos = "Error procesando datos."
        promedio_variacion1 = ""
        promedio_variacion2 = ""
        nota = f"Error: {str(e)}"
    

    return bar_fig, hist_fig, total_datos, promedio_variacion1, promedio_variacion2, nota





def find_available_port(start_port=8080, max_tries=10):
    """
    Encuentra un puerto disponible, comenzando en `start_port`.
    Intenta hasta `start_port + max_tries` antes de fallar.
    """
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))  
                return port  
            except OSError:
                continue  
    raise RuntimeError("No se encontraron puertos disponibles.")

if __name__ == '__main__':
    try:
        port = find_available_port(start_port=8080, max_tries=50)
        app.run_server(host='127.0.0.1', port=port, debug=False)
        print(f"El servidor está corriendo en http://127.0.0.1:{port}")
    except RuntimeError as e:
        print("Error:", str(e))

