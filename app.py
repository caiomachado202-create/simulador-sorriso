from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import uuid
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("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"))

if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/simular", methods=["POST"])
def simular_sorriso():

    data = request.json

    imagem_base64 = data.get("imagem")

    imagem_bytes = base64.b64decode(imagem_base64)

    nome_arquivo = f"{uuid.uuid4()}.png"

    caminho_original = f"static/{nome_arquivo}"

    with open(caminho_original, "wb") as f:
        f.write(imagem_bytes)

    prompt = """
    Improve this person's smile naturally:
    - Slight whitening
    - Keep natural look
    """

    with open(caminho_original, "rb") as img:
        response = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=prompt
        )

    imagem_editada_base64 = response.data[0].b64_json
    imagem_editada_bytes = base64.b64decode(imagem_editada_base64)

    caminho_editado = f"static/edit_{nome_arquivo}"

    with open(caminho_editado, "wb") as f:
        f.write(imagem_editada_bytes)

request_url = request.host_url

return jsonify({
    "antes": f"{request_url}{caminho_original}",
    "depois": f"{request_url}{caminho_editado}"
})
    
@app.route("/ping")
def ping():
    return {"ok": True}

@app.route("/")
def home():
    return "Servidor rodando 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
