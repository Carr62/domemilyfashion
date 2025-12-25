# DOMEMILY Fashion Site - Deployment Guide

## ✅ Pre-Deployment Checklist

### 1. Create your `.env` file
```bash
cp .env.example .env
```

Then edit `.env` with your production values:
```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

---

## 🚀 Hosting Options

### Option A: Railway (Recommended - Easy & Free Tier)
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Add environment variables in Railway dashboard
5. Deploy!

### Option B: Render
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repo
5. Set environment variables
6. Deploy!

### Option C: PythonAnywhere (Free Tier Available)
1. Create account at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your code
3. Configure WSGI file
4. Set up static files
5. Add domain

### Option D: Heroku
```bash
heroku create domemily-fashion
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
git push heroku main
heroku run python manage.py migrate
```

---

## 📁 Project Structure
```
fashion_site/
├── .env                 # Your secrets (DON'T commit!)
├── .env.example         # Template for .env
├── .gitignore           # Files to ignore in git
├── Procfile             # For Heroku/Railway
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version
├── manage.py
├── db.sqlite3           # SQLite database
├── media/               # User uploads
├── staticfiles/         # Collected static files (generated)
├── fashion/             # Main app
└── fashion_site/        # Project settings
```

---

## ⚠️ Important Notes

1. **Never commit `.env`** - It contains secrets!
2. **Media files** - For production, consider using cloud storage (AWS S3, Cloudinary)
3. **Database** - SQLite works for small sites. For scale, use PostgreSQL
4. **HTTPS** - Always use HTTPS in production (most hosts provide free SSL)

---

## 🔧 Local Development
```bash
# Run development server
python manage.py runserver

# Access at http://127.0.0.1:8000
# Admin at http://127.0.0.1:8000/admin
# Dashboard at http://127.0.0.1:8000/dashboard/
```

---

## 📞 Support
For issues, check:
- Django Docs: https://docs.djangoproject.com
- Your hosting provider's documentation
