import requests
import json
import os

API_KEY = os.getenv('API_KEY')
API_COOKIE = os.getenv('API_COOKIE')
# Dicionário com os códigos dos órgãos superiores
ORGAOS_SUPERIORES = {
    "Presidência da República": 20000,
    "Ministério das Relações Exteriores": 35000,
    "Ministério da Saúde": 36000,
    "Ministério da Justiça e Segurança Pública": 30000,
    "Ministério do Trabalho e Emprego": 40000,
    "Ministério da Educação": 30050,
    "Ministério da Ciência, Tecnologia e Inovação": 41500,
    "Ministério da Agricultura e Pecuária": 22000,
    "Ministério das Relações Exteriores": 20050,
    "Ministério do Trabalho e Emprego": 49100,
    "Ministério do Meio Ambiente": 50000,
    "Ministério do Turismo": 57000,
    "Ministério do Esporte": 51000,
    "Ministério da Defesa": 52000,
    "Ministério da Mulher, da Família e dos Direitos Humanos": 59000,
    "Ministério do Turismo": 54000,
    "Ministério da Cultura": 51050,
    "Ministério da Fazenda": 23000,
    "Ministério da Casa Civil": 15000,
    "Ministério da Integração e do Desenvolvimento Regional": 53000,
    "Ministério das Comunicações": 60000,
    "Ministério da Segurança Pública": 29000,
    "Ministério da Saúde (SUS)": 36001,
}

# Função para buscar os dados da API do Portal da Transparência
def fetch_data(pagina, orgao_superior):
    url = f"https://api.portaldatransparencia.gov.br/api-de-dados/despesas/por-orgao?ano=2024&orgaoSuperior={orgao_superior}&pagina={pagina}"
    
    # Definindo o cabeçalho com a chave da API e o cookie
    headers = {
        'chave-api-dados': API_KEY,  # Usando a chave de API obtida da variável de ambiente
        'Cookie': API_COOKIE  # Usando o cookie obtido da variável de ambiente
    }
    
    try:
        # Fazendo a requisição GET à API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se o código de status é 2xx

        # Retorna os dados da resposta como JSON
        return response.json()
    
    except requests.RequestException:
        print(f"Erro ao acessar a API para a página {pagina}.")
        return None

# Função principal que chama a API para diferentes órgãos e páginas
def fetch_and_save_data():
    # Cria a pasta 'despesas_json' caso não exista
    if not os.path.exists('despesas_json'):
        os.makedirs('despesas_json')
    for orgao, codigo in ORGAOS_SUPERIORES.items():
        print(f"Buscando dados para o órgão: {orgao} (Código: {codigo})")
        
        pagina = 1  # Começa pela primeira página
        
        while True:
            print(f"Buscando dados da página {pagina}...")
            data = fetch_data(pagina, codigo)
            
            # Se os dados estiverem vazios ou nulos, significa que a página está em branco
            if not data:
                print(f"Página {pagina} está em branco. Finalizando a busca para o órgão {orgao}.")
                break  # Interrompe a busca quando a página está vazia
            
            # Salva os dados em um arquivo, nomeado de acordo com o órgão e a página
            output_file = os.path.join('despesas_json', f"despesas_{codigo}_{orgao.replace(' ', '_')}_pagina_{pagina}.json")
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Dados salvos com sucesso em {output_file}")
            
            # Avança para a próxima página
            pagina += 1

if __name__ == "__main__":
    fetch_and_save_data()
