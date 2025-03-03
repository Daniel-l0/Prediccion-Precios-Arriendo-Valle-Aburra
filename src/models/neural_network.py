f#### Modelo de la optimizacion 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.optimizers import RMSprop
###--------------------------------------------------###
# Cargar datos
def load_data(filepath):
    df = pd.read_excel(filepath)
    df['precio_log'] = np.log1p(df['precio'])
    df = df.drop(columns=['precio'])
    return df

# Procesamiento de datos
def preprocess_data(df):
    target = 'precio_log'
    categorical_features = ['ciudad', 'antiguedad', 'comuna', 'zona', 'tipo_de_inmueble', 'estado']
    numerical_features = df.drop(columns=categorical_features + [target]).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    X = df.drop(columns=[target])
    y = df[target].values.reshape(-1, 1)
    target_scaler = StandardScaler()
    y = target_scaler.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return preprocessor, target_scaler, X_train, X_test, y_train, y_test

# Entrenamiento de la red neuronal
def train_neural_network(X_train, X_test, y_train, y_test, preprocessor, target_scaler):
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)
    

    # Definición del modelo
    # Definición del modelo con los mejores hiperparámetros encontrados
    model = Sequential([
        Input(shape=(X_train_transformed.shape[1],)),

        # Capa 1
        Dense(384, activation='tanh'),
        BatchNormalization(),
        Dropout(0.1),

        # Capa 2
        Dense(192, activation='leaky_relu'),
        BatchNormalization(),
        Dropout(0.3),

        # Capa 3 (no es necesaria según los mejores hiperparámetros, pero si deseas usarla, podría ser ajustada)
        Dense(320, activation='sigmoid'),
        BatchNormalization(),
        Dropout(0.3),

        # Capa de salida
        Dense(1)
    ])

    # Compilación del modelo con el optimizador rmsprop y la tasa de aprendizaje encontrada
    optimizer = RMSprop(learning_rate=0.00012122536697831619)
    model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
    history = model.fit(X_train_transformed, y_train, epochs=200, batch_size=64, validation_split=0.2, verbose=0)

    
    # Obtener las predicciones y reescalar la variable objetivo a su escala original
    predictions = model.predict(X_test_transformed).flatten()
    predictions = target_scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
    
    y_test = target_scaler.inverse_transform(y_test).flatten()
    y_test = np.expm1(y_test)
    predictions = np.expm1(predictions)

    # Evaluar el modelo
    evaluate_model(predictions, y_test)
    
    return model, predictions, history

# Evaluación del modelo
def evaluate_model(predictions, y_test):
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print(f"MAE: {mae}")
    print(f"RMSE: {rmse}")
    print(f"R2 Score: {r2}")
    
    plt.figure(figsize=(7, 4))
    sns.scatterplot(x=y_test, y=predictions, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    plt.ticklabel_format(style='plain')
    plt.xlabel('Valores reales')
    plt.ylabel('Predicciones')
    plt.title('Valores reales vs Predicciones')
    plt.show()

# Cargar y procesar datos
filepath = '../data/processed/data_arriendos_model.xlsx'
df = load_data(filepath)
preprocessor, target_scaler, X_train, X_test, y_train, y_test = preprocess_data(df)

# Entrenar modelo
nn_model_x, nn_predictions_x, history = train_neural_network(X_train, X_test, y_train, y_test, preprocessor, target_scaler)