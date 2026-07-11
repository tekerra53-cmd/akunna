# 🚀 Quick Start Guide

## What You Have

A fully functional **Crop Disease Detection System** with:
- ✅ 60+ crop diseases across 15+ crop types
- ✅ AI-powered disease detection using ML models
- ✅ Detailed symptoms and treatment recommendations
- ✅ Flask web application with REST API
- ✅ SQLite database for disease knowledge

## Current Status

✅ **Flask Server:** Running at http://127.0.0.1:5000
✅ **Database:** Initialized with 60+ diseases
✅ **Disease Library:** Expanded and ready
✅ **Ready for GitHub:** All files prepared

## Next Steps

### 1. Test Your Application (Now)

Open your browser and go to: **http://127.0.0.1:5000**

Try uploading crop leaf images to test disease detection!

### 2. Upload to GitHub (After Installing Git)

**Quick Steps:**
1. Install Git: https://git-scm.com/download/win
2. Create repository on GitHub: https://github.com/new
   - Name: `crop-disease-detector`
3. Get Personal Access Token: https://github.com/settings/tokens
4. Run: `.\upload_to_github.ps1`

**Detailed Instructions:** See `GITHUB_UPLOAD_INSTRUCTIONS.md`

## Supported Crops & Diseases

### 🌾 Cereals
- **Wheat:** 6 diseases (rusts, powdery mildew, fusarium head blight, etc.)
- **Rice:** 5 diseases (blast, bacterial blight, brown spot, tungro, sheath blight)
- **Maize/Corn:** 5 diseases (rusts, blights, gray leaf spot, tar spot)

### 🥔 Vegetables
- **Tomato:** 8 diseases (early/late blight, leaf mold, septoria, bacterial spot, wilts, mosaic virus)
- **Potato:** 4 diseases (early/late blight, blackleg, common scab)
- **Pepper:** 2 diseases (bacterial spot, anthracnose)

### 🌱 Cash Crops
- **Cotton:** 3 diseases (fusarium wilt, verticillium wilt, bacterial blight)
- **Soybean:** 4 diseases (rust, frogeye leaf spot, white mold, sudden death syndrome)
- **Cassava:** 4 diseases (bacterial blight, brown streak, mosaic, green mottle)

### 🍎 Fruits
- **Apple:** 3 diseases (scab, fire blight, powdery mildew)
- **Grape:** 3 diseases (powdery mildew, downy mildew, black rot)
- **Banana:** 2 diseases (Panama disease, black sigatoka)
- **Citrus:** 2 diseases (greening, canker)

## API Endpoints

### Health Check
```bash
GET http://127.0.0.1:5000/api/health
```

### Predict Disease
```bash
POST http://127.0.0.1:5000/api/predict
Content-Type: multipart/form-data

Parameters:
- leaf_image: (file) Image of crop leaf
- crop_type: (optional) Crop type hint (e.g., "tomato", "wheat", "rice")
```

## Project Structure

```
python_site/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Web routes and API endpoints
│   ├── inference.py         # ML inference engine
│   ├── models.py            # Database models
│   ├── seed_data.py         # Disease library (60+ diseases)
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── utils.py             # Helper functions
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── scripts/
│   ├── init_db.py           # Database initialization
│   ├── build_dataset.py     # Dataset builder
│   └── train_model.py       # Model training
├── instance/
│   └── crop_disease.db      # SQLite database
├── models/                  # ML model checkpoints
├── uploads/                 # Uploaded images
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # Documentation
```

## Environment Variables

Located in `python_site/.env`:

```env
SECRET_KEY=change-me
UNKNOWN_THRESHOLD=0.45
TOP_K=3
PRIMARY_MODEL_ID=mesabo/agri-plant-disease-resnet50
CASSAVA_MODEL_ID=nexusbert/resnet50-cassava-finetuned
RICE_MODEL_ID=prithivMLmods/Rice-Leaf-Disease
# HF_TOKEN=your_hugging_face_token_if_needed
```

## Stopping the Server

The Flask server is currently running in the background. To stop it:

1. Check running processes
2. Press Ctrl+C in the terminal where it's running
3. Or close the terminal window

## Need Help?

- **Setup Issues:** Check `python_site/README.md`
- **GitHub Upload:** Check `GITHUB_UPLOAD_INSTRUCTIONS.md`
- **API Documentation:** Check the `/api/health` endpoint

## What's Next?

1. ✅ Test the application with real crop images
2. ⏳ Upload to GitHub (waiting for Git installation)
3. 🔄 Share with others
4. 🚀 Deploy to production (Heroku, AWS, Azure, etc.)
5. 📊 Collect feedback and improve the model

---

**Your Crop Disease Detector is ready to use!** 🌱🔬
