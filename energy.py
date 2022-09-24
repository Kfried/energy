import pycurl

user = 'sk_live_6DD1PEhGrtL8kd9cHrBjGoCf'

headers = []
b64cred = base64.b64encode("{}:{}".format(user))
headers.append("Authorization: Basic {}".format(b64cred))


url = "https://api.octopus.energy/v1/accounts/"

querystring = {"category":"inspirational"}

headers = {
	"authorization": "Basic 
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)