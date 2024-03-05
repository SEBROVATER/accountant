FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip && pip install -U pip setuptools wheel && pip install pdm

#RUN apt-get update && \
#    apt-get install -y --no-install-recommends gcc

COPY pyproject.toml .
RUN mkdir __pypackages__ && pdm install --prod --no-editable


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# create directory for the nonroot user
RUN mkdir -p /home/nonroot

ENV HOME=/home/nonroot
ENV APP_HOME=/home/nonroot/app
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

RUN pip install --upgrade pip
ENV PYTHONPATH=/pkgs
COPY --from=builder /app/__pypackages__/3.12/lib /pkgs
COPY --from=builder /app/__pypackages__/3.12/bin/* /bin/

COPY . ${APP_HOME}

#CMD ["granian", "--interface", "asgi", "--port", "${EXPENSES_PORT}", "app.main:app"]
#CMD ["uvicorn", "app.main:app"]
