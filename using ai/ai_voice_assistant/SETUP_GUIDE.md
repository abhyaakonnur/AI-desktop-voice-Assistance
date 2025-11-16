# SETUP & TROUBLESHOOTING GUIDE

## ❌ The "proxies" Error - SOLVED

**Error:** `Client.__init__() got an unexpected keyword argument 'proxies'`

**Root Cause:** OpenAI library version 1.3.0 is outdated and incompatible with current API.

**Solution:** ✅ **Already Fixed!**
- Updated `requirements.txt` to use `openai>=1.40.0`
- Installed the latest OpenAI library

---

## 🔑 CRITICAL: Set Your OpenAI API Key

The main issue preventing commands from working is the **missing/placeholder API key**.

### Step 1: Get an API Key
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in to OpenAI
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-`)

### Step 2: Update `.env` File
Open `.env` and replace:
```
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_API_KEY_HERE
```

with your actual key:
```
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

⚠️ **Do NOT share your API key with anyone!**

---

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
Run the setup script:
```powershell
Set-Location "C:\Users\WIN\Desktop\using ai\ai_voice_assistant"
.\setup.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Navigate to project
Set-Location "C:\Users\WIN\Desktop\using ai\ai_voice_assistant"

# 2. Update .env with your API key (use Notepad or VS Code)
notepad .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the web app
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 📋 Commands That Now Work

Once API key is set, these commands should work:

**Voice Assistant (CLI):**
```powershell
python assistant.py
```

**Web Interface:**
```powershell
python app.py
```
Then visit: `http://localhost:5000`

**Example Commands:**
- "What's the time?"
- "Open Firefox"
- "Open WhatsApp"
- "Search Wikipedia for Python"
- "Play music on YouTube"
- "Tell me a joke"

---

## 🔧 Troubleshooting

### Issue: Still getting "proxies" error
**Solution:** Clear Python cache and reinstall:
```powershell
Remove-Item -Path "__pycache__" -Recurse -Force
pip install --force-reinstall --no-cache-dir openai>=1.40.0
python test_openai_client.py
```

### Issue: "OPENAI_API_KEY not set"
**Solution:** Your `.env` file has the placeholder key. Replace it with your real key.

### Issue: Microphone not working
**Solution:** Check your Windows audio settings:
1. Open Settings > System > Sound
2. Verify microphone is selected and enabled
3. Test microphone in Sound settings

### Issue: Commands like "open firefox" not working
**Solution:** The web assistant tries to open URLs/apps. On Windows:
- "open firefox" → Opens Firefox browser
- "open whatsapp" → Opens default web browser (WhatsApp Web)
- For native apps, use full paths or ensure they're in your system PATH

---

## 📦 What Was Updated

1. **requirements.txt** - Updated `openai>=1.3.0` → `openai>=1.40.0`
2. **setup.ps1** - New setup automation script
3. **Python cache** - Cleared old `.pyc` files

---

## ✅ Verification

Test that everything works:
```powershell
Set-Location "C:\Users\WIN\Desktop\using ai\ai_voice_assistant"
python test_openai_client.py
```

Expected output:
```
OpenAI client created: <class 'openai.OpenAI'>
```

---

## 📞 Support

If you still have issues:
1. Check that your OpenAI API key is valid (not expired)
2. Verify internet connection is stable
3. Make sure Python 3.7+ is installed
4. Run `pip list` to verify all packages are installed

---

**Last Updated:** November 16, 2025
