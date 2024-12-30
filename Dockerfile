FROM python:3.10-slim
WORKDIR /usr/src/app
COPY bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY bot/ .
CMD [ "python", "app/main.py" ]