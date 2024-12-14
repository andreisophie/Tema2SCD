FROM python:3.6
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY /api /app
WORKDIR /app
EXPOSE 80
CMD ["python", "main.py"]