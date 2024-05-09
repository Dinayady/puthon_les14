import requests

url = 'https://api.github.com/users/Dinayady'
req = requests.get(url)
response_dict = req.json()
print(response_dict.keys())

repos = response_dict['public_repos']
repos_url = response_dict['repos_url']
print('Quantity repos: ', repos)

repos_req = requests.get(repos_url)
res_dict_repos = repos_req.json()
print(res_dict_repos[0])