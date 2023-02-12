FROM python:3.11-slim

ENV PYTHONPATH "/app"


WORKDIR /app

RUN groupadd -g 5000 container && useradd -d /app -m -g container -u 5000 container

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip --no-cache-dir install -r requirements.txt

COPY . .
VOLUME ./data/

RUN chown -R 5000:5000 /app
USER container

CMD ["python", "run.py"]
