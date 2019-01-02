import sys
import urllib.request
import json

grafana_host = sys.argv[1]
token = sys.argv[2]

url_base = 'http://' + grafana_host + ':3000/api/'

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + token
}

datasource_list = [
  'prometheus'
]


def make_request(req):
  try:
    res = urllib.request.urlopen(req)
    res_str = res.read().decode('utf-8')
    return json.loads(res_str)

  except urllib.error.HTTPError as e:
    # print('error:', e.code, '-', e.msg)
    return e


query = 'datasources'
req = urllib.request.Request(url_base + query, headers=headers)

result = make_request(req)
# print(json.dumps(result, indent=2))

for datasource in result:
  try:
    index = datasource_list.index(datasource['name'])
    print(datasource['name'])

    file_name = './datasources/' + datasource['name'] + '.json'

    with open(file_name, 'w') as file:
      file.write(json.dumps(datasource))

  except ValueError:
    print('not in list:', datasource['name'])


print('\n=== done ===')