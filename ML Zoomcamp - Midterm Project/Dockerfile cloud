FROM agrigorev/zoomcamp-model:3.8.12-slim

RUN pip install pipenv
 
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict_cloud.py", "model.bin", "./"]

ENTRYPOINT ["waitress-serve",  "predict:app"]