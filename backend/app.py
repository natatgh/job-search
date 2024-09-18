from flask import Flask, request, jsonify
from flask_cors import CORS
from scraping import buscar_vagas

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    linguagens = data.get('linguagens', [])  # Agora trata múltiplas linguagens
    modalidade = data.get('modalidade', '')  # Default para '' caso não seja preenchido
    contrato = data.get('contrato', '')  # Default para '' caso não seja preenchido

    # Função de scraping ou lógica que recebe os filtros adicionais
    vagas = buscar_vagas(linguagens, modalidade, contrato)

    return jsonify(vagas)

if __name__ == '__main__':
    app.run(debug=True)
