ARG PYTHON_VERSION=3.14.3

FROM python:${PYTHON_VERSION}-slim-bookworm AS python


# Build
FROM python AS builder

RUN apt-get update && apt-get install \
    --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.14 \
    UV_PROJECT_ENVIRONMENT=/venv

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

COPY . /src
WORKDIR /src

RUN --mount=type=cache,target=/root/.cache \
    uv sync \
        --locked \
        --no-dev \
        --no-editable


# Run
FROM python AS run

ARG APP_HOME=/src
ARG APP_USER=fastapi
ARG APP_GROUP=fastapi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/venv/bin:$PATH

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    gettext \
    libpq5 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r ${APP_GROUP} && \
    useradd -r -g ${APP_GROUP} -d ${APP_HOME} -N ${APP_USER}

RUN mkdir -p ${APP_HOME}/backend/app/logs && \
    chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}/backend/app/logs && \
    chmod 775 ${APP_HOME}/backend/app/logs

# Copy the pre-built virtualenv from builder
COPY --from=builder --chown=fastapi:fastapi /venv /venv

COPY --chown=${APP_USER}:${APP_GROUP} ./backend/docker/local/fastapi/entrypoint.sh /entrypoint.sh
COPY --chown=${APP_USER}:${APP_GROUP} ./backend/docker/local/fastapi/start.sh /start.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh && \
    chmod +x /entrypoint.sh /start.sh

#COPY --chown=${APP_USER}:${APP_GROUP} . ${APP_HOME}

USER ${APP_USER}

ENTRYPOINT [ "/entrypoint.sh" ]