import requests
import json
import re
from collections import defaultdict
import os

# Caminho para o diretório onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definir a URL base
base_url = "https://api.portaldatransparencia.gov.br/api-de-dados/renuncias-valor?codigoIbge=5300108&pagina="

# Definir os cabeçalhos da requisição
headers = {
    'chave-api-dados': 'e6152c1558b273b4666d27d60ed32f3f',
    'Cookie': 'JSESSIONID=B9B5592239B9C1517C3A914D65C374F8'
}

# Função para buscar e imprimir os dados de uma página específica
def get_data(page):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Supondo que a resposta seja um JSON
    else:
        print(f"Erro ao acessar a página {page}: {response.status_code}")
        return None

# Função para sanitizar o nome do arquivo
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

# Função para ler o número da última página processada (do arquivo de controle)
def get_last_page():
    page_file_path = os.path.join(script_dir, 'pagina_atual.txt')  # Caminho absoluto para o arquivo de controle
    if os.path.exists(page_file_path):
        with open(page_file_path, 'r') as f:
            return int(f.read().strip())
    return 1  # Se não encontrar o arquivo, começa da página 1 (ou última válida que você determinar)

# Função para atualizar o arquivo com a última página processada
def update_last_page(page):
    page_file_path = os.path.join(script_dir, 'pagina_atual.txt')  # Caminho absoluto para o arquivo de controle
    with open(page_file_path, 'w') as f:
        f.write(str(page))

# Função para carregar os dados já existentes no arquivo JSON
def load_existing_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []  # Retorna uma lista vazia se o arquivo não existir

# Função para verificar se um item já existe no arquivo (usando todos os campos)
def is_duplicate(existing_data, new_item):
    # Verifica se algum item existente é exatamente igual ao novo item
    return any(
        item == new_item for item in existing_data
    )

# Garantir que a pasta json exista dentro da pasta do script
json_dir = os.path.join(script_dir, 'json')
os.makedirs(json_dir, exist_ok=True)

# Iniciar a captura de dados a partir da última página registrada
page = get_last_page()

while True:
    data = get_data(page)
    
    if data:  # Se dados foram encontrados
        for item in data:
            descricao_beneficio = item.get('descricaoBeneficioFiscal')
            if descricao_beneficio:
                # Filtra os dados por 'descricaoBeneficioFiscal'
                sanitized_type = sanitize_filename(descricao_beneficio)
                file_name = os.path.join(json_dir, f"dados_{sanitized_type}.json")  # Caminho correto para o arquivo JSON

                # Carregar os dados existentes
                existing_data = load_existing_data(file_name)

                # Se o item não for duplicado, adiciona
                if not is_duplicate(existing_data, item):
                    existing_data.append(item)
                    print(f"Adicionando item à página '{descricao_beneficio}'.")
                    
                    # Salvar os dados no arquivo JSON
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=4)
                else:
                    print(f"Item já existente. Ignorando duplicação.")

        print(f"Página {page} capturada com sucesso.")
        
        # Atualizar a página para a próxima e salvar a última página com dados
        update_last_page(page)  # Salvar a última página lida com dados
        page += 1
        
    else:
        # Se a página estiver vazia ou erro de requisição
        print(f"Página {page} vazia ou não encontrada. Terminando a captura.")
        
        # Parar imediatamente quando a página estiver vazia
        break

print("Processo finalizado.")
