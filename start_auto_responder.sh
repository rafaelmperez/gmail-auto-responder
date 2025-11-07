#!/bin/bash
cd /home/rafaelmp/gmail-auto-responder
source venv/bin/activate
/usr/bin/python3 gmail_auto_responder.py >> /home/rafaelmp/gmail-auto-responder/auto_responder.log 2>&1
