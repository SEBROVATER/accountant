FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt && \
    pip cache purge


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN mkdir -p /home/nonroot

ENV HOME=/home/nonroot
ENV APP_HOME=/home/nonroot/app
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

COPY --from=builder /app/wheels ${HOME}/wheels

RUN pip install --upgrade pip && \
    pip install --no-cache ${HOME}/wheels/* && \
    pip cache purge

COPY . ${APP_HOME}

ENTRYPOINT ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--forwarded-allow-ips=*"]
