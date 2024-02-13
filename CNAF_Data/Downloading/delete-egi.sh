#/bin/bash

### run with: ./delete-egi.sh
###
### This script 
### - deletes the egi oidc identity 


source ./setup.sh


echo "Delete identity egi ... "
echo "Please follow instructions"

# Identity egi added with:
oidc-gen --delete --scope=max --pw-env egi
# Use encryption password "intertwin" !!!!

