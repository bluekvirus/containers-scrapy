# containers-scrapy
Scrapy with Python 3 in a docker env, ready to deploy in any dev machine or runtime node.

## Commands

### Outside of container

#### A: development mode
```
docker run -it --rm \
    -v $(pwd):/code \
    -e USER=<your user on host> \
    bluekvirus/scrapy
```

#### B: runtime mode
```
docker run -d --rm \ 
    -v $(pwd):/code \
    -e SPIDER_NAME=<the spider name> \
    -e INTERVAL=[the repeat interval, default 60s] \
    --log-opt max-size=5m \
    --log-opt max-file=1 \
    bluekvirus/scrapy
```
Note that the spider/pipeline might require futher environment vars to operate, be sure to provide them with additional `-e` ! (e.g SLACK_WEBHOOK and REPORT_RATIO_THRESHOLD in nv-gpu-nowinstock spider's pipeline)

Real runtime cmd example
```
sudo docker run -d --log-opt max-size=5m --log-opt max-file=1 -v $(pwd):/code -e SPIDER_NAME=nv-gpu-nowinstock -e SLACK_WEBHOOK=https://hooks.slack.com/services/.../.../y0D46F4443McqHW8PRjUitNS -e REPORT_RATIO_THRESHOLD=1.35 bluekvirus/scrapy
```

We do not have repository branching support at the moment, cloned Scrapy repository will always use *master* by default.

### Inside of container (dev mode only)

#### A: interactive debug using fetch(request) and response.css().extract()
```
scrapy shell <url>
```

#### B: run spider by file
```
scrapy runspider <crawler.py> [-o items.json]
```

#### C: run spider defined in current Scrapy project **crawlers** (after startproject, genspider)
```
scrapy crawl <crawler by name>
```