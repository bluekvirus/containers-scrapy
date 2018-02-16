#!/bin/bash

if [ -z "$SPIDER_NAME" ]; then
    # entery dev mode, refresh perm on mounted volume
    useradd -s /bin/bash $USER
    chown -R $USER:$USER $CRAWLER_FOLDER
    su $USER
    /bin/bash
    #use watch -n ${INTERVAL:-60} scrapy crawl <spider name> to test
else
    # entery runtime mode, run spider in mounted volume
    # (volume must be a valid Scrapy project with scrapy.cfg at its root)
    export TERM=xterm # docker run -t hack
    while true; do
        scrapy crawl $SPIDER_NAME
        sleep ${INTERVAL:-60}
    done
fi

