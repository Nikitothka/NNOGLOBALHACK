# Используем Python 3.10 или выше
FROM python:latest

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt && pip3 install https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip --force-reinstall

# Копируем содержимое приложения
COPY . /app

# Запуск приложения
CMD ["python", "main.py"]
