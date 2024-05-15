import aiohttp


class Gemini:

    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.URL = "http://103.35.188.2:8000/api/v1/text_prompt"
        self.HEADERS = {"Content-Type": "application/json"}
        self.TOKEN_LIMIT = 12_000
        self.TIMEOUT = 60
        self.ATTEMPTS = 2

    async def ask_gemini(self, dialog: list[dict]) -> tuple[str, int]:
        """
        Основная функция для запросов к Gemini.
        Функция принимает диалог следующего формата:
        [{"role": "user", "parts": [prompt]}, {"role": "model", "parts": [response_text]}]
        Функция возвращает ответ модели и стоимость в токенах.
        """

        body = {
            'api_key': self.API_KEY,
            'history': dialog
        }

        async with aiohttp.ClientSession(timeout=self.TIMEOUT) as session:
            for attempt in range(self.ATTEMPTS):
                async with session.post(url=self.URL, json=body, headers=self.HEADERS) as response:

                    if response.status == 200:
                        response = await response.json()
                        response_text = response["tokens"]
                        tokens = response["tokens"]
                        return response_text, tokens
                    else:
                        details = response.content
                        error = f"ERROR: {details}, CODE: {response.status}, FULL: {response}"
                        if attempt == self.ATTEMPTS - 1:
                            raise Exception(error)
                        else:
                            print("Ошибка запроса, повторная попытка...")

    async def ask_gemini_one_question(self, question: str) -> tuple[str, int]:
        """
        Функция принимает строку, которая будет являться запросом для Gemini.
        Возвращает ответ и количество потраченных токенов.
        Главное отличие функции - работает с одним вопросом без контекста.
        """
        dialog = [{"role": "user", "parts": [question]}]
        return await self.ask_gemini(dialog)
