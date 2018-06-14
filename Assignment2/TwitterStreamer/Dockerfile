# Use an official Python runtime as a parent image
FROM python:3.6

ADD . /TwitterStreamer

WORKDIR /TwitterStreamer

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["./wait-for-it.sh", "-t", "0", "rabbitmq:5672", "--" ,"python", "twitterclient.py"]