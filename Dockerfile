FROM python:latest
LABEL Maintainer="mahmoudhsamaha"
WORKDIR /home/bookstore-api
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "bookstore-api.py"]
