FROM python:3.9-slim-buster


WORKDIR /app

# Copy requirements file
COPY requirements.txt app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r app/requirements.txt
RUN apt-get update && apt-get -y install ffmpeg libavcodec-extra

COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "bot/main.py"]