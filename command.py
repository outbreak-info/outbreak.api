import argparse
import requests
import paramiko
import secrets

from sys import argv

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
    key = paramiko.RSAKey.from_private_key_file(secrets.PRIVATE_KEY)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = secrets.DEV_HOST
    ssh.connect(host, port=secrets.PORT, username=secrets.USERNAME, pkey=key)
    stdin, stdout, stderr = ssh.exec_command('cd outbreak.api && git pull && sudo systemctl restart outbreak_web.service && touch finished.txt')
    print('\n'.join(stdout.readlines()))
    print('\n'.join(stderr.readlines()))

if __name__ == '__main__':
    if argv[1] == 'push':
        push()
