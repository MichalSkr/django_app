FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE file_app.settings
CMD ["python","manage.py","runserver"]