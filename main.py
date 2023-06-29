from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app, methods=['DELETE', 'POST', 'PUT', 'GET', 'OPTIONS'])

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "statistika"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

services = {}

@app.route('/zadnji-klic', methods=['GET'])
def zadnje_klican_endpoint():
    if len(services) == 0:
        return "No endpoints called yet."
    last_called_endpoint = max(services.keys())
    return f"Zadnje klican endpoint: {last_called_endpoint}"

@app.route('/najpogostejsi-klic', methods=['GET'])
def najpogosteje_klicana_storitev():
    if len(services) == 0:
        return "No services called yet."
    most_called_service = max(services, key=services.get)
    return f"Najpogosteje klicana storitev: {most_called_service}"

@app.route('/vsi-klici', methods=['GET'])
def stevilo_posameznih_klicev():
    return jsonify(services)

@app.route('/posodobi', methods=['POST'])
def posodobi_podatke():
    if not request.json or 'klicanaStoritev' not in request.json:
        return jsonify({'error': 'Invalid request body'}), 400

    service = request.json['klicanaStoritev']
    services[service] = services.get(service, 0) + 1

    return jsonify({'message': 'Data updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5050)
