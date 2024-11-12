import base64
import io
import time

from pydub import AudioSegment
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType
import os


class AudioRecognition:

    def __init__(self):
        # Аутентификация через API-ключ.
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=os.getenv('YANDEX_API_KEY')
            )
        )
        self.model = model_repository.recognition_model()
        self.model.model = 'general'
        self.model.language = 'ru-RU'
        self.model.audio_processing_type = AudioProcessingType.Full

    async def recognize_audio(self, audio) -> str:
        # Декодируем Base64 строку в двоичный формат
        audio_bytes = base64.b64decode(audio)

        # Преобразуем двоичные данные в байтовый поток для обработки с pydub
        audio_stream = io.BytesIO(audio_bytes)

        # Используем pydub для обработки аудиофайла
        audio = AudioSegment.from_file(audio_stream)
        # Распознавание речи в указанном аудиофайле.
        result = self.model.transcribe(audio)

        return str(result[0])
