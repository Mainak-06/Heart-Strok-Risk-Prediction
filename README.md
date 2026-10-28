🫀 Heart & Stroke Risk Prediction

A Streamlit web app that estimates cardiovascular risk from a patient's health inputs using a K-Nearest Neighbors (KNN) model.

🔗 Live demo: heart-strok-risk-prediction.streamlit.app

⚠️ Disclaimer: This project is for educational purposes only. It is not a medical device and must not be used for diagnosis or treatment decisions. Always consult a qualified healthcare professional.

📌 Overview

The app takes a person's health details through a simple form, applies the same preprocessing used during training, and returns a predicted risk (high / low).

<!-- TODO: One or two sentences on what exactly is predicted (heart disease? stroke?) and make the repo name, app title and this text consistent. -->
✨ Features
Interactive Streamlit form for entering health parameters
Pre-trained KNN classifier loaded from a saved model file
Consistent preprocessing using the saved scaler and column order
Instant prediction result in the browser
🧠 How It Works
The user fills in the input form in app.py.
The inputs are converted into a single-row table and aligned to the training columns (heart_columns.PKL).
Features are scaled with the fitted scaler (heart_scaler.PKL).
The KNN model (knn_heart_model.PKL) predicts the risk class.
The result is displayed in the app.
🗂️ Repository Structure
Heart-Strok-Risk-Prediction/
├── app.py                  # Streamlit application
├── knn_heart_model.PKL     # Trained KNN model
├── heart_scaler.PKL        # Fitted scaler (feature scaling)
├── heart_columns.PKL       # Column order / encoded feature names
├── requirements.txt        # Python dependencies
└── README.md
📊 Dataset & Model
Item	Details
Dataset	<!-- TODO: name + link (e.g. Kaggle) -->
Target	<!-- TODO: e.g. HeartDisease (0 = no, 1 = yes) -->
Model	K-Nearest Neighbors (scikit-learn)
Preprocessing	One-hot encoding of categorical features + feature scaling
Accuracy	<!-- TODO: e.g. 0.87 on the test set -->
Other metrics	<!-- TODO: precision / recall / F1 / ROC-AUC -->
Input features
<!-- TODO: list the inputs from the app form, for example: -->
Feature	Description
Age	Age in years
...	...
🚀 Run Locally
bash
# 1. Clone the repository
git clone https://github.com/Mainak-06/Heart-Strok-Risk-Prediction.git
cd Heart-Strok-Risk-Prediction

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py

The app opens at http://localhost:8501.

🛠️ Tech Stack
Python
Streamlit
scikit-learn (KNN, scaler)
pandas, NumPy
joblib / pickle for model persistence
⚠️ Limitations
KNN does not give well-calibrated probabilities, so treat the output as a rough indicator.
Performance depends on the training dataset, which may not represent all populations.
The model has not been clinically validated.
🔮 Future Improvements
Show a probability score and a plain-language explanation of the result
Compare with other models (Logistic Regression, Random Forest, XGBoost)
Add model evaluation notebook and training script for reproducibility
Add input validation and unit tests

👤 Author

Mainak · GitHub @Mainak-06
