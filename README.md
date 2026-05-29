# 🌾 Crop Disease Detector

An AI-powered web application for detecting crop diseases using machine learning. Upload a photo of a crop leaf, and get instant disease identification with detailed symptoms and treatment recommendations.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔬 **60+ Disease Detection** - Comprehensive database covering 15+ crop types
- 🤖 **AI-Powered** - Uses state-of-the-art deep learning models (ResNet, EfficientNet)
- 💊 **Treatment Recommendations** - Detailed symptoms and treatment guidance for each disease
- 🌐 **Web Interface** - User-friendly Flask-based web application
- 📊 **REST API** - Easy integration with other applications
- 💾 **SQLite Database** - Persistent storage for predictions and disease knowledge
- 🎯 **Multi-Model Ensemble** - Combines multiple specialized models for better accuracy

## 🌱 Supported Crops

### Cereals
- **Wheat** - Leaf rust, stem rust, stripe rust, powdery mildew, fusarium head blight, septoria leaf blotch
- **Rice** - Blast, bacterial blight, brown spot, tungro, sheath blight
- **Maize/Corn** - Common rust, northern leaf blight, gray leaf spot, southern leaf blight, tar spot

### Vegetables
- **Tomato** - Early blight, late blight, leaf mold, septoria leaf spot, bacterial spot, fusarium wilt, verticillium wilt, mosaic virus
- **Potato** - Early blight, late blight, blackleg, common scab
- **Pepper** - Bacterial spot, anthracnose

### Cash Crops
- **Cotton** - Fusarium wilt, verticillium wilt, bacterial blight
- **Soybean** - Rust, frogeye leaf spot, white mold, sudden death syndrome
- **Cassava** - Bacterial blight, brown streak disease, mosaic disease, green mottle

### Fruits
- **Apple** - Scab, fire blight, powdery mildew
- **Grape** - Powdery mildew, downy mildew, black rot
- **Banana** - Panama disease, black sigatoka
- **Citrus** - Greening (HLB), canker

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/didi5-com/crop-disease-detector.git
cd crop-disease-detector
```

2. **Navigate to the Python site directory**
```bash
cd python_site
```

3. **Create a virtual environment**
```bash
python -m venv .venv
```

4. **Activate the virtual environment**

Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

Windows (CMD):
```cmd
.venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source .venv/bin/activate
```

5. **Install dependencies**
```bash
pip install -r requirements.txt
```

6. **Set up environment variables**
```bash
cp .env.example .env
```

7. **Initialize the database**
```bash
python scripts/init_db.py
```

8. **Run the application**
```bash
python run.py
```

9. **Open your browser**
```
http://127.0.0.1:5000
```

## 📖 Usage

### Web Interface

1. Open http://127.0.0.1:5000 in your browser
2. Upload a clear photo of a crop leaf
3. (Optional) Select the crop type for better accuracy
4. Click "Analyze"
5. View the disease prediction with confidence score, symptoms, and treatment recommendations

### API Usage

#### Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

#### Predict Disease
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -F "leaf_image=@/path/to/leaf.jpg" \
  -F "crop_type=tomato"
```

**Response:**
```json
{
  "cropType": "tomato",
  "diseaseName": "Tomato Late Blight",
  "confidence": 0.92,
  "severity": "high",
  "isHealthy": false,
  "treatment": "Immediate sanitation, weather-based fungicide scheduling, and resistant varieties.",
  "topCandidates": [
    {
      "cropType": "tomato",
      "diseaseName": "Tomato Late Blight",
      "confidence": 0.92,
      "sources": ["global-multicrop", "local-finetuned"]
    }
  ]
}
```

## 🏗️ Project Structure

