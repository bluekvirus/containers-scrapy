#!/bin/bash

useradd -s /bin/false $USER
chown -R $USER:$USER $CRAWLER_FOLDER

/bin/bash
