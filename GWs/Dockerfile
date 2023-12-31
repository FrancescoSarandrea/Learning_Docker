FROM python:3.8

# Install dependencies
RUN apt-get update && apt-get install -y \
    libfftw3-dev \
    libhdf5-dev \
    libgsl-dev

# Install GWpy
RUN pip install gwpy

# Set the working directory
#WORKDIR /app

# Copy your application code into the container
COPY . .

# Command to run your application
CMD ["python", "GW_test.py"]
