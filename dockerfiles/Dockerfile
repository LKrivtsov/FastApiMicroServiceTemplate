FROM python:3.11.2-alpine3.16
WORKDIR /app
COPY ./ /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# RUN rm -r venv
# RUN rm -r __pycache__
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
