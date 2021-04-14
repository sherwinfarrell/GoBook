FROM python:3.6.9
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python3" ]
CMD ["-u", "flaskapp1.py" ]