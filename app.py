from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import uuid
import os
import base64
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/teste")
def teste():
    return '''
    <h2>Teste Simulador de Sorriso</h2>
    <form action="/simular" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <br><br>
        <button type="submit">Enviar</button>
    </form>
    '''


@app.route("/")
def home():
    return "Servidor rodando 🚀"


@app.route("/ping")
def ping():
    return {"ok": True}


@app.route("/simular", methods=["POST"])
def simular():
    try:
        if "file" not in request.files:
            return jsonify({"erro": "Arquivo não enviado"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

        nome_base = str(uuid.uuid4())
        caminho_original = os.path.join("static", f"{nome_base}.jpg")
        caminho_editado = os.path.join("static", f"edit_{nome_base}.png")

        file.save(caminho_original)

        # Reduz a imagem antes de enviar para ficar mais rápido e mais estável
        with Image.open(caminho_original) as img:
            img = img.convert("RGB")
            img.thumbnail((700, 700))
            img.save(caminho_original, format="JPEG", quality=88)

        prompt = """
        Create a realistic dental smile refinement for this photo.

        Rules:
        - keep the exact same person
        - preserve the same face, lips, skin, facial expression and head position
        - edit only the visible teeth and smile area
        - subtly whiten the teeth
        - slightly improve visible tooth alignment
        - close only very small gaps if present
        - keep the result conservative, elegant and clinically believable
        - do not change the lips
        - do not change the face shape
        - do not make the person smile more
        - do not create fake veneers
        - do not make teeth overly white
        - do not make teeth too large
        - avoid any artificial AI look
        - premium, natural and minimal result
        """

        with open(caminho_original, "rb") as img_file:
            response = client.images.edit(
                model="gpt-image-1",
                image=img_file,
                prompt=prompt,
                size="512x512",
                quality="medium"
            )

        imagem_editada_b64 = response.data[0].b64_json
        imagem_editada_bytes = base64.b64decode(imagem_editada_b64)

        with open(caminho_editado, "wb") as f:
            f.write(imagem_editada_bytes)

        base_url = request.host_url

        return jsonify({
            "antes": f"{base_url}{caminho_original}",
            "depois": f"{base_url}{caminho_editado}",
            "mensagem": "Simulação pronta"
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