```
crop-disease-detector/
├── python_site/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── routes.py            # Web routes and API endpoints
│   │   ├── inference.py         # ML inference engine
│   │   ├── models.py            # Database models
│   │   ├── seed_data.py         # Disease library (60+ diseases)
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database setup
│   │   ├── utils.py             # Helper functions
│   │   ├── static/              # CSS, JS, images
│   │   └── templates/           # HTML templates
│   ├── scripts/
│   │   ├── init_db.py           # Database initialization
│   │   ├── build_dataset.py     # Dataset builder
│   │   └── train_model.py       # Model training
│   ├── instance/                # SQLite database
│   ├── models/                  # ML model checkpoints
│   ├── uploads/                 # Uploaded images
│   ├── .env.example             # Environment variables template
│   ├── requirements.txt         # Python dependencies
│   ├── run.py                   # Application entry point
│   └── README.md               # Detailed documentation
├── .gitignore
└── README.md                    # This file
```

## 🧠 How It Works

1. **Image Upload** - User uploads a crop leaf image
2. **Preprocessing** - Image is resized and normalized
3. **Multi-Model Inference** - Multiple specialized models analyze the image:
   - Local fine-tuned model (if available)
   - Global multi-crop model
   - Crop-specific specialist models (cassava, rice)
4. **Ensemble Prediction** - Results are weighted and combined
5. **Disease Matching** - Prediction is matched against disease library
6. **Response** - Returns disease name, confidence, symptoms, and treatment

## Demo Notes

For the most reliable live demo right now, present the scanner with these crops:
- Tomato
- Potato
- Maize
- Pepper
- Cassava
- Rice
- Apple
- Grape

Wheat and sugarcane are still represented in the knowledge base, but they do not yet have the same level of dataset/model coverage as the crops above.

## 🔧 Configuration

Edit `python_site/.env` to customize:

```env
SECRET_KEY=your-secret-key-here
UNKNOWN_THRESHOLD=0.45          # Minimum confidence threshold
TOP_K=3                         # Number of top predictions to return
PRIMARY_MODEL_ID=mesabo/agri-plant-disease-resnet50
CASSAVA_MODEL_ID=nexusbert/resnet50-cassava-finetuned
RICE_MODEL_ID=prithivMLmods/Rice-Leaf-Disease
HF_TOKEN=your_hugging_face_token  # Optional, for private models
```

## 🎓 Training Your Own Model

1. **Build a dataset**
```bash
python scripts/build_dataset.py --output dataset/combined
```

By default this now merges:
- `mohanty/PlantVillage` from Hugging Face
- `avinashhm/plant-disease-classification-complete` tomato images from Hugging Face for more real-world tomato variation

To also merge your own downloaded tomato folders:
```bash
python scripts/build_dataset.py \
  --output dataset/combined \
  --local-image-folder path/to/your/tomato_dataset
```

Your local folder can use either:
- `train/Tomato___Late_Blight/*.jpg` style splits, or
- a simple class-folder root like `Tomato___Late_Blight/*.jpg`

2. **Train the model**
```bash
python scripts/train_model.py \
  --data-dir dataset/combined \
  --epochs 10 \
  --output models/local_classifier.pt
```

3. **The app automatically uses your trained model** (`models/local_classifier.pt`)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- 🌍 Add more crop diseases
- 🎨 Improve UI/UX
- 🧪 Add more ML models
- 📱 Create mobile app
- 🌐 Add internationalization
- 📊 Add analytics dashboard

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face** - For hosting pre-trained models
- **PyTorch** - Deep learning framework
- **Flask** - Web framework
- **Plant Disease Datasets** - Various open-source agricultural datasets

## 📧 Contact

- **GitHub:** [@didi5-com](https://github.com/didi5-com)
- **Email:** lovedidi500@gmail.com

## 🐛 Known Issues

- Large model downloads may take time on first run
- GPU acceleration not yet implemented (CPU inference only)
- Limited to image-based detection (no sensor data integration)

## 🗺️ Roadmap

- [ ] Add GPU support for faster inference
- [ ] Implement real-time video analysis
- [ ] Add mobile app (iOS/Android)
- [ ] Integrate weather data for better predictions
- [ ] Add multi-language support
- [ ] Create farmer community features
- [ ] Add treatment product recommendations
- [ ] Implement disease progression tracking

---

**Made with ❤️ for farmers and agricultural professionals worldwide** 🌾
#   a k u n n a - c r o p - d i s e a s e - d e t e c t o r  
 