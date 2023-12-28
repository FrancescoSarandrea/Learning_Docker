#specify the base image
FROM python:3.8
# copy all the files to the container
COPY . .
# write the command for running the application
CMD ["python","test.py"]
