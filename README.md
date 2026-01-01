# RentEase Frontend

Quick setup to run the Flask backend and frontend for the rent prediction model.

Prerequisites:
- Python 3.8+

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser to use the frontend.

Notes:
- The server will look for model files `rentease_final_model_.pkl` or `rentease_final_model.pkl` and encoder files `rentease_final_encoder_.pkl` or `rentease_final_encoder.pkl` in the project root.