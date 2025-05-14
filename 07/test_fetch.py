import unittest
from unittest.mock import patch, AsyncMock
import asyncio
import aiohttp
from fetcher import *


class TestFetcher(unittest.TestCase):

    @patch('aiohttp.ClientSession.get')
    def test_fetch_url_success(self, mock_get):
        async def run_test():
            mock_resp = AsyncMock()
            mock_resp.text.return_value = "Success"
            mock_get.return_value = mock_resp

            session = aiohttp.ClientSession()
            result = await fetch_url(session, "http://example.com")
            self.assertEqual(result, "Success")

            await session.close()

        asyncio.run(run_test())

    @patch('aiohttp.ClientSession.get')
    def test_fetch_url_timeout(self, mock_get):
        async def run_test():
            mock_get.side_effect = asyncio.TimeoutError

            session = aiohttp.ClientSession()
            result = await fetch_url(session, "http://example.com", timeout=1)
            self.assertEqual(result, {"error": "Время ожидания истекло"})

            await session.close()

        asyncio.run(run_test())

    @patch('aiohttp.ClientSession.get')
    def test_fetch_url_exception(self, mock_get):
        async def run_test():
            mock_get.side_effect = Exception("Some error")

            session = aiohttp.ClientSession()
            result = await fetch_url(session, "http://example.com")
            self.assertEqual(result,
                             {"error": "Неизвестная ошибка: Some error"})

            await session.close()

        asyncio.run(run_test())

    @patch('aiohttp.ClientSession.get')
    def test_fetch_worker(self, mock_get):
        async def run_test():
            mock_resp = AsyncMock()
            mock_resp.text.return_value = "Success"
            mock_get.return_value = mock_resp

            session = aiohttp.ClientSession()
            que = asyncio.Queue()
            await que.put("http://example.com")
            await que.put(None)  # Сигнал для завершения работы воркера

            await fetch_worker(session, que, "test_worker", 10)

            await session.close()

        asyncio.run(run_test())
