FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
RUN --mount=type=secret,id=CLOUDFLARE_ID,target=/run/secrets/CLOUDFLARE_ID \
    --mount=type=secret,id=CLOUDFLARE_ACCESS_KEY,target=/run/secrets/CLOUDFLARE_ACCESS_KEY \
    --mount=type=secret,id=CLOUDFLARE_ACCESS_TOKEN,target=/run/secrets/CLOUDFLARE_ACCESS_TOKEN

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
