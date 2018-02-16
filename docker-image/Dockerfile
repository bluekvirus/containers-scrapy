FROM ubuntu:xenial
MAINTAINER bluekvirus@gmail.com

# Install prerequisite
RUN apt-get update
# Scrapy and IPython system deps
RUN apt-get install -y --no-install-recommends gcc libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
# We want both under Python 3.5+ instead of 2.7
RUN apt-get install -y --no-install-recommends python3 python3-dev python3-pip git
# Pip deps's deps during install
RUN pip3 install -U setuptools wheel
# Finally the real thing needed
RUN pip3 install -U ipython scrapy requests

# Clean up APT when done
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ENV (map a local folder ./ into this docker by -v $(pwd):/code -e USER=<user>, this folder should contain all of your .py crawlers)
ENV CRAWLER_FOLDER /code
ENV USER tim

# Working dir mount
RUN mkdir -p ${CRAWLER_FOLDER}
WORKDIR ${CRAWLER_FOLDER}

# Entrypoint 
ADD init.sh /init.sh
ENTRYPOINT [ "/init.sh" ]

# CMD (outside)
# 
# A: dev mode
# docker run -it --rm -v $(pwd):/code -e USER=<your user on host OS, default is tim> bluekvirus/scrapy
#
# B: runtime mode
# docker run -d --rm -v $(pwd):/code -e SPIDER_NAME=<the spider name> -e INTERVAL=[the repeat interval, default 60s] bluekvirus/scrapy
# 
# Note that the spider/pipeline might require futher environment vars to operate, 
# be sure to provide them in addition with `-e` ! (e.g SLACK_WEBHOOK and REPORT_RATIO_THRESHOLD)

# CMD (inside)
#
# A: interactive debug using fetch(request) and response.css().extract()
# scrapy shell <url>
#
# B: run spider by file
# scrapy runspider <crawler.py> [-o items.json]
#
# C: run spider defined in current Scrapy project (after startproject, genspider)
# scrapy crawl <crawler by name>

