FROM python:3.13-alpine3.24

RUN apk add --no-cache bash qemu-system-x86_64

WORKDIR /app/backend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
