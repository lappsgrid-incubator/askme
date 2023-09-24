# Various Docker notes

In progress...



## TODO

- Adapt the web part so it has the right datasets
	- Did this by adding a corpus named nfcorpus with the contents of the bio domain 
	- Did not seem to help
	- Must find the query that is being used
- Test the start script
	- Now I am just manually starting everything from inside the container


Trying some manual queries. First just testing whether you get something out of the index:

```
curl \
    http://elastic:9200/nfcorpus/_search?pretty \
    -H "Content-Type: application/json"
```

Now something more useful. We search for "particle" in the tile or abstract but only print the title and only return 3 results.

```
curl \
    http://elastic:9200/nfcorpus/_search?pretty \
    -H "Content-Type: application/json" \
    -d '{
          "from": 0,
          "size": 3,
          "_source": { "includes": ["title"] },
          "query": { 
              "multi_match" : {
                "query" : "particle", 
                "fields" : ["title", "abstract"]
              }
            }
        }'
```



## The components

With the current `Dockerfile` we create an image with all components but do not start them.

```bash
$ docker build -t askme:v1 .
```

Running the container:

```bash
$ docker run --rm -it -p 15672:15672 -p 3000:3000 askme:v1 bash
```

Within the container we manually run the commands in `start.sh` (this obviously needs to change, just experimenting for now till I get it right):

```
export ELASTIC=elastic-1.1.0-v1.1.0.jar
export QUERY=query-1.2.0-v1.2.0.jar
export RANKING=ranking-1.1.0-v1.1.0.jar
export WEB=web-2.1.0-v2.1.0.jar
export JAVA=/usr/local/openjdk-8/bin/java

service rabbitmq-server start
rabbitmqctl add_user askme askme-pw
rabbitmqctl add_vhost askme
rabbitmqctl set_permissions -p askme askme ".*" ".*" ".*"
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl set_user_tags askme administrator

$JAVA -Xmx4G -jar jars/$ELASTIC &
$JAVA -Xmx4G -jar jars/$QUERY &
$JAVA -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=30 -XX:+UseCMSInitiatingOccupancyOnly -Xms4g -Xmx4G -jar jars/$RANKING &
$JAVA -Xmx4G -jar jars/$WEB &

cd git/askme-web-next
npm run start &
```


## The ElasticSearch image

Use this Dockerfile:

```docker
FROM docker.elastic.co/elasticsearch/elasticsearch:7.17.13

RUN mkdir /data \
	&& chown elasticsearch /data \
	&& echo "path.data: /data" >> /usr/share/elasticsearch/config/elasticsearch.yml \
	&& echo "discovery.type: single-node" >> /usr/share/elasticsearch/config/elasticsearch.yml

CMD bin/elasticsearch
```

This also starts the database, comment out the last line if you want to experiment with starting it.

Building and running:

```bash
$ docker build -t elastic -f Dockerfile-elastic .
$ docker run -d --rm -p 9200:9200 -v /Users/Shared/data/elasticsearch/data/:/data --user elasticsearch elastic
```

If you do not start the database you would use the following for entering the container and starting the database:

```bash
$ docker run -it --rm -p 9200:9200 -v /Users/Shared/data/elasticsearch/data/:/data --user elasticsearch elastic bash
elasticsearch@55ce21a2ad80:~$ bin/elasticsearch &
```

Notice the `--user` option, ElasticSearch cannot be ran as root.


## Networking the containers

See `docker-compose.yml`.

```bash
$ docker-compose up -d
```

To use the port to ElasticSearch from the `askme_main` you use "curl elastic:9200"