#!/bin/bash

useradd -s /bin/bash $USER
chown -R $USER:$USER $CRAWLER_FOLDER

su $USER
/bin/bash
