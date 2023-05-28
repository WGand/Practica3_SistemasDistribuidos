import argparse
import time
from kazoo.client import KazooClient
from os import system, name

class utils:
    def __init__(self, host, port):
        self.conn = KazooClient(hosts=f'{host}:{port}')

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

class Node:
    def __init__(self, id, utils):
        self.utils = utils
        self.path = '/leader'
        self.id = id
        self.account_id = None
        self.isLeader = False
        self.leader = None
        self.counter = 0
    
    def createNode(self):
        try:
            self.utils.conn.start()
            node_path = self.utils.conn.create(self.path + '/node-', ephemeral=True, sequence=True, makepath=True)
            self.account_id = node_path.split('/')[-1]
            print(f'Nodo creado: {node_path} bajo el id: {self.id}')
        except Exception as e:
            print(f'Error creando nodo: {e}')

    def watchChildren(self, children):
        sorted_children = sorted(children)
        self.leader = sorted_children[0]
        if self.leader == self.account_id:
            if self.isLeader:
                print(f'{self.id} es el nodo contador, cuenta: {self.counter}')
                self.count()
            else:
                print(f'{self.id} se ha vuelto el nodo contador')
                self.isLeader = True
                self.count()
        else:
            self.count()
            print(f'{self.id} es un nodo designado, cuenta: {self.counter}')

    def count(self):
        if self.isLeader:
            if not self.utils.conn.exists('/count'):
                self.utils.conn.create('/count', b"0")
            counter = int(self.utils.conn.get('/count')[0]) + 1
            self.utils.conn.set('/count', str(counter).encode())
        self.counter = int(self.utils.conn.get('/count')[0])

    def electLeader(self):
        while True:
            time.sleep(1)
            self.watchChildren(self.utils.conn.get_children(self.path))
    
    def run(self):
        self.createNode()
        self.electLeader()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distributed System Leader Election')
    parser.add_argument('-H', '--host', type=str, help='ZooKeeper server host', required=True)
    parser.add_argument('-p', '--port', type=str, help='ZooKeeper server port', required=True)
    parser.add_argument('account_id', type=str, help='Account ID')
    args = parser.parse_args()
    conn = utils(args.host, args.port)
    leader_election = Node(args.account_id, conn)
    leader_election.run()
