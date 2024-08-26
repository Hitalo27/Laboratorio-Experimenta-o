from Logger import *
import os
import datetime
import pytz
import requests
import csv
import time
from dotenv import load_dotenv

log = Logger()
nomeClasse = str(__name__).replace("_", '')
load_dotenv()

def lab01s01():
    log.criarLogPrint("Iniciando método lab01s01...", LogLevel.INFO, nomeClasse)

    # Digite seu token do GitHub no arquivo .env
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
                time.sleep(5)  # Espera 5 segundos antes de tentar novamente
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

    # Digite seu token do GitHub no arquivo .env
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
    resposta = requests.post(url, json={'query': query}, headers=header)

    if resposta.status_code == 200:
        log.criarLogPrint("Conexão com a API do GitHub bem-sucedida.", LogLevel.INFO, nomeClasse)
        dados = resposta.json()
        repositorios = dados['data']['search']['edges']
        log.criarLogPrint(f"Total de repositórios encontrados: {len(repositorios)}", LogLevel.INFO, nomeClasse)
    else:
        log.criarLogPrint(f"Falha ao acessar a API: {resposta.status_code}", LogLevel.ERROR, nomeClasse)
        repositorios = []

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