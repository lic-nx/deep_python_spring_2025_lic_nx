"""master-worker cервер для обработки запросов от клиента."""
import threading
import queue
import argparse
import socket
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from collections import Counter
import re
from contextlib import closing


mutex = threading.Lock()
PROCESSED = 0


def fetch_url(args, url):  # pylint: disable=R1732
    """обращение по url"""
    popular_words = args.k
    try:
        with closing(urlopen(url, timeout=2.5)) as resp:
            words = resp.read().decode()
        words = resp.read().decode()
        cleaner_html = re.compile("<.*?>")
        clean_text = re.sub(cleaner_html, " ", words)
        print("clean_text", clean_text)
        clean_text = clean_text.split(" ")
        most_common_words = dict(Counter(clean_text).most_common(popular_words))
        return most_common_words
    except socket.timeout:
        return {"error": "Время ожидания истекло"}
    except (URLError, HTTPError) as e:
        return {"error": f"Ошибка сети: {e}"}
    except Exception as e:
        return {"error": f"Неожиданная ошибка: {e}"}

# pylint: disable=W0603
def worker_fetch(que, args):
    """используем потоки для выполнения задач"""
    while True:
        connection, data = que.get()
        if data is None:
            que.task_done()
            break
        most_common_words = fetch_url(args, data)
        with mutex:
            global PROCESSED
            PROCESSED += 1
            print(f"Url было обработано на данный момент {PROCESSED}")
        connection.send(json.dumps(most_common_words,
                                   ensure_ascii=False).encode())
        connection.close()
        que.task_done()


def server_start(args):
    """запуск сервера"""
    que = queue.Queue()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("localhost", 12345))
    listener.listen(5)
    threads = [
        threading.Thread(
            target=worker_fetch, args=(que, args), name=f"worker_fetch_{i}"
        )
        for i in range(args.w)
    ]
    for th in threads:
        th.start()
    try:
        while True:
            connection, _ = listener.accept()
            data = connection.recv(1024).decode("utf8")
            que.put((connection, data))
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        for _ in range(args.w):
            que.put((None, None))
        for th in threads:
            th.join()
        listener.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w",
                        type=int,
                        default=5,
                        help="workers count")
    parser.add_argument("-k",
                        type=int,
                        default=5,
                        help="most common words count")
    console_args = parser.parse_args()
    server_start(console_args)
