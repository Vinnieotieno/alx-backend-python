FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# commands
# docker build -t messaging-app .
# docker run -d -p 8000:8000 messaging-app