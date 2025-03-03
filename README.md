# Predicción de Precios de Arriendo en el Valle de Aburrá

Este proyecto tiene como objetivo desarrollar un modelo de predicción de precios de arriendo para propiedades residenciales en los municipios del Valle de Aburrá, Antioquia. A través de este trabajo, se busca proporcionar una herramienta útil para propietarios, inquilinos y agentes inmobiliarios, facilitando la toma de decisiones informadas en el mercado de arriendo.

## Estructura del Proyecto

El proyecto está organizado en varias carpetas y archivos, cada uno con un propósito específico:

- **data/**: Contiene los datos utilizados en el proyecto.
  - **raw/**: Datos extraídos directamente desde la API de Finca Raíz.
  - **processed/**: Datos después del preprocesamiento y limpieza.

- **notebooks/**: Incluye Jupyter notebooks para análisis y modelado.
  - **1_EDA.ipynb**: Análisis Exploratorio de Datos (EDA).
  - **2_Limpieza_Datos.ipynb**: Limpieza y preprocesamiento de datos.
  - **3_Modelos_Comparativos.ipynb**: Comparación de modelos, incluyendo Random Forest y Regresión Lineal.
  - **4_Red_Neuronal.ipynb**: Entrenamiento de la red neuronal.

- **src/**: Código fuente del proyecto.
  - **data_collection.py**: Obtención de datos desde la API.
  - **eda.py**: Funciones para el análisis exploratorio de datos.
  - **preprocessing.py**: Funciones para la limpieza y ingeniería de características.
  - **models/**: Modelos predictivos.
    - **random_forest.py**: Modelo Random Forest.
    - **linear_regression.py**: Modelo de Regresión Lineal.
    - **neural_network.py**: Modelo de Red Neuronal y su optimización.

- **reports/**: Visualizaciones y reportes de resultados.
  - **figures/**: Gráficos generados. **Pendiente
  - **results/**: Resultados de los modelos. **Pendiente

- **tests/**: Pruebas unitarias para asegurar la calidad del código. **Pendiente
  - **test_data_collection.py**: Pruebas del scraping de datos. **Pendiente
  - **test_preprocessing.py**: Pruebas de las funciones de limpieza de datos. **Pendiente
  - **test_models.py**: Pruebas de los modelos predictivos. **Pendiente

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes dependencias. Puedes encontrar la lista completa en el archivo `requirements.txt`.

## Uso

1. Clona el repositorio en tu máquina local.
2. Accede a la carpeta del proyecto.
3. Ejecuta los notebooks en el orden indicado para realizar el análisis y modelado.
4. Consulta los resultados en la carpeta `reports/results/` y las visualizaciones en `reports/figures/`.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o envía un pull request.