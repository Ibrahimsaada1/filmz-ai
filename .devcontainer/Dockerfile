FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

WORKDIR /workspaces/filmz-ai

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .