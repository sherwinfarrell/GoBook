FROM python:3.8.0-slim
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python3" ]
CMD ["-u", "aioapp2.py" ]