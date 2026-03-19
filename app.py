from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance
import uuid
import os

app = Flask(__name__)
CORS(app)

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

        nome_arquivo = f"{uuid.uuid4()}.jpg"
        caminho_original = os.path.join("static", nome_arquivo)
        caminho_editado = os.path.join("static", f"edit_{nome_arquivo}")

        file.save(caminho_original)

        with Image.open(caminho_original) as img:
            img = img.convert("RGB")

            brilho = ImageEnhance.Brightness(img).enhance(1.08)
            contraste = ImageEnhance.Contrast(brilho).enhance(1.12)
            cor = ImageEnhance.Color(contraste).enhance(0.95)

            cor.save(caminho_editado, quality=90)

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
