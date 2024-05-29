#/bin/bash

### run with: source ./setup.sh
###
### This script sets the environment to use oidc-agent and rucio
### - gets the necessary authentication token from EGI using oidc-agent
### - sets the environment to access the endpoint at CNAF with gfal
### - sets the environment for the intertwin rucio instance at DESY

## Get token from EGI

eval `oidc-agent`

export OIDC_ENCRYPTION_PW="intertwin"

# You will need to edit this to point to your rucio.cfg. You need to specify the ABSOLUTE PATH 

export RUCIO_CONFIG="$PWD/rucio.cfg"

# get rid of x509 authentication, will conflict with tokens
echo "Destroying voms proxy if existing"
voms-proxy-destroy
unset X509_CERT_DIR    
unset X509_USER_CERT   
unset X509_USER_KEY 

#enable debug mode
#export XRD_LOGLEVEL=Debug
