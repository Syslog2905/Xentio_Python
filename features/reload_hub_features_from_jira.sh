#!/bin/bash

if [ -d "behave_pro_jira" ]; then
    rm -R behave_pro_jira
fi
python get_jira_tests.py -p 11350 -a -d behave_pro_jira
