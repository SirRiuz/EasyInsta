FROM python:3.12-slim

WORKDIR /app

COPY ci/requirements.txt ci/requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python"]
