# Login System - Quick Guide

## 🔐 Dashboard Access

Your Streamlit dashboard now has login protection!

### Login Credentials

**Username:** `Admin`  
**Password:** `Admin123`

---

## How to Use

### 1. Start Dashboard

```bash
streamlit run app.py
```

### 2. Login

You'll see a login screen with:
- 🏥 Velden Health branding
- Username field
- Password field  
- Login button

**Enter:**
- Username: `Admin`
- Password: `Admin123`

Click **Login**

### 3. Access Dashboard

After successful login:
- ✅ "Login successful!" message appears
- Dashboard loads automatically
- All features available

### 4. Logout

When finished:
- Look at left sidebar
- Scroll to bottom
- Click **"🚪 Logout"** button
- Returns to login screen

---

## Security Features

### Failed Login Attempts

- Maximum 3 attempts allowed
- Counter shows: "Attempt 1/3", "Attempt 2/3", etc.
- After 3 failures: "Too many failed attempts. Please refresh the page."

### Session Management

- Login persists during browser session
- Closing browser = automatic logout
- Refreshing page = stays logged in

### Logout Protection

- Manual logout via button
- Session cleared completely
- Must login again to access

---

## Changing Credentials

To update username/password:

1. Open `app.py`
2. Find these lines near the top:

```python
# Login credentials
USERNAME = "Admin"
PASSWORD = "Admin123"
```

3. Change to your desired values:

```python
# Login credentials
USERNAME = "YourUsername"
PASSWORD = "YourStrongPassword123!"
```

4. Save file
5. Restart dashboard

---

## For Deployment

### Streamlit Cloud

When deploying to Streamlit Cloud:

**Option 1: Use Streamlit Secrets (Recommended)**

1. In Streamlit Cloud dashboard → App Settings
2. Click "Secrets"
3. Add:
```toml
USERNAME = "Admin"
PASSWORD = "Admin123"
```

4. Update `app.py`:
```python
# Login credentials
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]
```

**Option 2: Environment Variables**

Similar but using environment variables instead of secrets.

### Security Best Practices

⚠️ **Important:**
- Change default password before deployment
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Don't commit passwords to public GitHub repos
- Use secrets/environment variables for production

---

## Multi-User Support

To add multiple users, update `app.py`:

```python
# Multiple users
USERS = {
    "Admin": "Admin123",
    "User1": "Password1",
    "User2": "Password2"
}

# In login_page function, change authentication check:
if username in USERS and USERS[username] == password:
    st.session_state.logged_in = True
    st.session_state.username = username  # Track who's logged in
    st.success(f"✅ Welcome {username}!")
    st.rerun()
```

---

## Troubleshooting

### Can't Login

**Check:**
- Username is exactly: `Admin` (case-sensitive)
- Password is exactly: `Admin123` (case-sensitive)
- No extra spaces before/after credentials

### Logout Button Not Visible

- Scroll down in sidebar
- Button is at bottom, below data refresh buttons

### Session Expired

- This is normal after browser close
- Just login again

### Forgot Password

Currently no password recovery (simple system).

**Solutions:**
1. Check this guide for default credentials
2. Edit `app.py` to reset password
3. Contact administrator (you!) to reset

---

## Current Login Flow

```
Start Dashboard
    ↓
[Login Screen]
    ↓
Enter: Admin / Admin123
    ↓
Click Login
    ↓
✅ Success → [Dashboard]
    ↓
Use all features
    ↓
Click Logout → Back to [Login Screen]
```

---

## Features Available After Login

Once logged in, you have full access to:

✅ Clinic data tab  
✅ Doctor data tab  
✅ All filters  
✅ Search functionality  
✅ Data refresh buttons  
✅ CSV export  
✅ All dashboard features  

---

**🔒 Your dashboard is now secure!**

Only users with the correct credentials can access your pipeline data.
