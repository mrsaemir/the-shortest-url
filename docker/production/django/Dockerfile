FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

COPY . ${APP_HOME}
WORKDIR ${APP_HOME}

RUN pip install -r ./requirements/${BUILD_ENVIRONMENT}.txt

COPY ./docker/production/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/${BUILD_ENVIRONMENT}/django/start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
