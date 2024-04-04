# Используйте официальный образ Python 3.11
FROM python:3.11

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файлы зависимостей и установите зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте остальные файлы проекта внутрь контейнера
COPY . .

# Запустите приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
