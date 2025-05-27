from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
CORS(app)

# Load data
with open('data.json') as f:
    data = json.load(f)
df = pd.DataFrame(data).dropna(subset=['score'])

features = ['price', 'area', 'propertyType', 'inventoryType', 'bhk',
            'furnishing', 'reraApproved', 'possession', 'facing']
X = df[features]
y = df['score']

cat_cols = ['area', 'propertyType', 'inventoryType', 'furnishing', 'possession', 'facing']
num_cols = ['price', 'bhk', 'reraApproved']

cat_pipe = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                     ('encoder', OneHotEncoder(handle_unknown='ignore'))])
num_pipe = Pipeline([('imputer', SimpleImputer(strategy='mean'))])

preprocessor = ColumnTransformer([
    ('cat', cat_pipe, cat_cols),
    ('num', num_pipe, num_cols)
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])
model.fit(X, y)

@app.route('/recommend', methods=['POST'])
def recommend():
    input_data = request.json
    df['predicted_score'] = model.predict(X)
    top = df.sort_values(by='predicted_score', ascending=False).head(10)
    return jsonify(top[features + ['name', 'predicted_score']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
