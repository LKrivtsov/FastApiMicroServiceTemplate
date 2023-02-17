FROM python:3.11.2-alpine3.16

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements/production.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
