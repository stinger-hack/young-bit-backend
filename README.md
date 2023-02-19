# Backend

## Реализованная функциональность

* формальные / неформальные события - добавление и просмотр
* задания - создание, просмотр, назначение заданий
* инициативы - добавление, подтверждение, просмотр
* важные события - создание, передача по вебсокету при добавлении нового события
* профиль пользователя - просмотр
* библиотека - добавление, просмотр, прогресс по статье
* пользователи - задания, связь с остальными сущностями
* отделы - задания, связь с остальными сущностями
* магазин - просмотр, покупка, списание баллов, добавление товаров, начисление бонусов
* бот-помощник - заполнение форм, срочный вызов сотрудника, бонусы

## Особенность проекта

* **нетворк ланчи** - обед со случайными людьми, которое позволит знакомиться с людьми
* срочный вызов сотрудника - уведомление наставнику при критических ситуациях
* магазин с товарами
* статистика по задачам
* награды для отделов в виде больших призов (пазлы)
* гибкие цели на неделю
* **стикеры в телеграме**

## Стек

### Frontend

* React, SASS
* Typescript
* Vite
* Docker, Docker-compose

### Backend

* Python, FastAPI
* PostgreSQL, SQLAlchemy
* Websockets
* Docker, Docker-compose

## Демо

* <http://stingerhack.space/> - версия для работника
* <https://stingerhack-admin.web.app> - версия для HR
* <http://stingerhack.space:8000/api/docs> - API

## Запуск проекта

Все части проекта можно запустить из докера

```bash
cd backend
docker-compose up --build -d
cd bot
docker-compose up --build -d
```

Далее нужно заполнить данные в БД и готово!

РАЗРАБОТЧИКИ

|          |      |   |
|--------------|-----------|------------|
| Павел Ивин | Backend     | [@pavivin](https://t.me/pavivin)      |
| Семён Колесников      | Frontend  | [@dragonite24](https://t.me/dragonite24)       |
| Дык Фам      | Frontend  | [@TagidickTagidick](https://t.me/TagidickTagidick)       |
