FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

ENV APP_MODULE app:/recosys/app

COPY --from=requirements-stage /tmp/requirements.txt /recosys/requirements.txt


RUN pip install --upgrade pip && pip install -r /recosys/requirements.txt


COPY ./pyproject.toml ./poetry.lock* /recosys
COPY ./app /recosys/app
COPY ./data /recosys/data
COPY ./_tests /recosys/_tests

WORKDIR /recosys

RUN mkdir reports


#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]

RUN ["pytest", "-v","--cov", "--junitxml=reports/result.xml"]

CMD tail -f /dev/null
