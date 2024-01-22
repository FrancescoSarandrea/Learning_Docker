FROM python:3.8


RUN pip3 install rucio-clients


FROM fedora:latest


#RUN yum install -y gfal2-all
RUN dnf -y install python3-gfal2 gfal2-plugin-file gfal2-plugin-gridftp gfal2-plugin-http gfal2-plugin-srm gfal2-plugin-xrootd xrootd-client gfal2-util

WORKDIR /app

# Copy the token file to the working directory inside the container
COPY token.txt /app/


# Copy the file to the working directory inside the container
COPY clarabella.txt /app/

ENV BEARER_TOKEN= "your_token"



# Run gfal-copy to copy the file and gfal-ls to list the files
CMD ["sh", "-c", "gfal-copy clarabella.txt davs://xfer-intertwin.cr.cnaf.infn.it:8443/intertwin/virgo/sarandrea && gfal-ls davs://xfer-intertwin.cr.cnaf.infn.it:8443/intertwin/virgo/sarandrea"]


