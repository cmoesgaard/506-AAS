FROM ubuntu:18.04

RUN apt-get update && apt-get -y install cron python3 python3-pip

RUN echo "0 10 * * 1-5 python3 /app/menu.py > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/bot-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/bot-cron

# Apply cron job
RUN crontab /etc/cron.d/bot-cron

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

# Run the command on container startup
CMD ["cron", "-f"]

