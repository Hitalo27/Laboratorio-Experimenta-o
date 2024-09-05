from typing import Counter
from Logger import *
import os
import datetime
import pytz
import requests
import csv
import time
import matplotlib.pyplot as plt

log = Logger()
nomeClasse = str(__name__).replace("_", '')
def lab01s01():
    log.criarLogPrint("Iniciando método lab01s01...", LogLevel.INFO, nomeClasse)

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("Token de autenticação não encontrado. Defina a variável de ambiente 'GITHUB_TOKEN'.")

    header = {'Authorization': f'bearer {token}'}
    query = """
    {
    search(query: "stars:>0", type: REPOSITORY, first: 100) {
        edges {
        node {
            ... on Repository {
            name
            stargazers {
                totalCount
            }
            forks {
                totalCount
            }
            issues(states: OPEN) {
                totalCount
            }
            createdAt
            updatedAt
            pushedAt
            releases {
                totalCount
            }
            pullRequests(states: MERGED) {
                totalCount
            }
            primaryLanguage {
                name
            }
            }
        }
        }
    }
    }
    """

    url = 'https://api.github.com/graphql'
    max_retries = 3
    for attempt in range(max_retries):
        resposta = requests.post(url, json={'query': query}, headers=header)
        if resposta.status_code == 200:
            log.criarLogPrint("Conexão com a API do GitHub bem-sucedida.", LogLevel.INFO, nomeClasse)
            dados = resposta.json()
            repositorios = dados['data']['search']['edges']
            log.criarLogPrint(f"Total de repositórios encontrados: {len(repositorios)}", LogLevel.INFO, nomeClasse)
            break
        else:
            log.criarLogPrint(f"Falha ao acessar a API: {resposta.status_code}", LogLevel.ERROR, nomeClasse)
            if attempt < max_retries - 1:
                log.criarLogPrint("Tentando novamente...", LogLevel.WARNING, nomeClasse)
                time.sleep(5)
            else:
                raise Exception(f"Classe: main - Falha ao acessar a API: {resposta.status_code}")

    with open('resultado.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
        nomes_campos = ['Nome', 'Estrelas', 'Forks', 'Issues Abertas', 'Criado em', 'Última Atualização', 'Último Push', 'Número de Releases', 'Total de Pull Requests Aceitas', 'Linguagem Primária']
        escritor = csv.DictWriter(arquivo_csv, fieldnames=nomes_campos)
        
        escritor.writeheader()
        log.criarLogPrint("Escrevendo dados no arquivo CSV...", LogLevel.INFO, nomeClasse)

        for repositorio in repositorios:
            nodo = repositorio['node']
            nome = nodo['name']
            estrelas = nodo['stargazers']['totalCount']
            forks = nodo['forks']['totalCount']
            issues_abertas = nodo['issues']['totalCount']
            criado_em = nodo['createdAt']
            ultima_atualizacao = nodo['updatedAt']
            ultimo_push = nodo['pushedAt']
            linguagem = nodo['primaryLanguage']['name'] if nodo['primaryLanguage'] else 'N/A'
            numero_releases = nodo['releases']['totalCount']
            numero_pull_requests = nodo['pullRequests']['totalCount']
            
            escritor.writerow({
                'Nome': nome,
                'Estrelas': estrelas,
                'Forks': forks,
                'Issues Abertas': issues_abertas,
                'Criado em': criado_em,
                'Última Atualização': ultima_atualizacao,
                'Último Push': ultimo_push,
                'Número de Releases': numero_releases,
                'Total de Pull Requests Aceitas': numero_pull_requests,
                'Linguagem Primária': linguagem
            })
        
        log.criarLogPrint("Dados escritos com sucesso no arquivo CSV 'resultado.csv'.", LogLevel.INFO, nomeClasse)
            

def lab01s02():
    log.criarLogPrint("Iniciando método lab01s02...", LogLevel.INFO, nomeClasse)

    token = ''
    headers = {'Authorization': f'token {token}'}
    per_page = 100
    num_repos = 1000
    repos = []
    cont = 0

    for page in range(1, (num_repos // per_page) + 2):
        url = f'https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page={per_page}&page={page}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            repos += response.json().get('items', [])
        else:
            print(f"Falha ao acessar a API: {response.status_code}")
            break

    csv_path = 'resultado.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nome', 'Estrelas', 'Forks', 'Issues Abertas', 'Criado em', 'Última Atualização', 'Último Push', 'Número de Releases', 'Total de Pull Requests Aceitas', 'Razão de Issues Fechadas', 'Linguagem Primária']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for repo in repos:
            name = repo['name']
            stars = repo['stargazers_count']
            forks = repo['forks_count']
            open_issues = repo['open_issues_count']
            created_at = repo['created_at']
            updated_at = repo['updated_at']
            pushed_at = repo['pushed_at']
            language = repo['language']

            pulls_url = repo['pulls_url'].replace('{/number}', '?state=all')
            pulls_response = requests.get(pulls_url, headers=headers)
            if pulls_response.status_code == 200:
                pulls_data = pulls_response.json()
                num_pulls = len([pull for pull in pulls_data if pull['state'] == 'closed'])
            else:
                num_pulls = 0

            releases_url = repo['releases_url'].replace('{/id}', '')
            releases_response = requests.get(releases_url, headers=headers)
            num_releases = len(releases_response.json()) if releases_response.status_code == 200 else 0

            issues_url = repo['issues_url'].replace('{/number}', '?state=all')
            issues_response = requests.get(issues_url, headers=headers)
            if issues_response.status_code == 200:
                issues_data = issues_response.json()
                closed_issues = len([issue for issue in issues_data if issue['state'] == 'closed'])
                total_issues = len(issues_data)
                issue_ratio = closed_issues / total_issues if total_issues > 0 else 0
            else:
                closed_issues = 0
                total_issues = 0
                issue_ratio = 0

            writer.writerow({
                'Nome': name,
                'Estrelas': stars,
                'Forks': forks,
                'Issues Abertas': open_issues,
                'Criado em': created_at,
                'Última Atualização': updated_at,
                'Último Push': pushed_at,
                'Número de Releases': num_releases,
                'Total de Pull Requests Aceitas': num_pulls,
                'Razão de Issues Fechadas': issue_ratio,
                'Linguagem Primária': language
            })
            cont += 1
            print(cont)

    log.criarLogPrint("Dados escritos com sucesso no arquivo CSV 'resultado.csv'.", LogLevel.INFO, nomeClasse)


    nomes_repos = [repo['name'] for repo in repos]
    estrelas = [repo['stargazers_count'] for repo in repos]
    forks = [repo['forks_count'] for repo in repos]
    linguagens = [repo['language'] for repo in repos]
    releases = [repo['releases_url'].replace('{/id}', '') for repo in repos]


    plt.figure(figsize=(10, 6))
    plt.barh(nomes_repos[:10], estrelas[:10], color='skyblue')
    plt.xlabel('Número de Estrelas')
    plt.ylabel('Repositórios')
    plt.title('Top 10 Repositórios com Mais Estrelas')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('top_10_repos_estrelas.png')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.scatter(estrelas, forks, alpha=0.5, color='orange')
    plt.xlabel('Número de Estrelas')
    plt.ylabel('Número de Forks')
    plt.title('Relação entre Estrelas e Forks dos Repositórios')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('estrelas_vs_forks.png')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    linguagens_count = Counter(linguagens)
    plt.pie(linguagens_count.values(), labels=linguagens_count.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Distribuição das Linguagens de Programação')
    plt.savefig('distribuicao_linguagens.png')
    plt.show()

    num_releases = []
    for repo in repos:
        releases_url = repo['releases_url'].replace('{/id}', '')
        releases_response = requests.get(releases_url, headers=headers)
        num_releases.append(len(releases_response.json()) if releases_response.status_code == 200 else 0)

    plt.figure(figsize=(10, 6))
    plt.barh(nomes_repos[:10], num_releases[:10], color='salmon')
    plt.xlabel('Número de Releases')
    plt.ylabel('Repositórios')
    plt.title('Top 10 Repositórios com Mais Releases')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('top_10_repos_releases.png')
    plt.show()

    log.criarLogPrint("Gráficos gerados com sucesso.", LogLevel.INFO, nomeClasse)

if __name__ == "__main__":

    data_atual = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    data_atual_str = data_atual.strftime('%d_%m_%Y')

    dir_loggin = os.path.join(os.getcwd(), 'LES-Lab06/Laboratorio01/dados_logging')
    if not os.path.exists(dir_loggin):
        os.makedirs(dir_loggin)

    dir_loggin = os.path.join(dir_loggin, f'Execution_{data_atual_str}.log')

    dir_loggin = dir_loggin.replace('\\', '/')

    logging.basicConfig(
        filename=dir_loggin,
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO,
        filemode='a'
    )

    while True:
        
        print("\n\n--------------------------------------")
        print("Menu de Debug:")
        print("1 - Lab01s01")
        print("2 - Lab01s02")
        print("3 - Executar todas as opções")
        print("0 - Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            break
        elif escolha == '1':

            log.criarLogPrint("Opcão 1 iniciada.", LogLevel.INFO, nomeClasse)
            lab01s01()
            log.criarLogPrint("Opcão 1 finalizada.", LogLevel.INFO, nomeClasse)
        elif escolha == '2':
            log.criarLogPrint("Opcão 2 iniciada.", LogLevel.INFO, nomeClasse)
            lab01s02()
            log.criarLogPrint("Opcão 2 finalizada.", LogLevel.INFO, nomeClasse)

        elif escolha == '3':
            log.criarLogPrint("Executando todas as opções", LogLevel.INFO, nomeClasse)

            log.criarLogPrint("Opcão 1 iniciada.", LogLevel.INFO, nomeClasse)
            lab01s01()
            log.criarLogPrint("Opcão 1 finalizada.", LogLevel.INFO, nomeClasse)

            log.criarLogPrint("Opcão 2 iniciada.", LogLevel.INFO, nomeClasse)
            lab01s02()
            log.criarLogPrint("Opcão 2 finalizada.", LogLevel.INFO, nomeClasse)

        else:
            log.criarLogPrint("Opção inválida. Tente novamente.", LogLevel.INFO, nomeClasse)