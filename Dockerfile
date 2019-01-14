FROM python:3-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP /app/collector/collector.py
ENV FLASK_ENV development

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["/app/collector/collector.py"]