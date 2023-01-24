FROM python:3.10

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip install -U pip && pip install -U -r requirements.txt
WORKDIR /app
RUN chmod 777 /app

COPY . .

CMD ["python3", "-m", "mbot/__main__"]
