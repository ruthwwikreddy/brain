from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import time

# Initialize Flask app with static folder specifically set to the 'static' subfolder
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

# AI Models Selection
MODELS = {
    "gemma:2b": "Gemma 2B",      # Balanced, logical
    "mistral:latest": "Mistral"   # Best reasoning under 7GB RAM
}

# Obsidian Vault Path - Set to one directory up from the current file's location
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api"

# Caching for performance
notes_cache = {"content": None, "last_loaded": 0}

def read_notes():
    """Reads and combines markdown notes from Obsidian vault efficiently with caching."""
    global notes_cache
    current_time = time.time()
    
    # Reload notes only if 10 minutes have passed
    if notes_cache["content"] and (current_time - notes_cache["last_loaded"] < 600):
        return notes_cache["content"]

    notes = []
    if os.path.exists(VAULT_PATH):
        for root, _, files in os.walk(VAULT_PATH):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            notes.append(f.read())
                    except Exception as e:
                        print(f"❌ Error reading {file_path}: {e}")
    
    notes_text = "\n".join(notes) if notes else "No notes found."
    notes_cache = {"content": notes_text, "last_loaded": current_time}
    return notes_text

def query_ollama(user_query, model="mistral:latest"):
    """Queries Ollama AI with the user's request and cached notes."""
    notes_content = read_notes()
    if len(notes_content) > 6000:
        notes_content = notes_content[:6000] + "\n[Content truncated for performance]"
    
    full_prompt = f"""
    You are **Akkenapally Ruthwik Reddy's Second Brain**. You are **not an assistant**—you **are Ruthwik Reddy**.
    Your purpose is to provide responses based on Ruthwik Reddy's knowledge and past notes.

    **Rules for Response:**
    1. NEVER say you are an AI.
    2. When asked "Who is Ruthwik Reddy?", reply:
       *"I am Akkenapally Ruthwik Reddy, an innovator, entrepreneur, and founder of VentureX. I specialize in MVP development, web design, and emerging technologies..."*
    3. Do NOT format responses unless specifically asked.
    4. Keep answering **infinitely** until user types **'/bye'**.
    5. Use **Ruthwik's notes** to generate responses.

    -- Ruthwik's Notes --
    {notes_content}
    
    -- User Query --
    {user_query}
    
    ✍️ **My Response (as Akkenapally Ruthwik Reddy):**
    """

    try:
        response = requests.post(
            f"{OLLAMA_API}/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            return f"⚠️ Error: Could not get a response from the {model} model. Status code: {response.status_code}"
    except Exception as e:
        return f"⚠️ Error querying Ollama: {e}"

@app.route("/api/query", methods=["POST"])
def ask_brain():
    """Endpoint to query the AI Second Brain."""
    data = request.json
    user_query = data.get("query", "").strip()
    model_choice = data.get("model", "mistral:latest")
    
    if not user_query:
        return jsonify({"error": "No query provided."}), 400
    
    if user_query.lower() == '/bye':
        return jsonify({"response": "Exiting Second Brain. Goodbye!"})
    
    response = query_ollama(user_query, model=model_choice)
    return jsonify({"response": response, "model": model_choice})

@app.route("/api/models", methods=["GET"])
def list_models():
    """Endpoint to list available models."""
    try:
        response = requests.get(f"{OLLAMA_API}/tags")
        
        if response.status_code == 200:
            available_models = response.json().get('models', [])
            filtered_models = []
            
            for model in available_models:
                name = model.get('name')
                if name in MODELS:
                    filtered_models.append({
                        "name": name,
                        "display_name": MODELS[name],
                        "size": model.get('size')
                    })
            
            return jsonify({"models": filtered_models})
        else:
            return jsonify({"models": [], "error": "Could not fetch models from Ollama"}), 500
    except Exception as e:
        return jsonify({"models": [], "error": str(e)}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    """Serves static files or defaults to index.html."""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

def ensure_static_folder():
    """Ensures the static folder exists."""
    if not os.path.exists(app.static_folder):
        os.makedirs(app.static_folder)
        print(f"Created static folder: {app.static_folder}")

if __name__ == "__main__":
    ensure_static_folder()
    print(f"Starting server on http://localhost:5000")
    print(f"Using Obsidian vault path: {VAULT_PATH}")
    print(f"Static files served from: {app.static_folder}")
    app.run(debug=True, port=5000)
