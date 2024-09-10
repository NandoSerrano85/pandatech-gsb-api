# FastAPI Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade setuptools===58.0.0
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# # Generate proto files
# RUN python generate_protos.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]