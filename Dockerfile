# FROM continuumio/anaconda3:4.4.0
# COPY . /usr/app/
# EXPOSE 5000
# WORKDIR /usr/app/
# RUN pip install -r requirements.txt
# CMD python3 app.py

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]