# Базовый образ
FROM python:3.11

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы зависимостей и установите их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте проект
COPY . .

# Здесь может быть ваша команда для запуска парсера
CMD ["python", "main.py"]
