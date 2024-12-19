import requests
import json

# Exemplo simples de chamada de API
try:
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    response.raise_for_status()  # Levanta uma exceção para erros HTTP (status 4xx/5xx)

    # Converte os dados da resposta para JSON
    data = response.json()

    # Salva os dados em um arquivo 'data.json'
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Dados salvos com sucesso em 'data.json'")

except requests.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
except Exception as e:
    print(f"Erro ao processar os dados: {e}")
