# SDK для Gemini API

## Использование

1. Необходимо скопировать файл gemini.py к себе в проект
2. Создать экземпляр класса Gemini со своим API-ключом
3. Обращаться к API по аналогии с примером в usage.py

Доступно как использование в режиме диалога через функцию ask_gemini, так и одиночные текстовые запросы через ask_gemini_one_question

## Ответные статус коды

| Статус код | Значение                                                                                                                              |
|------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 200        | OK                                                                                                                                    |
| 400        | Плохой запрос (Ошибка в структуре диалога, <br/>не хватает информации в запросе, превышен<br/>лимит по токенам на один диалог и т.д.) |
| 401        | Недействительный API-ключ                                                                                                             |
| 402        | Закончился баланс                                                                                                                     |
| 500        | Внутренние ошибки сервиса                                                                                                             |
| 503        | API временно недоступен                                                                                                               |


## Переход с ChatGPT на Gemini

Если на данный момент бот работает на GPT, то чтобы не менять формат хранения диалога, можно использовать функцию gpt_to_gemini_format из файла utils.py для конвертации формата в тот, который принимается API.

Проверить корректность диалога (на соблюдение структуры) можно функцией dialog_validator из файла utils.py. Точно такая же проверка находится на стороне сервера.

## Помощь

Для помощи и предложений напишите мне: https://t.me/IMC_tech

SDK находится в стадии разработки, поэтому мы будем рады услышать ваши предложения по улучшению кода!

# Эндпоинты и прочая инфа если вы не можете использовать SDK

## REST API:

Base_url = http://103.35.188.2:8001/api/v1/

## Gemini text completion

| Method | Address     | Status code |
|--------|-------------|-------------| 
| POST   | text_prompt | 200         |

Payload:

```
{
    "user_api": "API_KEY",
    "history": [{"role": "user", "parts": ["Who are you?"]}]
}
```

Answer:
```
{
    "message": "I am Gemini!",
    "tokens": 24
}
```

## Check balance

| Method | Address  | Status code |
|--------|----------|-------------| 
| GET    | balance  | 200         |

Payload:

```
{
    "user_api": "API_KEY"
}
```

Answer:
```
{
    "balance": 5000,
    "user_id": 350789765
}
```
Баланс указывается в рублях
