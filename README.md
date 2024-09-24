### Название проекта
"API для Yatube"
### Описание проекта
Приложение Yatube позволяет размещать, группировать , росматривать, комментировать публикации, подписываться на авторов. Внесение изменений в данные требует авторизации.
Проект представляет собой реализацию приложения API для Yatube, которое дает возможность взаимодействовать с приложением другим системам посредством http-запросов.
### Технологии  
Используемое ПО:
python 3.9
Django==3.2.16
djangorestframework==3.12.4
djangorestframework-simplejwt==4.7.2
Pillow==9.3.0
PyJWT==2.1.0
### Как запустить проект:
https://github.com/VoznayaOlga/api_final_yatube.git

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VoznayaOlga/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### Спецификация:
При локальном запуске проекта спецификация доступна по ссылке 
http://127.0.0.1:8000/redoc/