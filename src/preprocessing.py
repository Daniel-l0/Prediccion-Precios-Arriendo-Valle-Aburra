# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

# def load_data(file_path):
#     """Load the dataset from a specified file path."""
#     data = pd.read_csv(file_path)
#     return data

# def clean_data(data):
#     """Clean the dataset by handling missing values and duplicates."""
#     data = data.drop_duplicates()
#     data = data.dropna()
#     return data

# def feature_engineering(data):
#     """Perform feature engineering on the dataset."""
#     # Example: Convert categorical variables to dummy variables
#     data = pd.get_dummies(data, drop_first=True)
#     return data

# def preprocess_data(file_path):
#     """Load, clean, and preprocess the data."""
#     data = load_data(file_path)
#     data = clean_data(data)
#     data = feature_engineering(data)
#     return data

# def scale_features(X):
#     """Scale features using StandardScaler."""
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
#     return X_scaled

# def split_data(data, target_column):
#     """Split the data into features and target variable."""
#     X = data.drop(columns=[target_column])
#     y = data[target_column]
#     X_scaled = scale_features(X)
#     X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
#     return X_train, X_test, y_train, y_test