# Use the official Python 3.9 image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make Pickle file work
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1


# Copy the current directory contents into the container
COPY main2.py .
COPY .env .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for Cloud Run
ENV PORT 8080

# Run the Python script when the container launches
CMD ["python", "./main2.py"]

