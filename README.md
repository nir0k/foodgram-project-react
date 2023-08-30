# Foodgram

Сайт для побуликации и просмотра рецептов
Возможноти:
- Публикация рецептов
- Просмотр рецептов других пользователей сайта
- Подписка на пользователей
- Добавление рецептов в список покупок
- Печать списка покупок

## Для подключения
домен сервера: foodgram-book.ddns.net
Суперпользователь: admin
Пароль: Dem0nh)st


### Как запустить проект:
<details>
<summary>Инструкция</summary>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nir0k/foodgram-project-react.git

```

```
cd foodgram-project-react
```

Установить docker


Запустить docker-compose:

```
docker compose up
```

При первом запуске создать суперпользователя
```
docker exec <название контерйнера backend> python /app/manage.py createsuperuser
```
</details>

# Для входа на сайт
- Вход для пользователей: http://localhost:7000/
- Вход в консоль администратора: http://localhost:7000/admin/
- Начальная точка API : http://localhost:7000/api/