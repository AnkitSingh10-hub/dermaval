# pull official base image
FROM python:3.9.21-slim-bookworm

# Install system dependencies (This block looks good, kept as is)
RUN --mount=type=cache,target=/var/cache/apt,id=global_apt_cache,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,id=global_apt_lists,sharing=locked \
    apt-get update && \
    apt-get -y -o Dir::Cache::Archives=/var/cache/apt/ install --no-install-recommends \
    apt-transport-https ca-certificates gnupg fonts-dejavu fonts-noto fonts-noto-cjk \
    libffi-dev libpq-dev python-dev-is-python3 gcc 2to3 binutils libproj-dev \
    python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 git build-essential \
    software-properties-common curl libgdal-dev gdal-bin postgresql-client \
    gettext ffmpeg libmagic1 nano

# Install GCloud SDK (Kept as is)
RUN --mount=type=cache,target=/var/cache/apt,id=global_apt_cache,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,id=global_apt_lists,sharing=locked \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && apt-get update -y \
    && apt-get -y -o Dir::Cache::Archives=/var/cache/apt/ install google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.10 /uv /uvx /bin/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_DIR=/app \
    USER=app \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID -o ${USER}
RUN useradd -ms /bin/bash -u $UID -g $GID ${USER}

# Ensure the app directory exists and permissions are correct BEFORE switching users
RUN mkdir -p ${PROJECT_DIR} && chown ${USER}:${USER} ${PROJECT_DIR}

USER ${USER}
WORKDIR ${PROJECT_DIR}

# 1. FIX: Use --chown so the "app" user owns the config files
COPY --chown=${USER}:${USER} pyproject.toml uv.lock ./

# 2. OPTIMIZATION: Use --frozen and --no-install-project
# --frozen: Fails if lock file is out of sync (safety for production)
# --no-install-project: Installs dependencies but NOT your django app package yet (caching speed)
RUN --mount=type=cache,target=/home/${USER}/.cache/uv,id=uv-cache,uid=${UID},gid=${GID} \
    uv sync --frozen --no-install-project --dev

# 3. FIX: Copy the rest of the code with correct permissions
COPY --chown=${USER}:${USER} . .

# 4. Final sync to install the actual project (if your pyproject.toml defines the project itself)
RUN --mount=type=cache,target=/home/${USER}/.cache/uv,id=uv-cache,uid=${UID},gid=${GID} \
    uv sync --frozen --dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Command to run (optional default)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]