import requests
import csv

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


with open('C:/Users/Assemp/Desktop/resultado.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        cont = cont + 1
        print(cont)

print("Dados salvos em resultado.csv")