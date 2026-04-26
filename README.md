# YouTube Notes App

Сервис для создания заметок к видео на YouTube.  
Пользователь добавляет ссылку на видео, сервис получает данные через YouTube API, а затем можно оставлять заметки с таймкодами.

## Технологии

- **FastAPI** — бэкенд
- **PostgreSQL** — база данных
- **Redis** — кэш и сессии
- **Kafka** — очередь задач
- **Docker** — контейнеризация
- **JWT** — авторизация

## Как запустить

```bash
git clone https://github.com/BabchenkovDanil/youtube-notes.git
cd youtube-notes
docker-compose up --build -d
------------------------------
Тестовый пользователь:

Email: test2@mail.ru
Пароль: qwerty
------------------------------
Эндпоинты
Метод        URL	          Описание
POST    /auth/register  	Регистрация
POST    /auth/login	      Вход (JWT)
POST	  /video/add	      Добавить видео (через Kafka)
GET	    /video/{id}	      Получить видео с заметками
POST	  /notes/	          Создать заметку
-----------------------------
Docker-контейнеры
Проект поднимает 6 контейнеров одной командой:

postgres — база данных
redis — кэш и сессии
zookeeper — для Kafka
kafka — очередь задач
fastapi — само приложение
consumer — воркер Kafka
