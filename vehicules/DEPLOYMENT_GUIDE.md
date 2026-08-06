# 🚀 Deployment Guide - Host Your Website Online

## Option 1: PythonAnywhere (FREE) ⭐ RECOMMENDED

Perfect for beginners and small businesses. Your site will be live at: `yourusername.pythonanywhere.com`

### Step-by-Step Deployment (30 minutes):

#### 1. Create Account
1. Go to: https://www.pythonanywhere.com
2. Click **"Start running Python online in less than a minute!"**
3. Sign up for **FREE Beginner Account**
4. Verify your email

#### 2. Upload Your Files
1. In PythonAnywhere Dashboard, click **"Files"**
2. Click **"Upload a file"**
3. Upload these files from your computer:
   - `app.py`
   - `requirements.txt`
   - Zip your `templates` folder → upload → unzip
   - Zip your `static` folder → upload → unzip

**OR** Use Git (if you know how):
```bash
git clone your-repository-url
```

#### 3. Set Up Virtual Environment
1. Click **"Consoles"** → **"Bash"**
2. Run these commands:
```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 myenv

# Install packages
pip install -r requirements.txt

# Create database
python app.py
# Press Ctrl+C after it creates database
```

#### 4. Configure Web App
1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Flask"**
4. Python version: **3.10**
5. Path: `/home/yourusername/app.py`

#### 5. Set WSGI Configuration
1. In Web tab, click on WSGI configuration file link
2. Find the Flask section
3. Change the path to your app:
```python
from app import app as application
```

#### 6. Set Static Files
In **"Web"** tab, under **"Static files"**:
- URL: `/static/`
- Directory: `/home/yourusename/static/`

#### 7. Go Live!
1. Click **"Reload"** button (green button)
2. Visit: `https://yourusername.pythonanywhere.com`
3. Your site is LIVE! 🎉

### 🌐 Custom Domain (Optional - $5/month)
1. Upgrade to **Hacker plan** ($5/month)
2. Buy domain (Namecheap, GoDaddy: $10-15/year)
3. Configure CNAME records
4. Add domain in PythonAnywhere settings

---

## Option 2: Render (FREE with Custom Domain)

Free tier with automatic HTTPS and custom domain support.

### Deployment Steps:

#### 1. Prepare for Deployment
Create `render.yaml` file:
```yaml
services:
  - type: web
    name: douala-vehicles
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

Add `gunicorn` to `requirements.txt`:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
Flask-Mail==0.9.1
gunicorn==21.2.0
```

#### 2. Create GitHub Repository
1. Create account on GitHub.com
2. Create new repository
3. Upload your project files

#### 3. Deploy on Render
1. Go to: https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - Name: `douala-vehicles`
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment

Your site will be live at: `https://douala-vehicles.onrender.com`

### Custom Domain (FREE on Render):
1. Buy domain ($10-15/year)
2. Add CNAME record pointing to Render
3. Add custom domain in Render dashboard

---

## Option 3: Railway.app ($5 Free Credit/Month)

Modern platform, very easy deployment.

### Deployment Steps:

#### 1. Prepare Files
Add `Procfile`:
```
web: gunicorn app:app
```

Add to `requirements.txt`:
```
gunicorn==21.2.0
```

#### 2. Deploy
1. Go to: https://railway.app
2. Sign up with GitHub
3. Click **"New Project"**
4. Choose **"Deploy from GitHub repo"**
5. Select your repository
6. Railway auto-detects Python and deploys!
7. Get public URL from dashboard

**Cost**: $5 free credit/month, then ~$5-10/month

---

## 🔧 Important: Update for Production

Before deploying, update `app.py`:

### 1. Change Secret Key
```python
app.config['SECRET_KEY'] = 'your-actual-long-random-secret-key-here'
```
Generate one:
```python
import secrets
print(secrets.token_hex(32))
```

### 2. Update Database for Production (PythonAnywhere)
```python
# Change this line in app.py:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yourusername/database.db'
```

### 3. Disable Debug Mode
At bottom of `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=False)  # Change to False
```

### 4. Update Contact Information
Update all phone numbers, emails, and addresses in:
- `templates/base.html` (navigation & footer)
- `templates/contact.html`
- `templates/index.html`
- `app.py` (email configuration)

---

## 📊 Comparison Table

| Hosting | Cost | Setup Time | Best For | Custom Domain |
|---------|------|------------|----------|---------------|
| **PythonAnywhere** | Free-$5/mo | 30 min | Beginners | $5/mo |
| **Render** | Free | 40 min | Free w/ domain | FREE |
| **Railway** | $5 credit | 20 min | Easy deploy | FREE |
| **Heroku** | $7/mo | 40 min | Reliable | FREE |
| **VPS** | $5-12/mo | 2-3 hrs | Tech-savvy | FREE |

---

## 🎯 My Recommendation

### For You: Start with **PythonAnywhere FREE**

**Reasons**:
1. ✅ No cost to start
2. ✅ Easy setup (30 minutes)
3. ✅ Perfect for Flask
4. ✅ Good enough for 100+ daily visitors
5. ✅ Upgrade later if needed

### When to Upgrade:
- More than 1000 visitors/day → Railway ($7/mo)
- Need custom domain → PythonAnywhere Hacker ($5/mo) or Render (free)
- High traffic → VPS ($12/mo)

---

## 🆘 Deployment Help

Need help deploying? I can guide you through:
1. PythonAnywhere setup
2. GitHub repository creation
3. Custom domain configuration
4. SSL certificate setup
5. Database migration

Just let me know which option you choose!

---

## 📱 After Deployment

1. **Test everything**:
   - Homepage loads
   - Inventory page works
   - Contact form sends emails
   - Admin panel login works
   - Images display correctly

2. **Update URLs**:
   - Google Maps location
   - Social media links
   - Email templates

3. **Monitor**:
   - Check admin panel for inquiries
   - Test email notifications
   - Monitor site speed

---

## 🔐 Security Checklist

Before going live:
- [ ] Changed SECRET_KEY
- [ ] Changed admin password
- [ ] Added Gmail App Password
- [ ] Disabled debug mode
- [ ] Updated all placeholder text
- [ ] Tested on mobile devices
- [ ] Set up HTTPS (automatic on most platforms)

---

**Ready to deploy? Follow the PythonAnywhere guide above!** 🚀
