from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import base64
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/")
def home():
    return "Servidor rodando 🚀"


@app.route("/ping")
def ping():
    return {"ok": True}


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


@app.route("/simular", methods=["POST"])
def simular():
    try:
        if "file" not in request.files:
            return jsonify({"erro": "Arquivo não enviado"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

        nome_base = str(uuid.uuid4())
        caminho_original = os.path.join("static", f"{nome_base}.png")
        caminho_editado = os.path.join("static", f"edit_{nome_base}.png")

        file.save(caminho_original)

        prompt = """
        Edit this portrait photo to create a realistic dental smile simulation.
        Requirements:
        - preserve the same person and facial identity
        - enhance the smile in a natural and believable way
        - subtly whiten the teeth
        - slightly improve tooth alignment
        - close only small visible gaps if present
        - keep natural anatomy, lip shape, gingiva and proportions
        - avoid fake veneers, overexposed white teeth, or artificial plastic look
        - keep the result clinically plausible and premium
        - maintain realistic skin, lighting and facial details
        """

        with open(caminho_original, "rb") as img:
            response = client.images.edit(
                model="gpt-image-1",
                image=img,
                prompt=prompt,
                size="1024x1024",
                quality="medium",
                output_format="png"
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
