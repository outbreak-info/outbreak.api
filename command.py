import argparse
import requests
import paramiko

def attach_repository(name):
    backup_name = f"{name}_backup"
    data = {
        "name": f"outbreak_{name}_repository",
        "type": "s3",
        "settings": {
            "bucket": "biothings-es6-snapshots",
            "region": "us-west-2",
            "base_path": f"outbreak/{name}"
        }
    }
    res = requests.put(f"http://localhost:9200/_snapshot/{backup_name}?pretty", json=data)
    return res

def fetch_index(name, index_name, index_rename):
    backup_name = f"{name}_backup"

    data = {
      "indices": f"{index_name}",
      "ignore_unavailable": True,
      "include_global_state": True,              
      "allow_no_indices": False,
      "rename_pattern": ".+",
      "rename_replacement": f"{index_rename}"
    }
    res = requests.post(f"http://localhost:9200/_snapshot/{backup_name}/{index_name}/_restore?pretty", json=data)
    return res

def push():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = secrets.DEV_HOST
    ssh.connect(host, port=secrets.PORT, username=secrets.USERNAME, password=secrets.PASSWORD, look_for_keys=False)
    ssh.exec_command('cd outbreak.api && git pull && sudo systemctl restart outbreak_web.service && touch finished.txt')

if __name__ == '__main__':
    if argv[1] == 'push':
        push()
