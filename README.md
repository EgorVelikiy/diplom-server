# Облачное хранилище  

## Инструкции по развертыванию приложения  

### Настройка сервера:

1. Необходимо клонировать репозиторий:
   ```
   git clone https://github.com/EgorVelikiy/diplom-server
   ```

2. Запустите проект в любой IDE
3. Откройте терминал
4. Введите команду:
   ```
   py -3 -m venv .venv
   ```

5. Активируйте окружение:
   ```
   .venv\scripts\activate
   ```
6. Установите все записимости:
   ```
   pip install -r requirements.txt
   ```

7. Создайте файл `.env` в директории
8. Введите значения:
   ```
   DEBUG=
   SECRET_KEY=
   DB_HOST=localhost
   DB_NAME=dbname
   DB_PORT="5432"
   DB_USER=user
   DB_PASSWORD=password
   ```
9.  Для того, чтобы создать базу данных:
    ```
    createdb -U <DB_USER> <DB_NAME>
    ```
    Подставьте значения из `.env` в `<DB_USER>` и `<DB_NAME>`
10. Введите пароль, указанный в `.env`
11. Создайте суперпользователя:
    ```
    python manage.py create_superuser
    ```
    Имя пользователя и пароль обязательны для заполнения

12. Выполните миграции:
    ```
    python manage.py migrate
    ```

13. Запустите сервер:
    ```
    python manage.py runserver
    ```

