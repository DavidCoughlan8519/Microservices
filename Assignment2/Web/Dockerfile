# Use an official Python runtime as a parent image
FROM python:3.6

ADD . /Web

WORKDIR /Web

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["./wait-for-it.sh", "-t", "0", "rabbitmq:5672", "--" ,"python", "twitterweb.py"]