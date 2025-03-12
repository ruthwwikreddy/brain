# AI Second Brain - Ruthwik's Personal Knowledge System

## 📌 Overview
This project is an **AI-powered Second Brain** that integrates **Obsidian notes** with **Ollama's AI models** to provide intelligent, personalized responses based on stored knowledge. It acts as an extension of your thinking, allowing you to query your past notes and get relevant, AI-generated insights.

## 🚀 Features
- **Obsidian Vault Integration**: Uses markdown notes as a knowledge base.
- **AI-Powered Responses**: Queries Ollama AI models like `mistral:latest` and `gemma:2b`.
- **Fast Caching**: Optimized for performance with a 10-minute cache refresh.
- **Flask API**: Provides endpoints for querying the AI and managing models.
- **Web Interface Support**: Serves a static `index.html` page for UI integration.

---

# 🔧 Setup Guide

## 1️⃣ Install Prerequisites
Before running the Second Brain, ensure you have the required dependencies installed:

### ✅ Install Python (if not installed)
Ensure Python 3.8+ is installed. You can check by running:
```sh
python --version
```

### ✅ Install Flask & Requests
```sh
pip install flask requests
```

### ✅ Install Ollama (Local AI Models)
Download and install Ollama from [Ollama's website](https://ollama.ai). Once installed, start the Ollama server:
```sh
ollama run mistral:latest
```

### ✅ Install & Configure Obsidian
1. Download Obsidian from [Obsidian.md](https://obsidian.md).
2. Set up your **Obsidian Vault** (your notes will be stored here).
3. Note the **absolute path** to your vault (e.g., `C:\Users\YourName\ObsidianVault`).
4. Update the `VAULT_PATH` in the `app.py` file to match your vault location.

---

# 🚀 Running the AI Second Brain
Once everything is installed and set up, follow these steps:

### 1️⃣ Start the Ollama AI Server
Ensure Ollama is running before launching the app:
```sh
ollama serve &
```

### 2️⃣ Run the Flask Application
Start the AI Second Brain server:
```sh
python app.py
```
You should see output like:
```
 * Running on http://localhost:5000/
```

---

# 🛠️ Usage Guide

## 📡 Querying the AI via API
You can send a query to your AI Second Brain using `curl` or Postman:
```sh
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my notes on AI research?", "model": "2"}'
```

Response example:
```json
{
  "response": "Your notes mention AI research in multiple contexts, including deep learning, reinforcement learning..."
}
```

## 🌐 Web Interface (Optional)
If you have a frontend UI, place `index.html` inside the `static/` folder, and access the web interface at:
```
http://localhost:5000/
```

## 🧠 Changing AI Models
You can switch between AI models using the API:
- **Mistral (default)**: Best for reasoning
- **Gemma**: More balanced, logical responses

Specify the model in your API request:
```sh
{"query": "Summarize my business ideas", "model": "1"}
```

---

# 🔄 Updating Notes
Your notes refresh **every 10 minutes** automatically. However, if you want to force a reload:
1. Restart the Flask app.
2. Run:
```sh
python app.py
```

---

# ⚠️ Troubleshooting

### ❌ Error: "Could not get a response from the AI"
✅ Ensure **Ollama is running** by executing:
```sh
ollama serve
```
✅ Restart Flask:
```sh
python app.py
```

### ❌ Error: "No notes found"
✅ Check if `VAULT_PATH` is correctly set in `app.py`.
✅ Ensure `.md` files exist in your Obsidian vault.

### ❌ Error: "500 Internal Server Error"
✅ Check for missing dependencies and install them:
```sh
pip install flask requests
```

---

# 🔥 Future Improvements
- **Add Web UI** for easier interactions.
- **Improve AI Context Awareness** using better prompt engineering.
- **Enable Note Editing** via API.

---

# 🤝 Credits
Developed by **Akkenapally Ruthwik Reddy** 🎯
