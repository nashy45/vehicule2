# 📧 Email Notification Setup Instructions

Your website is now configured to send you an email whenever someone submits the contact form!

## ✅ What's Been Set Up

- ✅ Email notifications using Gmail
- ✅ Notifications sent to: **Paatymurray@gmail.com**
- ✅ Contact form messages still saved to database
- ✅ Works even if email fails

## 🔐 Required: Gmail App Password

To send emails, you need a **Gmail App Password** (NOT your regular Gmail password).

### Step-by-Step Setup (5 minutes):

1. **Go to your Google Account**:
   - Visit: https://myaccount.google.com/

2. **Enable 2-Step Verification** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

3. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in if prompted
   - Select app: **Mail**
   - Select device: **Windows Computer** (or Other)
   - Click **Generate**
   - Copy the **16-character password** (it looks like: `abcd efgh ijkl mnop`)

4. **Add Password to Your App**:
   - Open: `app.py`
   - Find this line (around line 22):
     ```python
     app.config['MAIL_PASSWORD'] = 'your-app-password-here'
     ```
   - Replace `'your-app-password-here'` with your App Password:
     ```python
     app.config['MAIL_PASSWORD'] = 'abcdefghijklmnop'  # Your 16-char password (no spaces)
     ```
   - Save the file

5. **Install Email Package**:
   ```cmd
   pip install Flask-Mail
   ```

6. **Restart Your Application**:
   - Stop the server (Ctrl+C)
   - Run `start.bat` again

## ✅ Test It!

1. Go to your Contact page: http://127.0.0.1:5000/contact
2. Fill out the form and submit
3. Check your email: **Paatymurray@gmail.com**
4. You should receive an email with the inquiry details!

## 📧 What You'll Receive

When someone sends a message, you'll get an email like this:

```
Subject: New Contact Form Inquiry - Douala Vehicles

New inquiry from your website!

Name: John Doe
Phone: +237 XXX XXX XXX
Email: john@example.com

Message:
I'm interested in the Toyota Camry...

---
This inquiry has been saved to your database.
Login to your admin panel to manage: http://127.0.0.1:5000/admin/login
```

## 🔧 Troubleshooting

### Email Not Sending?

**Check 1: App Password**
- Make sure you used an App Password (not your regular Gmail password)
- No spaces in the password in `app.py`

**Check 2: 2-Step Verification**
- Must be enabled on your Google account

**Check 3: Gmail Security**
- Check Gmail security alerts
- Approve any blocked sign-in attempts

**Check 4: Email Address**
- Verify `Paatymurray@gmail.com` is correct in `app.py` (line 20 and 21)

### Still Having Issues?

1. Check the Command Prompt window for error messages
2. Make sure Flask-Mail is installed: `pip list | findstr Flask-Mail`
3. Try sending a test email from Python console

## 📱 Alternative: WhatsApp Notifications

If email doesn't work or you prefer WhatsApp, I can set up WhatsApp notifications instead using:
- Twilio API (paid, but reliable)
- WhatsApp Business API (free but more setup)

Just let me know if you want WhatsApp instead!

## 🎯 Current Setup Summary

- **Email From**: Paatymurray@gmail.com
- **Email To**: Paatymurray@gmail.com
- **Email Server**: Gmail (smtp.gmail.com)
- **Backup**: All inquiries saved to database
- **Admin Panel**: View all inquiries at /admin/inquiries

## 📝 Next Steps

1. ✅ Get your Gmail App Password
2. ✅ Add it to `app.py`
3. ✅ Restart the server
4. ✅ Test the contact form
5. ✅ Check your email!

---

**Need help?** Let me know if you have any issues setting this up!
