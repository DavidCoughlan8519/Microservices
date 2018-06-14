# Use an official Python runtime as a parent image
FROM python:3.6

# Copy the current directory contents into the container at /NewsStreamer
ADD . /NewsStreamer

# Set the working directory to /NewsStreamer
WORKDIR /NewsStreamer

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["./wait-for-it.sh", "-t", "0", "rabbitmq:5672", "--" ,"python", "NewsStreamer.py"]
