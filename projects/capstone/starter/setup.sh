#!/bin/bash

# DB-URL for running app locally:
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"

# DB-URL for running app on Heroku
# export DATABASE_URL="postgres://mlikgggsavynxb:5228c44ceec20664b3604049c8c503a4259aaff120a385ebf39bd45eb954d846@ec2-54-172-219-6.compute-1.amazonaws.com:5432/dfcvrbns2bk3oe"

# Auth0 settings
export Auth0_Domain_Name='fstutorial.eu.auth0.com'
export JWT_Code_Signing_Secret='0Dy9vCeXbv5Me8xyPFQORgw2Z0rhU1lxBvWFsYO5tfi9KW0qXp-asBfFeWDEWzIU'
export Auth0_Client_ID='tFtzqtWvPqTGDzC829orycTHqvwdsLGi'

# Test bash file
export EXCITED="true"
echo "setup.sh script executed successfully!"