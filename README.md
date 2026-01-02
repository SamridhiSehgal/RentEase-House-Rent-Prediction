🏠 RentEase: Indian House Rent Prediction & Deployment
RentEase is a complete end-to-end Machine Learning project designed to predict house rental prices in major Indian cities. It encompasses data cleaning, predictive modeling using XGBoost, and a web-based deployment interface.

📁 Project Structure
Following the repository organization:

app.py: The core Flask application that handles the web backend and model inference.

house-rent_prediction.ipynb: The Jupyter notebook containing the full data science pipeline, from EDA to model training.

rentease_final_model_.pkl: The trained and serialized XGBoost regression model.

rentease_final_encoder_.pkl: The saved One-Hot Encoder used to transform categorical inputs.

templates/: Directory containing HTML files for the web interface.

static/ (via script.js & style.css): Contains frontend logic and styling for the application.

requirements.txt: List of all Python dependencies required to run the project.

🚀 Features
High-Accuracy Modeling: Utilizes an XGBoost Regressor tuned to handle complex rental market data.

Intelligent Data Preprocessing: Features a custom pipeline that handles missing values, standardized city names via fuzzy matching, and manages price outliers.

Interactive Web UI: A clean interface where users can input house details (BHK, Size, Locality, etc.) and receive an instant price estimate.

Robust Input Handling: The backend includes logic to handle "Other" categories for cities and localities not present in the training set.

🛠️ Tech Stack
Machine Learning: Python, XGBoost, Scikit-Learn, Pandas, NumPy.

Preprocessing: FuzzyWuzzy (Levenshtein distance for text cleaning).

Web Framework: Flask.

Frontend: HTML5, CSS3, JavaScript.

🔧 Installation & Setup
Clone the repository:

Bash

git clone https://github.com/SamridhiSehgal/RentEase-ML-deploy.git
cd RentEase-ML-deploy
Create a Virtual Environment:

Bash

python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
Install Dependencies:

Bash

pip install -r requirements.txt
Run the Application:

Bash

python app.py
Access the app at http://127.0.0.1:5000/.

📊 Model Performance
R² Score: ~0.70

Mean Absolute Error (MAE): ₹10,587.44

Target Transformation: Log transformation was used on the rent values to improve model stability and minimize skewness.

📺 Demonstration
(Optional: Insert a GIF or a link to a video showing the application predicting a rent value based on user input.)![reneaseml](https://github.com/user-attachments/assets/64740610-a8b7-4167-b116-7a09c453772d)
