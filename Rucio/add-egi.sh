#/bin/bash

### run with: ./add-egi.sh
###
### This script 
### - setup the necessary oidc identity to get the authorization token from EGI using oidc-agent


source ./setup.sh

echo "Adding identity egi ... "
echo "Please follow instructions"

# Identity egi added with:
oidc-gen --pub --issuer https://aai-demo.egi.eu/auth/realms/egi --scope=max --pw-env --flow=device egi

# Use encryption password "intertwin" !!!!

