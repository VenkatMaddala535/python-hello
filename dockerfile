FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

EXPOSE 5001

CMD ["python", "src/hello_web/__main__.py"]



