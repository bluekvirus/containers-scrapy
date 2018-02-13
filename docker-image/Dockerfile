FROM ubuntu:xenial
MAINTAINER bluekvirus@gmail.com

# ENV (map a local folder ./ into this docker by -v $(pwd):/code, this folder should contain all of your .py crawlers)
ENV CRAWLER_FOLDER /code
ADD scrapy.cfg ${CRAWLER_FOLDER}/scrapy.cfg

# Install prerequisite
RUN apt-get update
RUN apt-get install -y --no-install-recommends python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install scrapy ipython

# Clean up APT when done
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Working dir mount
RUN mkdir -p ${CRAWLER_FOLDER}
WORKDIR ${CRAWLER_FOLDER}

# CMD (outside)
# docker run -it --rm -v $(pwd):/code

# CMD (inside)
#
# A: interactive debug using fetch(request) and response.css().extract()
# scrapy shell <url>
#
# B: run spider by file
# scrapy runspider <crawler.py> [-o items.json]
#
# C: run spider defined in Scrapy project (after startproject, genspider)
# scrapy crawl <crawler by name>

