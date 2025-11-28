# PhishGuard - Advanced Phishing Detection System

A hybrid machine learning-based phishing detection tool that combines URL feature analysis and visual website analysis to accurately identify phishing threats.

## Features

- **URL-based Detection**: Analyzes 30+ URL features including domain structure, SSL certificates, special characters, and redirects
- **Random Forest Classifier**: ~92% accuracy on phishing detection
- **User-Friendly Interface**: Modern, responsive web UI for easy URL submission
- **Real-time Analysis**: <3 seconds per URL check
- **Confidence Scoring**: Combined score from URL and visual analysis
- **Feature Transparency**: Shows top contributing features for each prediction

## Technologies Used

- **Backend**: Python 3, Flask
- **Machine Learning**: Scikit-Learn (Random Forest)
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript
- **Deployment**: Gunicorn, Render

## Project Structure

