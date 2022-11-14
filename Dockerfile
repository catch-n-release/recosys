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
COPY ./_tests /recosys/_tests
COPY ./app /recosys/app
COPY ./data /recosys/data
COPY ./ml /recosys/ml
COPY ./utils /recosys/utils


WORKDIR /recosys

RUN mkdir reports

#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]

RUN ["pytest", "-v","_tests/unit/test_ml","--cov", "--junitxml=reports/ml_result.xml"]
RUN ["pytest", "-v",--ignore=_tests/unit/test_ml","--cov", "--junitxml=reports/app_result.xml"]

CMD tail -f /dev/null
