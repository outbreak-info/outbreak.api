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
    print(requests.delete(f'http://localhost:9200/{index_rename}'))

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

def push(restart):
    key = paramiko.RSAKey.from_private_key_file(secrets.PRIVATE_KEY)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host = secrets.DEV_HOST
    ssh.connect(host, port=secrets.PORT, username=secrets.USERNAME, pkey=key)

    commands = [
            'echo "Performing git pull"',
            'cd outbreak.api',
            'git pull',
    ]
    if restart:
        commands += [
            'echo "Performing server restart"',
            'sudo systemctl restart outbreak_web.service',
            'sudo journalctl -u outbreak_web.service | tail -2'
        ]
    stdin, stdout, stderr = ssh.exec_command(' && '.join(commands))
    print(''.join(stdout.readlines()))
    err = stderr.readlines()
    if err:
        print('----- Errors ----------')
        print(''.join(err))

if __name__ == '__main__':
    if argv[1] == 'push':
        restart = True
        if len(argv) > 2 and argv[2] == '-no-restart':
            restart = False
        push(restart)
    elif argv[1] == 'update':
        fetch_index('genomics_dev', argv[2], 'outbreak-genomics')
