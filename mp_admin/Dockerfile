# Базовый образ
FROM python:3.11

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы зависимостей и установите их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте проект
COPY . .

# Запустите сервер разработки Django на 0.0.0.0
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
