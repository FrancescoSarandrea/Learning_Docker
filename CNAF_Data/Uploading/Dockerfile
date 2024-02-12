# Use an official Python runtime as a parent image
FROM python:3.11

#FROM centos:8

# Install dependencies
RUN pip3 install pandas gwpy rucio-clients dask


#FROM fedora:latest

#RUN dnf -y install python3-gfal2 gfal2-plugin-file gfal2-plugin-gridftp gfal2-plugin-http gfal2-plugin-srm gfal2-plugin-xrootd xrootd-client gfal2-util

#FROM cern/cc7-base



RUN dnf install -y python3-gfal2 gfal2-plugin-file gfal2-plugin-gridftp gfal2-plugin-http gfal2-plugin-srm gfal2-plugin-xrootd xrootd-client gfal2-util

#RUN apt-get update && apt-get install -y gfal2-tools



#RUN yum install -y python3 \
#    && pip3 install pandas gwpy rucio-clients dask

# Set the working directory in the container
WORKDIR /app

# Copy the notebook into the container
COPY download-cnaf.py gspy_O3a.csv O3_raw_CNAF.txt /app/

# Run the application when the container launches
CMD ["python","download-cnaf.py"]



#ENV BEARER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ1MFUyNmxSOVFMM2NhYTBaMnBtQ3NxQk1SN3ZJVmFtcmo3STNwYW1JaDk4In0.eyJleHAiOjE3MDYxMDcyMzcsImlhdCI6MTcwNjEwMzYzNywiYXV0aF90aW1lIjoxNzA2MTAzNjM3LCJqdGkiOiJiMjhhNzkyMS02YThmLTQ1NmMtOWM1ZS1hNzQxZTI0NjY2NTkiLCJpc3MiOiJodHRwczovL2FhaS1kZW1vLmVnaS5ldS9hdXRoL3JlYWxtcy9lZ2kiLCJzdWIiOiIxMTNjMDE3NGE0MjZmZDRiNWNiMjM2OGQzZTc0YmJmNDk2NGVhOGZmMmEwNjQwMzVkMTU3M2UzNGRiYzkwNjBmQGVnaS5ldSIsInR5cCI6IkJlYXJlciIsImF6cCI6InRva2VuLXBvcnRhbCIsIm5vbmNlIjoiMmFkMjQ0YTVmZGIxYzFiN2M5MmE4M2E3NDRjMTY4NDYiLCJzZXNzaW9uX3N0YXRlIjoiMmE5NTBmZWItNDE1My00NjFjLTlmMWMtYzcwYTdlMWQzNmZlIiwic2NvcGUiOiJvcGVuaWQgZWR1cGVyc29uX2VudGl0bGVtZW50IHZvcGVyc29uX2lkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIyYTk1MGZlYi00MTUzLTQ2MWMtOWYxYy1jNzBhN2UxZDM2ZmUiLCJ2b3BlcnNvbl9pZCI6IjExM2MwMTc0YTQyNmZkNGI1Y2IyMzY4ZDNlNzRiYmY0OTY0ZWE4ZmYyYTA2NDAzNWQxNTczZTM0ZGJjOTA2MGZAZWdpLmV1IiwiYXV0aGVudGljYXRpbmdfYXV0aG9yaXR5IjoiaHR0cHM6Ly9pZHAuaW5mbi5pdC9zYW1sMi9pZHAvbWV0YWRhdGEucGhwIn0.D8WnEVoUSAuErCp-DUWLViWA1d71KORZwh6jHlJmtQoxvDcPJmDJBPIfS3Ith3ETzFawbdOvl-rKBtJsbExGW2k4AX8AeP5tDnfPfxBNoVfOSxTURxM4KzpCSpZP513_XNN3osHCFiRuMLRXA4VKtcWOcUh70QQNyi4BnI11h8H9OvHI1yDtX668dQ80uVgEoblWfe1UanJZ1BNRxcJ15RUSZwzseyfu4Kyk1vuypBtsevIy-z9zqmJOyNTUbislZlty3XOvJB7V8HmaSQqTINoau9vHMQvnJFZ3bt6vav5K_z1v_SB1tL2M5FUjmKBsNXdNlVAMUJtAjBKjvfBr_Q"




#CMD ["sh", "-c", "gfal-ls davs://xfer-intertwin.cr.cnaf.infn.it:8443/intertwin/virgo/sarandrea"]

