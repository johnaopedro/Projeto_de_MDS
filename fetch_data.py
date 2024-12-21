import requests
import json

# URLs dos diferentes endpoints
ENDPOINTS = [
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/users"
]

# Nome do arquivo para salvar os dados
OUTPUT_FILES = ["posts.json", "comments.json", "users.json"]

def fetch_and_save_data():
    for endpoint, output_file in zip(ENDPOINTS, OUTPUT_FILES):
        try:
            # Faz a requisição GET à API
            response = requests.get(endpoint)
            response.raise_for_status()  # Gera uma exceção para códigos de status 4xx/5xx

            # Obtém os dados da resposta em JSON
            data = response.json()

            # Salva os dados no arquivo correspondente
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Dados salvos com sucesso em {output_file}")

        except requests.RequestException as e:
            print(f"Erro ao acessar a API em {endpoint}: {e}")
        except Exception as e:
            print(f"Erro ao processar os dados de {endpoint}: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
