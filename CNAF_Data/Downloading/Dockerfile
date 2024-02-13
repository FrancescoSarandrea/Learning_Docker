# has installed oidc client
FROM docker.io/dvrbanec/rucio-client:latest   
#FROM docker.io/rucio/rucio-clients:release-33.0.0 # cannot install oidc client on rootless docker

USER root

#install necessary packages

# install gfal
RUN yum install -y python3-gfal2 gfal2-plugin-file gfal2-plugin-gridftp gfal2-plugin-http gfal2-plugin-srm gfal2-plugin-xrootd xrootd-client gfal2-util

# install voms-proxy
RUN yum install -y voms-clients

# install CA files
COPY ./egi-trustanchors.repo /etc/yum.repos.d/egi-trustanchors.repo
RUN yum install -y ca-policy-egi-core

# install oidc-agent
COPY ./data-kit-edu-rockylinux9.repo /etc/yum.repos.d/data-kit-edu-rockylinux9.repo
RUN yum install -y oidc-agent oidc-agent-cli


# add files
COPY ./get-token.sh /root/get-token.sh
COPY ./add-egi.sh /root/add-egi.sh
COPY ./refresh-egi.sh /root/refresh-egi.sh
COPY ./delete-egi.sh /root/delete-egi.sh
COPY ./setup.sh /root/setup.sh
COPY ./rucio.cfg /root/rucio.cfg

COPY ./virgo.voms /root/virgo.voms
COPY ./setup_virgo_proxy.sh /root/setup_virgo_proxy.sh
COPY ./cronfile /root/cronfile

#COPY ./usercert.pem /root/.globus/usercert.pem
#COPY ./userkey.pem /root/.globus/userkey.pem

COPY ./usercert.pem /root/.globus/usercert.pem
COPY ./userkey.pem /root/.globus/userkey.pem

#COPY ./cert-csr.pem /root/cert-csr.pem
#COPY ./cert-key.pem /root/cert-key.pem

#copy scripts used to download V1-SL files
COPY ./gspy_O3a_Scattered_Light_V1.csv /root/gspy_O3a_Scattered_Light_V1.csv 
COPY ./O3_raw_CNAF.txt /root/O3_raw_CNAF.txt
COPY ./download-cnaf-FS3.py /root/download-cnaf-FS3.py
COPY ./gfal-commands.sh /root/gfal-commands.sh

ENV OIDC_SOCK=/tmp/oidc-forward
ENV RUCIO_CONFIG=/root/rucio.cfg
ENV OIDC_ENCRYPTION_PW=intertwin

WORKDIR /root/
RUN oidc-agent --version
RUN ./add-egi.sh

#install Python and other dependencies

RUN dnf install -y python3 python3-pip && \
	dnf clean all


#RUN apt update && \
#    apt install -y python3 python3-pip 
#&& \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*


#install additional Python packages
RUN pip3 install --no-cache-dir gwpy pandas dask

# Install necessary system dependencies
#RUN dnf install -y gcc python3-devel libtool-ltdl-devel libffi-devel openssl-devel lalsuite-python3


# Install lalsuite and lalframe
#RUN dnf install -y lalsuite-python3

RUN pip3 install lalsuite

# Install Vim
RUN dnf install -y vim && \
    dnf clean all

#create directory where to save the h5 files
RUN mkdir glitches

CMD ["cron", "-f"]
