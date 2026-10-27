from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Carrega as informações do arquivo .env
load_dotenv()

app = Flask(__name__)

# Dados do recurso Azure
AZURE_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_REGION = os.getenv("AZURE_TRANSLATOR_REGION")


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/traduzir", methods=["POST"])
def traduzir():
    try:
        dados = request.get_json()

        texto = dados.get("texto", "").strip()
        idioma_destino = dados.get("idioma_destino", "en")

        if not texto:
            return jsonify({"erro": "Digite um texto para traduzir."}), 400

        if not AZURE_KEY or not AZURE_ENDPOINT or not AZURE_REGION:
            return jsonify({
                "erro": "As configurações do Azure não foram preenchidas."
            }), 500

        url = AZURE_ENDPOINT.rstrip("/") + "/translate"

        parametros = {
            "api-version": "3.0",
            "to": idioma_destino
        }

        cabecalhos = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY,
            "Ocp-Apim-Subscription-Region": AZURE_REGION,
            "Content-Type": "application/json"
        }

        corpo = [{"Text": texto}]

        resposta = requests.post(
            url,
            params=parametros,
            headers=cabecalhos,
            json=corpo,
            timeout=30
        )

        resposta.raise_for_status()

        resultado = resposta.json()
        traducao = resultado[0]["translations"][0]["text"]

        return jsonify({
            "traducao": traducao
        })

    except requests.exceptions.HTTPError:
        return jsonify({
            "erro": "O Azure não conseguiu realizar a tradução. Verifique as configurações do recurso."
        }), 502

    except requests.exceptions.RequestException:
        return jsonify({
            "erro": "Não foi possível conectar ao serviço Azure."
        }), 502

    except Exception:
        return jsonify({
            "erro": "Ocorreu um erro inesperado no servidor."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)