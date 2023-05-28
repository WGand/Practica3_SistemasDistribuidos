# Distributed System Leader Election

Este es un sistema distribuido de elección de líder basado en ZooKeeper. El sistema permite la creación de nodos que compiten por el liderazgo y realizan operaciones basadas en su estado de liderazgo.

## Requisitos

- Python 3.x
- Biblioteca Kazoo
- Docker

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/WGand/Practica3_SistemasDistribuidos

2. Creación de la red e inicio de Zookeper:

    ```bash
    docker network create zoo-net
    docker run --rm -d --name zookeeper-server --network zoo-net --network-alias -p 2181:2181 zookeeper zookeeper:3.8.1

## Ejecución

3. Ejecución del script "electionLeaderWithCounter.py":

    ```bash
    python3 electionLeaderWithCounter.py -H <ZooKeeper_host> -p <ZooKeeper_port> <account_id>

Valores:

- <ZooKeeper_host>: La dirección IP o nombre de host del servidor de ZooKeeper.

- <ZooKeeper_port>: El puerto del servidor de ZooKeeper.

- <account_id>: El ID de cuenta del nodo.

## Explicación del programa:

- El script creará un nodo y competirá por el liderazgo en el sistema distribuido.

- Dependiendo de si el nodo se convierte en líder o no, realizará diferentes operaciones:

        1. Si el nodo se convierte en líder, incrementará un contador y mostrará su valor.
        2. Si el nodo no es líder, seguirá el contador y mostrará su valor.
        3. Si el nodo líder deja de existir, un nodo designado será el nuevo líder. (Puede tardar algunos segundos mientras Zookeeper elimina el último nodo líder)
- Puedes ejecutar múltiples instancias del script en diferentes terminales para simular varios nodos compitiendo por el liderazgo.