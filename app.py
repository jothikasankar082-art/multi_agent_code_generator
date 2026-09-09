# app.py — Flask Backend
# Run: python app.py
# Then open: http://localhost:5000

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from groq import Groq

from agents.planning_agent import PlanningAgent
from agents.designing_agent import DesigningAgent
from agents.creating_agent import CreatingAgent
from agents.testing_agent import TestingAgent

load_dotenv()
app = Flask(__name__, static_folder='.')
CORS(app)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file!")

client = Groq(api_key=api_key)

# ── These are the models on YOUR specific account that support text/code ──
# Ordered best to worst for coding tasks
YOUR_WORKING_MODELS = [
    "openai/gpt-oss-120b",   # Best — largest
    "openai/gpt-oss-20b",    # Good — faster
    "qwen/qwen3.8-27b",      # Qwen is good at coding
    "qwen/qwen3.6-27b",      # Qwen fallback
    "groq/compound",         # Groq compound
    "groq/compound-mini",    # Groq compound mini
]

# ── Models to always skip (wrong type or need terms) ──
SKIP_MODELS = [
    "canopylabs/orpheus-arabic-saudi",  # needs terms + arabic TTS
    "canopylabs/orpheus-v1-english",    # TTS model, not text gen
    "whisper-large-v3",                 # speech-to-text, not code
    "whisper-large-v3-turbo",           # speech-to-text, not code
    "meta-llama/llama-prompt-guard-2-22m",  # safety classifier
    "meta-llama/llama-prompt-guard-2-86m",  # safety classifier
    "openai/gpt-oss-safeguard-20b",    # safety model
    "allam-2-7b",                       # Arabic language model
]

def find_working_model():
    try:
        available = client.models.list()
        available_ids = [m.id for m in available.data]

        print("\n📋 Your account models:")
        for m in available_ids:
            status = "⛔ skip" if m in SKIP_MODELS else "✅ ok"
            print(f"   {status}  {m}")

        # Try preferred models first
        for model in YOUR_WORKING_MODELS:
            if model in available_ids:
                print(f"\n🚀 Selected: {model}\n")
                return model

        # Fallback: any model not in skip list
        for m in available_ids:
            if m not in SKIP_MODELS:
                print(f"\n🚀 Fallback model: {m}\n")
                return m

    except Exception as e:
        print(f"⚠️  Could not list models: {e}")

    return "openai/gpt-oss-20b"

model = find_working_model()

planning_agent  = PlanningAgent(client, model)
designing_agent = DesigningAgent(client, model)
creating_agent  = CreatingAgent(client, model)
testing_agent   = TestingAgent(client, model)

print(f"✅ Using model : {model}")
print("✅ All 4 agents ready")
print("✅ Open http://localhost:5000 in your browser\n")


@app.route('/ping')
def ping():
    return jsonify({'status': 'ok', 'model': model})


@app.route('/')
def index():
    return send_from_directory('.', 'ui.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Could not read request'}), 400

    user_request = data.get('request', '').strip()
    language     = data.get('language', 'python')

    print(f"\n📥 Request: '{user_request}' | Language: {language}")

    if not user_request:
        return jsonify({'error': 'No request provided'}), 400

    full_request = f"{user_request} (write in {language})"

    try:
        print("🔍 Step 1: Planning...")
        plan = planning_agent.run(full_request)

        print("📐 Step 2: Designing...")
        design = designing_agent.run(full_request, plan)

        print("💻 Step 3: Creating...")
        code = creating_agent.run(full_request, plan, design)

        print("🧪 Step 4: Testing...")
        tests = testing_agent.run(full_request, code)

        print("✅ All done!\n")
        return jsonify({'plan': plan, 'design': design,
                        'code': code, 'tests': tests})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))