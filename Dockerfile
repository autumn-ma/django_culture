# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# libraqm0 for captcha
RUN apt-get update \
 && apt-get -y install libpq-dev gcc libraqm0

# Install the project into /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Convert lockfile to requirements.txt and install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
 --mount=type=bind,source=uv.lock,target=uv.lock \
 --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
 uv export --format requirements-txt --no-dev > requirements.txt && \
 uv pip install --system -r requirements.txt

# Copy source code
COPY . .


RUN mkdir -p /var/log/legal_ai

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Fix line endings and make it executable
RUN sed -i 's/\r$//g' /app/entrypoint.sh && \
 chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
