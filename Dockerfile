FROM python:3.10 as builder
RUN python3.10 -m venv /usr/share/python3/app
COPY . /appp
EXPOSE 80
WORKDIR /appp
RUN /usr/share/python3/app/bin/pip install -r requirements.txt
CMD ["/usr/share/python3/app/bin/python3", "-m", "timetable_bot"]
