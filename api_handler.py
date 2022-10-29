
from data import *
import requests

api_key = encoded_api
headers = {'Authorization':'Basic {}'.format(api_key)}
base_url = f'https://api.octopus.energy/v1/'
account = f'accounts/{account_number}'
electricity_path = f'electricity-meter-points/{mpan}/meters/{elec_meter}/consumption'
gas_path = f'gas-meter-points/{gpan}/meters/{gas_meter}/consumption'


def __get_data(url):
    response = requests.get(url, headers=headers, timeout=5).json()
    response_blocks = []
    response_blocks.append(response['results'])
    while response['next']:
        url = response['next']
        response = requests.get(url, headers=headers, timeout=5).json()
        response_blocks.append(response['results'])
    return response_blocks

def get_data(type, dates=None):
    if type == 'electricity':
        return __get_electricity_consumption(dates)
    elif type == 'gas':
        return __get_gas_consumption(dates)


def __get_electricity_consumption(days=None):
    url = base_url+electricity_path+'/'+days if days else base_url+electricity_path
    return __get_data(url)

def __get_gas_consumption(days=None):
    url =base_url+gas_path+'/'+days if days else base_url+gas_path
    return __get_data(url)
'''    



response = requests.get(base_url+account, headers=headers, timeout=5)

content = response.json()
elec = content['properties']
for k in elec:
    print(k)
print(content)

response = requests.get(base_url+electricity, headers = headers, timeout=5)
content = response.json()
print(content)
while 'next' in content:
    next_page = content['next']
    response = requests.get(next_page, headers = headers, timeout=5)
    content = response.json()
    print(content)'''
