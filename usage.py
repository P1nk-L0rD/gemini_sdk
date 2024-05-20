import asyncio

from gemini import Gemini


# Простейшее использование
gemini = Gemini("API_KEY")


def simple_usage(question: str):
    answer, tokens = asyncio.run(gemini.ask_gemini_one_question(question))
    print(answer)


simple_usage("Что такое красивый код и почему я не умею его писать?")


# С поддержкой контекста


async def make_request_to_gemini(user_id: int, question: str, dialogs: dict[int: dict]) -> tuple[str, int]:

    # Проверка был ли у пользователя ранее диалог с ботом
    if user_id not in dialogs:
        # Создание нового диалога если нет
        history = [{"role": "user", "parts": [question]}]

    # Проверка на превышения лимита по контексту
    elif dialogs[user_id]["tokens"] > gemini.TOKEN_LIMIT:
        print("Диалог был сброшен из-за превышения максимальной длины контекста!")
        history = [{"role": "user", "parts": [question]}]

    # Использование старого диалога если прошлые условия не соблюдаются
    else:
        # Создается копия диалога на случай если не придет успешный ответ
        history = dialogs[user_id]["history"].copy()
        history.append({"role": "user", "parts": [question]})

    # Обращение к Gemini
    answer, tokens = gemini.ask_gemini(history)

    # Сохранение ответа Gemini в копию диалога
    history.append({"role": "model", "parts": [answer]})

    # Сохранение копии диалога и расхода в токенов в историю всех диалогов
    dialogs[user_id] = {
        "history": history,
        "tokens": tokens
    }

    return answer, tokens

# Узнать баланс

print(asyncio.run(gemini.get_balance()))
