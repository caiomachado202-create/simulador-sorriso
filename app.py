from flask import Flask, request, jsonify
import base64
import uuid
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="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")

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

    return jsonify({
        "antes": f"http://localhost:5000/{caminho_original}",
        "depois": f"http://localhost:5000/{caminho_editado}"
    })
@app.route("/")
def home():
    return "Servidor rodando 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
