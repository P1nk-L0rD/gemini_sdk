def gpt_to_gemini_format(dialog: list[dict]):
    """
    Функция принимает диалог формата ChatGPT, например:
    [
        {"role": "system", "content": "You are ChatGPT."},
        {"role": "user", "content": "Who are you?"},
        {"role": "assistant", "content": "I am ChatGPT"}
    ]
    А возвращает диалог в формате, приемлимом для Gemini.
    Функция не валидирует принимаемый диалог, считая корректным.

    Подходит для быстрого перехода с GPT на Gemini с минимальными изменениями кода.
    """
    if len(dialog) < 1:
        return []

    if dialog[0].get("role") == "system":
        dialog.pop(0)

    gemini_dialog = list()
    for pair in dialog:
        role = pair.get("role")
        content = pair.get("content")

        if role != "user":
            role = "model"

        gemini_dialog.append({"role": role, "parts": [content]})

    return gemini_dialog


def dialog_validator(dialog: list[dict]) -> bool:
    """
    Функция принимает диалог и проверяет его формат на корректность.
    Возвращает True если формат корректен, в остальных случаях возвращает False.

    По умолчанию функция не используется на стороне клиента, однако точно такая же проверка
    происходит на стороне API, поэтому рекомендуем локально проверить данные перед отправкой.
    """
    if not isinstance(dialog, list):
        return False

    if len(dialog) < 1:
        return False

    for index, pair in enumerate(dialog):
        if not isinstance(pair, dict):
            return False

        role = pair.get("role")
        if index % 2 == 0:
            if role != "user":
                return False
        else:
            if role != "model":
                return False

        parts = pair.get("parts")
        if not isinstance(parts, list):
            return False

        if len(parts) != 1:
            return False

        if not isinstance(parts[0], str):
            return False

    return True
