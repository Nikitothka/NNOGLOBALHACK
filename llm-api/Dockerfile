FROM python:3.10

WORKDIR /app


RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8035

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8035"]