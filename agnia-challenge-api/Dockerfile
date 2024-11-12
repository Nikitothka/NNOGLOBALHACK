# Используем Python 3.10 или выше
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY authorizations/requirements.txt /app/authorizations/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/authorizations/requirements.txt

# Копируем содержимое приложения
COPY . /app

# Открываем порт, который будет использовать uvicorn
EXPOSE 9000

# Запускаем приложение с uvicorn
CMD ["uvicorn", "authorizations.src.main:app", "--host", "0.0.0.0", "--port", "9000"]
