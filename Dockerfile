FROM python:3.9
WORKDIR /code
COPY requirement.txt /code/requirement.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt
COPY . /code
CMD [ "uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]