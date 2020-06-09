FROM python:3.7
ADD . /darius_submission
WORKDIR /darius_submission
RUN pip install -r requirements.txt