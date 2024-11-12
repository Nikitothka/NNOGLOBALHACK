FROM python:latest

WORKDIR /app

COPY app/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt  && pip3 install https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip --force-reinstall

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]