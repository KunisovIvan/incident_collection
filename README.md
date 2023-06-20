# incident_collection

## Основаная информация

Система сбора инцидентов

Так как тело запроса не определенно заранее, 
было принято решение использовать `mongoDB` (как я понял, вы используете `pymongo client` - взял его).
Я точно не знаю какие будут поля в запросе и сколько их будет, 
поэтому поле `body` сделал списком из объектов - это позволило мне добавить `индекс` на все поле `body`, 
что сильно ускорило поиск по БД. https://habr.com/ru/articles/177761/. Тоже самое и с `headers`.
Думаю, что парсинг ответов от `mongo pydantic` моделями тоже занимает время - можно с этим поработать еще.
Кроме того при тестах на 1 млн + записей начинаются проблемы с отрисовкой ответа даже в swagger, 
добавил `skip` и `limit` query params.

## Стек

Python 3.10

REST: FastAPI

БД: MongoDB (pymongo 3.11.0)

## Установка и запуск приложения

### Установка зависимостей

```shell
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Запуск приложения

```shell
# start service
docker-compose up -d

# start db
docker-compose up -d incident-collection-mongo

# start server
python3.10 -m incident_collection
```

## Структура проекта

 - main.py - точка входа
 - requirements.txt
 - usecases - слой бизнес логики
 - routes - роуты приложения
 - schemas - схемы запросов и отвветов pydantic, а также схемы юзкейсов
 - core - вещи связанные с логированием, запуском приложения
 - connectors - класс-коннектор для работы с mongoDB


## Основные методы
Подробную документацию по методам REST API можно получить на странице со swagger сервиса 
`http://{{service_url_here}}/docs`

## 1. Problems

### 1.1 Добавление инцидента

POST `/problems`

Request:

```json
{
    "hello": "world",
    "z": "6.456",
}
```


Response:

```json
{
  "hash": "-8479093057316546897"
}
```

### 1.2 Получение информации об инциденте

POST `/find?skip=0&limit=10`

Request:

```json
{"body": {"hello": "world"}}
```
or
```json
{"headers": {"host": "0.0.0.0:8300"}}
```

Response:

```json
[
  {
    "hash": "9068091503734132046",
    "body": {
      "hello": "world",
      "z": "6.456"
    },
    "headers": {
      "host": "0.0.0.0:8300",
      "connection": "keep-alive",
      "content-length": "42",
      "accept": "application/json",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
      "content-type": "application/json",
      "origin": "http://0.0.0.0:8300",
      "referer": "http://0.0.0.0:8300/docs",
      "accept-encoding": "gzip, deflate",
      "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
      "cookie": "_pk_id.1.2525=80f5036c0d028998.1671265965."
    }
  }
]
```

### 1.3 Получение информации об инциденте по hash

GET `/find2?h=9068091503734132046&skip=0&limit=10`

Response:

```json
[
  {
    "hash": "9068091503734132046",
    "body": {
      "hello": "world",
      "z": "6.456"
    },
    "headers": {
      "host": "0.0.0.0:8300",
      "connection": "keep-alive",
      "content-length": "42",
      "accept": "application/json",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
      "content-type": "application/json",
      "origin": "http://0.0.0.0:8300",
      "referer": "http://0.0.0.0:8300/docs",
      "accept-encoding": "gzip, deflate",
      "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
      "cookie": "_pk_id.1.2525=80f5036c0d028998.1671265965."
    }
  }
]
```

## Схема БД

problems
  - _id: ObjectId
  - body: list of dict
  - headers: list of dict
  - hash: str

