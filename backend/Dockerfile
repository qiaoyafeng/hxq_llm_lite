FROM python:3.10.13-slim

ENV PYTHONUNBUFFERED=1

# 设置时区为东八区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sed -i 's@deb.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources

# RUN apt-get update && apt-get install -y --no-install-recommends gcc procps vim

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

WORKDIR /opt/hxq_llm_lite/backend

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml uv.lock /opt/hxq_llm_lite/backend/

RUN uv sync --locked

WORKDIR /opt/hxq_llm_lite/backend/hxq_llm_lite

CMD ["/bin/bash"]
