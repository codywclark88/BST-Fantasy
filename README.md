# Fantasy Football Dashboard

A retro-styled ESPN fantasy football history dashboard.

## Deploy to Railway (free)

### 1. Create a GitHub repo
- Go to github.com and create a new **private** repo (keeps your ESPN cookies private)
- Upload all files from this folder to the repo

### 2. Deploy on Railway
- Go to [railway.app](https://railway.app) and sign up (free)
- Click **New Project → Deploy from GitHub repo**
- Select your repo — Railway auto-detects Python and deploys

### 3. Set environment variables
In Railway's dashboard → your project → **Variables**, add:
```
ESPN_S2   = <your espn_s2 cookie value>
SWID      = <your SWID cookie value>
```
This keeps your credentials out of the code.

### 4. Open your dashboard
Railway gives you a public URL like `https://yourapp.up.railway.app`
That's it — share it with your league!

## Local development
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5050
```

## File structure
```
app.py                        — Flask server + ESPN proxy
requirements.txt              — Python dependencies  
Procfile                      — Tells Railway how to start the app
railway.json                  — Railway config
static/
  fantasy_dashboard.html      — The dashboard frontend
```
