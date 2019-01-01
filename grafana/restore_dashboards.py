import sys
import os
import urllib.request
import json

grafana_host = sys.argv[1]
token = sys.argv[2]
dashboards_path = './dashboards/'

url_base = 'http://' + grafana_host + ':3000/api/'

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + token
}

def make_request(req):
  try:
    res = urllib.request.urlopen(req)
    res_str = res.read().decode('utf-8')
    return json.loads(res_str)

  except urllib.error.HTTPError as e:
    # print('error:', e.code, '-', e.msg)
    return e

def delete_dashboard(uid):
  print('delete_dashboard')

  query = 'dashboards/uid/' + uid
  req = urllib.request.Request(url_base + query, headers=headers, method='DELETE')

  return make_request(req)

def create_update_dashboard(data):
  print('create_update_dashboard')

  query = 'dashboards/db'
  data = json.dumps(data).encode('utf-8')
  req = urllib.request.Request(url_base + query, data=data, headers=headers)

  return make_request(req)


dashboard_files = os.listdir('./dashboards')
# print(dashboard_files)

for file in dashboard_files:
  with open(dashboards_path + file, 'r') as f:
    data = json.load(f)
  
  #print(json.dumps(data, indent=2))
  
  uid = data['dashboard']['uid']
  result = delete_dashboard(uid)
  print(' ', result)

  title = data['dashboard']['title']

  create_data = {
    'dashboard': {
      'id': None,
      'uid': uid,
      'title': title,
      'timezone': 'browser',
      'schemaVersion': 16,
      'version': 0
    },
    'folderId': 0,
    'overwrite': True
  }

  result = create_update_dashboard(create_data)
  print(' ', result)

  data['dashboard']['id'] = result['id']
  data['overwrite'] = True

  result = create_update_dashboard(data)
  print(' ', result)


print('\n=== done ===')