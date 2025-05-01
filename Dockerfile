
FROM python:3.10-slim

WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && wget -q "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.33.0-linux64.tar.gz" \
    && tar -xvzf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.33.0-linux64.tar.gz \
    && apt-get clean

EXPOSE 5000


CMD ["python", "image_processor_ui.py"]