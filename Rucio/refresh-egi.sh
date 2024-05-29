#/bin/bash

### run with: ./refresh-egi.sh
###
### This script 
### - refreshes the token for the egi identity 


source ./setup.sh


echo "Refreshing token for egi ... "
echo "Please follow instructions"

oidc-gen --reauthenticate --pw-env --flow=device egi
# Use encryption password "intertwin" !!!!

