import aiohttp
from aiohttp.client_exceptions import ClientResponseError


class Gemini:

    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.API_URL = "https://yummyapi.shop/api/v1/"
        self.TEXT_URL = self.API_URL + "text_prompt"
        self.BALANCE_URL = self.API_URL + "balance"
        self.HEADERS = {"Content-Type": "application/json"}
        self.TOKEN_LIMIT = 12_000
        self.TIMEOUT = aiohttp.ClientTimeout(total=90)
        self.ATTEMPTS = 2

    async def __make_request(self, body: dict):
        """
        Внутренний метод класса. Предназначен для отправки асинхроного запроса.
        Посылает запрос self.ATTEMPTS раз в случае статус кода, отличного от 200.
        Вызывает ошибку в случае неуспеха.
        """

        async with aiohttp.ClientSession(timeout=self.TIMEOUT) as session:
            # 2 попытки запроса если в первый раз вернулся статус код не 200
            for attempt in range(self.ATTEMPTS):
                async with session.post(url=self.TEXT_URL, json=body, headers=self.HEADERS) as response:

                    if response.status == 200:
                        response = await response.json()
                        response_text = response["message"]
                        tokens = response["tokens"]
                        return response_text, tokens
                    else:
                        if attempt < self.ATTEMPTS - 1 and response.status not in range(400, 500):
                            continue

                        raise ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            code=response.status,
                            message=f"{response.reason} {await response.text()}",
                            headers=response.headers
                        )

    async def ask_gemini(self, dialog: list[dict]) -> tuple[str, int]:
        """
        Основная функция для запросов к Gemini.
        Функция принимает диалог следующего формата:
        [{"role": "user", "parts": [prompt]}, {"role": "model", "parts": [response_text]}]
        Функция возвращает ответ модели и стоимость в токенах.
        """

        body = {
            'user_api': self.API_KEY,
            'history': dialog
        }

        # 2 попытки запроса если в первый раз произошла ошибка
        for attempt in range(self.ATTEMPTS):
            try:
                answer, tokens = await self.__make_request(body)
                return answer, tokens
            except Exception as error:
                if attempt < self.ATTEMPTS - 1:
                    continue
                raise error

    async def ask_gemini_one_question(self, question: str) -> tuple[str, int]:
        """
        Функция принимает строку, которая будет являться запросом для Gemini.
        Возвращает ответ и количество потраченных токенов.
        Главное отличие функции - работает с одним вопросом без контекста.
        """
        dialog = [{"role": "user", "parts": [question]}]
        return await self.ask_gemini(dialog)

    async def get_balance(self):
        """
        Узнать текущий баланс.
        """
        body = {"user_api": self.API_KEY}
        async with aiohttp.ClientSession(timeout=self.TIMEOUT) as session:
            # 2 попытки запроса если в первый раз вернулся статус код не 200
            for attempt in range(self.ATTEMPTS):
                async with session.get(url=self.BALANCE_URL, params=body, headers=self.HEADERS) as response:

                    if response.status == 200:
                        response = await response.json()
                        return response["balance"]
                    else:
                        if attempt < self.ATTEMPTS - 1 and response.status not in range(400, 500):
                            continue

                        raise ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            code=response.status,
                            message=f"{response.reason} {await response.text()}",
                            headers=response.headers
                        )
