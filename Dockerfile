FROM node:22-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /skill
COPY . .
RUN python3 scripts/bootstrap.py && node node_modules/playwright/cli.js install --with-deps chromium
ENV PATH="/skill/.venv/bin:${PATH}"
ENTRYPOINT ["python", "/skill/scripts/remake.py"]
CMD ["doctor"]
