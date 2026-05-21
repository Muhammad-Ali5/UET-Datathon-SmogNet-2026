# 🌫️ SmogNet - AI-Powered Air Quality Prediction System

SmogNet is an intelligent air quality prediction and alert system for Pakistan, leveraging machine learning to forecast pollution levels and notify users through WhatsApp. It combines real-time weather data, historical pollution patterns, and predictive analytics to help citizens and authorities make informed decisions about air quality.

## 🎯 Project Overview

SmogNet provides:
- **Real-time AQI Predictions** - ML-powered forecasts for PM2.5, PM10, NO, NO₂, SO₂ across 5 major Pakistani cities
- **Interactive Dashboard** - Visualize historical trends and current air quality metrics
- **WhatsApp Alerts** - Instant notifications when pollution levels exceed safe thresholds
- **Chatbot Intelligence** - AI-powered chatbot to answer air quality questions (Groq/Llama integration)
- **Data Analytics** - Comprehensive analysis of pollution patterns from Aug 2021 to Dec 2024

**Cities Covered:** Lahore, Karachi, Islamabad, Peshawar, Quetta

---

## 📁 Project Structure

```
UET-Datathon-SmogNet-2026/
├── backend/                          # Flask API & ML services
│   ├── app.py                       # Main Flask application
│   ├── model_service.py             # ML model prediction engine
│   ├── alerts.py                    # Alert management logic
│   ├── weather.py                   # OpenWeather API integration
│   ├── config.py                    # Configuration management
│   ├── process_datasets.py          # Data processing pipeline
│   ├── .env.example                 # Environment variables template
│   └── README.md                    # Backend-specific docs
├── frontend/                         # Web interface
│   ├── index.html                   # Home page
│   ├── dashboard.html               # Main dashboard
│   ├── chatbot.html                 # AI chatbot interface
│   ├── alerts_manager_smognet.html  # Alert manager
│   ├── input.css                    # Tailwind CSS styles
│   ├── tailwind.config.js           # Tailwind configuration
│   ├── package.json                 # Frontend dependencies
│   └── aqi_data.json                # Sample AQI data
├── ml_models/                        # Pre-trained ML models
│   ├── best_smognet_model.pkl       # Main prediction model
│   └── label_encoder.pkl            # Label encoding utility
├── datasets/                         # Training & testing data
│   ├── Training/                    # Historical data Aug 2021 - Jul 2024
│   │   ├── concatenated_dataset_Aug_2021_to_July_2024.csv
│   │   ├── peshawar_complete_data.csv
│   │   └── [other city datasets]
│   └── Testing/                     # Test data Jul - Dec 2024
│       └── [city-specific test sets]
├── requirements.txt                  # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🛠️ Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Twilio Account** (for WhatsApp alerts)
- **OpenWeather API Key** (for real-time weather data)
- **Groq API Key** (optional, for AI chatbot)

---

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Muhammad-Ali5/UET-Datathon-SmogNet-2026.git
cd UET-Datathon-SmogNet-2026
```

### 2. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables
```powershell
copy backend\.env.example backend\.env
```

Edit `backend\.env` with your credentials:
```env
# API Keys
GROQ_API_KEY=your-groq-api-key
OPENWEATHER_API_KEY=your-openweather-key

# Twilio WhatsApp Settings
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_FROM=+14155238886

# Server Configuration
API_HOST=0.0.0.0
API_PORT=5000
ALERT_THRESHOLD=100
```

### 4. Start the Backend Server
```powershell
python backend\app.py
```

Server will start at: `http://127.0.0.1:5000`

### 5. Access the Application
Open your browser and navigate to:
- **Dashboard**: `http://127.0.0.1:5000/dashboard.html`
- **Chatbot**: `http://127.0.0.1:5000/chatbot.html`
- **Alert Manager**: `http://127.0.0.1:5000/alerts_manager_smognet.html`

---

## 🔌 API Endpoints

