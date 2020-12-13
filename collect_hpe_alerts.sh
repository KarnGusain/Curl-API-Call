#!/bin/bash
#########################################################################################################################
### Title: collect_hpe_alerts.sh                                                                                      ###
### Version: 01                                                                                                       ###
### Published : 13th December 2020                                                                                    ###
### Author : Karn Kumar (karn.itguy@gmail.com)                                                                        ###
#########################################################################################################################

# currentVersion=$(curl -k -H "accept: application/json"  -X GET https://synergy.udalt.mycom.com/rest/version |jq -r ".currentVersion")

# Set the timestamp for file based on the TIMESTAMP1 and TIMESTAMP2
TIMESTAMP1=$(date "+%Y-%m-%d")
TIMESTAMP2=$(date "+%H:%M:%S")

# Set the Destination file Variable
OUTFILE=(/home/nxf59093/script_logs/hpeCriticalAlert.${TIMESTAMP1}.csv)

# Get the Session ID in order to use during GET connection request
sessionID=$(curl -k -H "accept: application/json" -H "content-type: application/json" -H "x-api-version: 120" -d '{"userName":"administrator","password":"myPassword"}' -X POST https://synergy.nxdi.nxp.com/rest/login-sessions | jq -r ".sessionID")

# cUrl command with header and payload information to ftech the Data using API call
CMD=$(curl -k -H 'accept: application/json' \
        -H 'content-type: text/csv' \
        -H 'x-api-version: 2' \
        -H "auth: $sessionID" \
        -X GET https://synergy.udalt.mycom.com/rest/resource-alerts)

if [ -f "$OUTFILE" ]; then
  mv "${OUTFILE}" "${OUTFILE}-${TIMESTAMP2}.log"
  # Just to take the command output & redirect to OUTFILE
echo "${CMD}"  > "${OUTFILE}"
fi
