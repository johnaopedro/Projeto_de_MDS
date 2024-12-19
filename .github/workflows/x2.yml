import requests
import json

# URL da API (insira aqui quando disponível)
API_URL = "https://jsonplaceholder.typicode.com/posts"  # Exemplo de URL de API pública

# Nome do arquivo para salvar os dados
OUTPUT_FILE = "data.json"

def fetch_and_save_data():
    try:
        # Faz a requisição GET à API
        response = requests.get(API_URL)
        response.raise_for_status()  # Gera uma exceção para códigos de status 4xx/5xx

        # Obtém os dados da resposta em JSON
        data = response.json()

        # Salva os dados no arquivo data.json
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Dados salvos com sucesso em {OUTPUT_FILE}")

    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
