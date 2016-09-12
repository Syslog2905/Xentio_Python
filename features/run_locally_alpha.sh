#!/bin/bash

TARGET_SERVER="https://alpha-hub.dev.blippar.com"
HUB_API_URL="https://alpha-api.dev.blippar.com"
BAKE_API_URL="https://bake-env.dev.blippar.com"
RECO_URL="https://reco.dev.blippar.com"
STATS_API_URL="https://stats.dev.blippar.com"
ADS_API="https://ads.dev.blippar.com"
ACCOUNTS_URL="https://alpha-accounts.dev.blippar.com"
TRANSCODER_API="http://mediacoder.dev.blippar.com"

echo "Running" $1 "tagged scenarios. Test type: " $2

behave $EXEC_FEATURES \
-D test_type=$2 \
-D browser_name="local" \
-D target_env=$TARGET_SERVER \
-D hub_api_url=$HUB_API_URL \
-D bake_api_url=$BAKE_API_URL \
-D stats_api_url=$STATS_API_URL \
-D reco_url=$RECO_URL \
-D ads_api=$ADS_API \
-D accounts_url=$ACCOUNTS_URL \
-D wait_between_tests="2" \
-D browser_version="" \
--tags "~@AUTOMATABLE" \
--tags "~@DISABLED" \
--tags $1 \
--no-skipped \
--junit