### Predictions
- `GET /api/predict?city=Lahore` - Get AQI prediction for a city
- `POST /api/predict` - Batch predictions

### Alerts
- `GET /api/alerts` - Fetch active alerts
- `POST /api/alert` - Trigger WhatsApp alert
- `DELETE /api/alerts/<alert_id>` - Dismiss alert

### Weather
- `GET /api/weather?city=Karachi` - Real-time weather data
- `GET /api/weather/history?city=Islamabad&days=30` - Historical weather

### Chat
- `POST /api/chat` - Send message to AI chatbot

---

## 📊 Key Features

### Machine Learning Model
- **Algorithm**: Trained on 3+ years of pollution data
- **Features**: PM2.5, PM10, NO, NO₂, SO₂, temperature, humidity, wind speed
- **Accuracy**: Optimized for Pakistan's regional climate patterns

### Real-time Data Integration
- OpenWeather API for current conditions
- Historical trends from Aug 2021 - Dec 2024
- Automated data refresh every 30 minutes

### Intelligent Alerts
- Threshold-based notifications
- WhatsApp integration via Twilio
- Historical alert tracking

### AI Chatbot
- Groq/Llama 3.3 70B model
- Pakistan-specific AQI knowledge
- Natural language understanding

---

## 🚀 Technologies Used

**Backend:**
- Flask - Web framework
- Pandas - Data processing
- Scikit-learn - Machine learning
- Requests - HTTP library
- Python-dotenv - Environment management

**Frontend:**
- HTML5/CSS3
- Tailwind CSS - Utility-first styling
- Vanilla JavaScript
- Responsive design

**External APIs:**
- OpenWeatherMap API
- Twilio WhatsApp API
- Groq AI API

**ML & Data:**
- Scikit-learn
- Pandas
- NumPy

---

## ⚙️ Configuration

### Backend Configuration (`backend/config.py`)
- Model paths
- API keys (externalized to `.env`)
- Alert thresholds
- SMTP settings

### Alert Thresholds
- **Good**: AQI < 50
- **Moderate**: AQI 50-100
- **Unhealthy for Sensitive**: AQI 101-150
- **Unhealthy**: AQI 151-200
- **Very Unhealthy**: AQI 201-300
- **Hazardous**: AQI > 300

---

## 🐛 Troubleshooting

### Backend Won't Start
- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies: `pip list`
- Check if port 5000 is available: `netstat -ano | findstr :5000`

### API Keys Not Working
- Verify `.env` file exists in `backend/` directory
- Check for typos in API keys
- Ensure keys have proper permissions on respective platforms

### WhatsApp Alerts Not Sending
- Confirm Twilio credentials are correct
- Verify phone number is in Twilio sandbox (if using trial)
- Check network connectivity
- Review Twilio logs for errors

### Model File Missing
- Ensure `ml_models/best_smognet_model.pkl` exists
- Download from cloud storage if missing
- Verify file integrity: File should be ~50MB

### CORS Errors
- Frontend and backend must use same domain/port
- Do not use `file://` protocol for frontend
- Access via `http://127.0.0.1:5000`

---

## 📈 Performance Metrics

- **Prediction Latency**: < 100ms per city
- **Model Accuracy**: ~82% (validation set)
- **Alert Delivery**: < 30 seconds (WhatsApp)
- **Data Refresh**: Every 30 minutes

---

## 📝 Notes

- The Flask backend serves all frontend pages; no separate web server needed
- Model predictions are cached to optimize performance
- WhatsApp alerts require active Twilio account with verified numbers
- All API communications use HTTPS in production
- Historical data covers Aug 2021 - Dec 2024 for 5 major cities

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Team

Developed for **UET Datathon 2026** - SmogNet Project

---

## 📞 Support

For issues and questions:
- Open an [Issue](https://github.com/Muhammad-Ali5/UET-Datathon-SmogNet-2026/issues)
- Check existing documentation in `backend/README.md`
- Review API endpoint specs above

---

**Last Updated:** May 2026
