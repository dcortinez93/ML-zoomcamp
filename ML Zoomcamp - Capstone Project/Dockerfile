FROM agrigorev/zoomcamp-model:3.8.12-slim

RUN pip install pipenv
 
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "model.bin", "./"]

CMD waitress-serve --listen=0.0.0.0:$PORT predict:app