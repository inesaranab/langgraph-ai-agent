# Fresh Deployment Checklist

## 🚀 Creating Fresh Railway Project

### Step 1: Create New Railway Project
1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"** 
4. Choose **"langgraph-ai-agent"** repository
5. Railway will auto-detect Python and start building

### Step 2: Configure Railway Environment
**IMPORTANT**: Do NOT set API keys as environment variables!

Your app is designed for users to provide their own API keys dynamically through the frontend settings modal. This is more secure and scalable.

Railway will deploy without environment variables - this is expected and correct.

### Step 3: Get Railway URL
- Copy the Railway URL (looks like: `https://your-app-name.up.railway.app`)

---

## 🌐 Creating Fresh Vercel Project

### Step 1: Create New Vercel Project  
1. Go to [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import **"langgraph-ai-agent"** repository
4. **IMPORTANT**: Set **Root Directory** to `frontend`
5. Vercel will auto-detect Next.js and deploy

### Step 2: Get Vercel URL
- Copy the Vercel URL (looks like: `https://your-app-name.vercel.app`)

---

## 🔧 Update Project URLs

### Step 1: Update the Script
1. Open `update_deployment_urls.py`
2. Replace:
   ```python
   NEW_RAILWAY_URL = "YOUR_NEW_RAILWAY_URL_HERE"
   NEW_VERCEL_URL = "YOUR_NEW_VERCEL_URL_HERE"
   ```
   With your actual URLs:
   ```python
   NEW_RAILWAY_URL = "https://your-new-railway-app.up.railway.app" 
   NEW_VERCEL_URL = "https://your-new-app.vercel.app"
   ```

### Step 2: Run the Update Script
```bash
python update_deployment_urls.py
```

### Step 3: Commit Changes
```bash
git add .
git commit -m "Update to fresh Railway and Vercel deployments"
git push origin main
```

---

## ✅ Test New Deployments

### Test Railway Backend
```bash
# Test health endpoint
curl https://your-new-railway-app.up.railway.app/health

# Test with your API keys
python test_chat_with_keys.py
```

### Test Vercel Frontend
1. Visit your new Vercel URL
2. Open Settings modal
3. Add your API keys
4. Test a chat message

---

## 🎯 Why This Will Work Better

1. **Clean State**: Fresh deployments without any cached issues
2. **Proper Environment**: Railway will have environment variables from start  
3. **No Confusion**: Clear separation between old and new deployments
4. **Faster Debugging**: If issues arise, they'll be deployment-specific, not code issues

---

## 📝 What We Fixed in the Code

- ✅ Removed `SecretStr` wrapper causing validation errors
- ✅ Fixed source extraction in LangGraph Agent v2  
- ✅ Updated health endpoints to show correct status
- ✅ All local testing passes

The code is ready - we just need fresh deployment environments!