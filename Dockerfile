FROM python:3.7-alpine3.8

EXPOSE 8888
EXPOSE 8889

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
CMD ["server"]
