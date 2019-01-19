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

dashboard_list = [
  'cpu_core',
  'cpu_frequency',
  'disk',
  'filesystem',
  'grafana',
  'memory',
  'network',
  'overview',
  'prometheus',
  'zfs'
]


def make_request(req):
  try:
    res = urllib.request.urlopen(req)
    res_str = res.read().decode('utf-8')
    return json.loads(res_str)

  except urllib.error.HTTPError as e:
    # print('error:', e.code, '-', e.msg)
    return e


dashboard_meta = []

query = 'search?folderIds=0&query=&starred=false'
req = urllib.request.Request(url_base + query, headers=headers)

result = make_request(req)
# print(result)

for dashboard in result:
  try:
    index = dashboard_list.index(dashboard['title'])
    print(dashboard['title'])
    dashboard_meta.append(dashboard)

  except ValueError:
    print('not in list:', dashboard['title'])


for dashboard in dashboard_meta:
  query = 'dashboards/uid/' + dashboard['uid']
  req = urllib.request.Request(url_base + query, headers=headers)

  result = make_request(req)
  # print(result)

  file_name = './dashboards/' + dashboard['title'] + '.json'

  with open(file_name, 'w') as file:
    file.write(json.dumps(result))


print('\n=== done ===')