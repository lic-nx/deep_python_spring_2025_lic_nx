
"""утилита, отправляющая запросы с урлами серверу по TCP в несколько потоков."""
import threading
import queue
import argparse
import socket


def worker_fetch(que):
    """отправка запросов"""
    print(f"{threading.current_thread().name} -- started")
    while True:
        url = que.get()
        if url is None:
            que.put(None)
            break

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.connect(("localhost", 12345))
        server_sock.send(url.encode())
        response = server_sock.recv(1024).decode()
        server_sock.close()
        print(f"{str(url)} : {response}")


# pylint: disable=W0621
def start_client(args):
    """запуск клиента"""
    que = queue.Queue()
    with open(args.filename, "r", encoding="UTF-8") as file:
        for url in file:
            que.put(url.strip())

    for _ in range(args.number_threads):
        que.put(None)

    threads = [
        threading.Thread(target=worker_fetch,
                         args=(que,),
                         name=f"worker_fetch_{i}")
        for i in range(args.number_threads)
    ]

    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number_threads", type=int, help="Number of threads")
    parser.add_argument("filename", type=str, help="File containing URLs")
    args = parser.parse_args()
    start_client(args)
