"""Тестирование серввера и клиента"""
import unittest
import queue
from unittest.mock import patch, MagicMock, mock_open
import socket
import threading
import json
from urllib.error import URLError
import server
import client


class TestServer(unittest.TestCase):
    """Тестирование сервера"""
    @patch("server.urlopen")
    def test_fetch_url_success(self, mock_urlopen):
        """Проверяем, что fetch_url корректно обрабатывает ответ"""
        # Мокаем содержимое страницы
        mock_resp = MagicMock()
        mock_resp.read.return_value.decode.return_value = "hello world hello"
        mock_urlopen.return_value = mock_resp

        args = MagicMock(k=2)
        result = server.fetch_url(args, "http://example.com")

        self.assertEqual(result, {"hello": 2, "world": 1})

    def test_fetch_url_timeout_with_message(self):
        """тестирование """
        args = MagicMock(k=5)
        with patch(
            "server.urlopen", side_effect=socket.timeout("Connection timed out")
        ):
            result = server.fetch_url(args, "http://example.com")
            self.assertEqual(result, {"error": "Время ожидания истекло"})

    def test_fetch_url_http_error(self):
        """Проверяем обработку ошибки сети"""
        args = MagicMock(k=5)
        with patch("server.urlopen", side_effect=URLError("Not found")):
            result = server.fetch_url(args, "http://example.com")
            self.assertEqual(
                result,
                {"error": "Неизвестная ошибка: <urlopen error Not found>"}
            )

    @patch("server.fetch_url", return_value={"hello": 2})
    @patch("server.mutex")
    # pylint: disable=W0613
    def test_worker_fetch_processes_url(self, mock_mutex, mock_fetch_url):
        """Тестирование 2"""
        que = queue.Queue()
        args = MagicMock(w=1, k=5)

        # Добавляем одну задачу
        mock_connection = MagicMock()
        que.put((mock_connection, "http://example.com"))
        que.put((None, None))  # сигнал завершения

        server.worker_fetch(que, args)

        # Проверяем, что fetch_url был вызван с правильным URL
        mock_fetch_url.assert_called_once_with(args, "http://example.com")

        # Проверяем отправку результата клиенту
        mock_connection.send.assert_called_once_with(
            json.dumps({"hello": 2}, ensure_ascii=False).encode()
        )
        mock_connection.close.assert_called_once()

    @patch("server.fetch_url", return_value={"hello": 2})
    @patch("server.mutex")
    # pylint: disable=W0613
    def test_worker_fetch_(self,
                           mock_mutex,
                           mock_fetch_url):
        """проверяем проверку"""
        que = queue.Queue()
        args = MagicMock(w=1, k=5)

        mock_connection = MagicMock()

        # Помещаем корректные данные в очередь
        que.put((mock_connection, "http://example.com"))  # ✅
        que.put((None, None))  # ✅ сигнал завершения

        server.worker_fetch(que, args)

        mock_fetch_url.assert_called_once_with(args, "http://example.com")

        mock_connection.send.assert_called_once_with(
            json.dumps({"hello": 2}, ensure_ascii=False).encode()
        )
        mock_connection.close.assert_called_once()


class TestClient(unittest.TestCase):
    """Класс для тестирования клиента"""
    def test_worker_fetch_processes_url(self):
        """Проверяем, что worker_fetch отправляет URL и получает ответ"""
        que = queue.Queue()
        que.put("http://example.com")
        que.put(None)

        with patch("client.socket") as mock_socket:
            mock_sock_instance = MagicMock()
            mock_sock_instance.recv.return_value.decode.return_value = (
                '{"hello": 2}'
            )
            mock_sock_instance.recv.return_value = b'{"hello": 2}'
            sock_mock = mock_socket.socket.return_value
            sock_mock.__enter__.return_value = mock_sock_instance

            thread = threading.Thread(target=client.worker_fetch, args=(que,))
            thread.start()
            thread.join()

    def test_worker_fetch_handles_none_gracefully(self):
        """Проверяем, что worker_fetch корректно завершает работу при None"""
        que = queue.Queue()
        que.put(None)

        with patch("client.socket"):
            thread = threading.Thread(target=client.worker_fetch, args=(que,))
            thread.start()
            thread.join()

            # Проверяем, что поток завершился без ошибок
            self.assertFalse(thread.is_alive())

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="http://example.com\nhttp://test.com\n",
    )
    def test_start_client_loads_urls_from_file(self, mock_file):
        """Проверяем, что start_client загружает URL'ы из файла"""
        args = MagicMock(number_threads=2, filename="urls.txt")

        with patch("threading.Thread") as mock_thread:
            mock_thread.return_value.join.return_value = None
            client.start_client(args)

            mock_file.assert_called_with(args.filename, "r", encoding="UTF-8")

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="http://example.com\n")
    # pylint: disable=W0613
    def test_start_client_creates_correct_number_of_threads(self, mock_file):
        """Проверяем, что создаётся правильное число потоков"""
        args = MagicMock(number_threads=3, filename="urls.txt")

        with patch("threading.Thread") as mock_thread:
            client.start_client(args)
            self.assertEqual(mock_thread.call_count, args.number_threads)

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="http://example.com\n")
    # pylint: disable=W0613
    def test_start_client_puts_none_for_each_thread(self, mock_file):
        """Проверяем, что после URL'ов добавляется None для каждого потока"""
        args = MagicMock(number_threads=3, filename="urls.txt")
        que_mock = MagicMock(spec=queue.Queue())

        with patch("queue.Queue", return_value=que_mock):
            client.start_client(args)

            # Проверяем, что None был положен N раз
            self.assertEqual(
                que_mock.put.call_count, 1 + args.number_threads
            )  # 1 URL + N None

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="http://example.com\nhttp://test.com\n",
    )
    # pylint: disable=W0613
    def test_start_client_starts_and_joins_all_threads(self, mock_file):
        """Проверяем, что все потоки запущены и дождены"""
        args = MagicMock(number_threads=2, filename="urls.txt")

        with patch("threading.Thread") as mock_thread:
            thread_instance = MagicMock()
            mock_thread.return_value = thread_instance

            client.start_client(args)

            # Проверяем, что Thread.start() и .join() вызваны
            self.assertEqual(thread_instance.start.call_count,
                             args.number_threads)
            self.assertEqual(thread_instance.join.call_count,
                             args.number_threads)


if __name__ == "__main__":
    unittest.main()
