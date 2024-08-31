import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def parse_budget_range(budget_str):
    """Parse budget string into a tuple of min and max budget."""
    budget_map = {
        "251 juta - 500 juta": (251_000_000, 500_000_000),
        "501 juta - 750 juta": (501_000_000, 750_000_000),
        "751 juta - 1 miliar": (751_000_000, 1_000_000_000),
        "1,5 miliar - 2 miliar": (1_500_000_000, 2_000_000_000),
        "2,1 miliar - 3 miliar": (2_100_000_000, 3_000_000_000),
    }
    return budget_map.get(budget_str, (0, float('inf')))

def prepare_data(architects_data, project_area):
    """Prepare features and labels from the architect data."""
    cities = [architect['city'] for architect in architects_data]
    themes = [architect['most_frequent_theme'] for architect in architects_data]
    rates = [architect['rate'] if architect['rate'] else 0 for architect in architects_data]

    # Calculate estimated budget
    estimated_budgets = [rate * project_area for rate in rates]

    # Normalize estimated budgets
    scaler = MinMaxScaler()
    estimated_budgets_scaled = scaler.fit_transform(np.array(estimated_budgets).reshape(-1, 1))

    # Convert categorical data to numeric
    city_encoder = LabelEncoder()
    theme_encoder = LabelEncoder()
    
    cities_encoded = city_encoder.fit_transform(cities)
    themes_encoded = theme_encoder.fit_transform(themes)
    
    X = np.column_stack((cities_encoded, themes_encoded, estimated_budgets_scaled))

    return X, city_encoder, theme_encoder, scaler

def recommend_architect(project_data, architects_data, k=5):
    project_city = project_data.get('city')
    project_theme = project_data.get('theme')
    project_area = int(project_data.get('area'))
    project_budget_str = project_data.get('budget')
    project_budget_min, project_budget_max = parse_budget_range(project_budget_str)
    project_budget_mid = (project_budget_min + project_budget_max) / 2

    # Prepare data
    X, city_encoder, theme_encoder, scaler = prepare_data(architects_data, project_area)

    # Prepare the project data point
    project_city_encoded = city_encoder.transform([project_city])[0] if project_city in city_encoder.classes_ else -1
    project_theme_encoded = theme_encoder.transform([project_theme])[0] if project_theme in theme_encoder.classes_ else -1
    project_estimated_budget = project_budget_mid

    # Scale project estimated budget
    project_estimated_budget_scaled = scaler.transform([[project_estimated_budget]])[0][0]
    
    # Scale the project data point to match the normalized data
    project_features = np.array([[project_city_encoded, project_theme_encoded, project_estimated_budget_scaled]])
    
    # Fit k-NN model
    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(X, X)  # Fit using X as both features and targets

    # Get the nearest neighbors
    distances, indices = knn.kneighbors(project_features)

    # Retrieve the recommended architects
    recommended_architects = [architects_data[idx] for idx in indices[0]]

    # Format the output
    formatted_recommendations = [
        {
            **architect,
            "distance": distance
        }
        for architect, distance in zip(recommended_architects, distances[0])
    ]
    
    return formatted_recommendations