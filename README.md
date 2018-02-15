# containers-scrapy
Scrapy with Python 3 in a docker env, ready to deploy in any dev machine.

## Commands

### Outside of container
```
docker run -it --rm -v $(pwd):/code -e USER=<your user on host> bluekvirus/scrapy
```

### Inside of container

### A: interactive debug using fetch(request) and response.css().extract()
```
scrapy shell <url>
```

### B: run spider by file
```
scrapy runspider <crawler.py> [-o items.json]
```

### C: run spider defined in current Scrapy project **crawlers** (after startproject, genspider)
```
scrapy crawl <crawler by name>
```