from flask import Flask, request, jsonify, send_from_directory
import os
import logging
from logging.handlers import RotatingFileHandler
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['PASTA_UPLOAD'] = './uploads'
app.config['EXTENSOES_PERMITIDAS'] = {'pdf'}
app.config['PASTA_LOGS'] = './logs'
app.config['TOKEN_SERVICO'] = 'SIMULANDO_TOKEN'

if not os.path.exists(app.config['PASTA_LOGS']):
    os.makedirs(app.config['PASTA_LOGS'])

log_handler = RotatingFileHandler(os.path.join(app.config['PASTA_LOGS'], 'app.log'), maxBytes=10000, backupCount=1)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

def arquivo_permitido(nome_arquivo):
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in app.config['EXTENSOES_PERMITIDAS']

def pdf_para_texto(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ''
        return texto
    except Exception as e:
        return f"Erro: {str(e)}"

def registra_log(mensagem):
    app.logger.info(mensagem)

@app.route('/converte-pdf-para-txt', methods=['POST'])
def converte_pdf_para_txt():
    if 'file' not in request.files:
        registra_log('Nenhum arquivo foi enviado')
        return jsonify({'erro': 'Nenhum arquivo foi enviado'}), 400

    arquivo = request.files['file']
    if arquivo.filename == '':
        registra_log('Nenhum arquivo foi selecionado')
        return jsonify({'erro': 'Nenhum arquivo foi selecionado'}), 400

    if arquivo and arquivo_permitido(arquivo.filename):
        nome_arquivo = secure_filename(arquivo.filename)
        caminho_pdf = os.path.join(app.config['PASTA_UPLOAD'], nome_arquivo)
        os.makedirs(app.config['PASTA_UPLOAD'], exist_ok=True)
        arquivo.save(caminho_pdf)

        texto = pdf_para_texto(caminho_pdf)
        if texto.startswith("Erro"):
            registra_log(f'Erro na conversão do arquivo {nome_arquivo}: {texto}')
            return jsonify({'erro': texto}), 500

        nome_txt = nome_arquivo.rsplit('.', 1)[0] + '.txt'
        caminho_txt = os.path.join(app.config['PASTA_UPLOAD'], nome_txt)
        with open(caminho_txt, 'w', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write(texto)

        registra_log(f'Conversão concluída para o arquivo {nome_arquivo}, salvo como {nome_txt}')
        return jsonify({
            'mensagem': 'Conversão concluída',
            'arquivo_txt': nome_txt,
            'link_download': f'/download/{nome_txt}'
        }), 201
    else:
        registra_log(f'Arquivo não permitido: {arquivo.filename}')
        return jsonify({'erro': 'Arquivo não permitido'}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_arquivo(filename):
    return send_from_directory(app.config['PASTA_UPLOAD'], filename)

def decode_text(input_text):
    try:
        return input_text.decode('utf-8')
    except UnicodeDecodeError as e:
        app.logger.error(f"Erro ao decodificar: {e}")
        return input_text.decode('utf-8', errors='ignore')

@app.route('/emite-relatorio', methods=['POST'])
def emite_relatorio():
    token = request.headers.get('Authorization')
    if token != app.config['TOKEN_SERVICO']:
        registra_log('Acesso não autorizado ao serviço de log')
        return jsonify({'erro': 'Acesso não autorizado'}), 403
    try:
        with open(os.path.join(app.config['PASTA_LOGS'], 'app.log'), 'rb') as log_file:  # Note o modo 'rb'
            log_content = log_file.read()
        decoded_log_content = decode_text(log_content)
        return jsonify({'relatorio': decoded_log_content}), 200
    except Exception as e:
        app.logger.error(f'Erro ao emitir relatório: {str(e)}')
        return jsonify({'erro': 'Erro ao emitir relatório'}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
