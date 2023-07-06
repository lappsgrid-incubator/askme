# Installing AskMe for xDD

This assumes access to an ElasticSearch database from the instance that AskMe runs on. AskMe has been tested on Ubuntu 22.04. AskMe consists of four jar files, a Javascitp front-end and a RabbitMQ server, which all run on teh same box. We typically run AskMe as the `ubuntu` user and the notes below assume that.

## Software requirements:

- Java 8
- npm
- Maven
- RabbitMQ

All jars used by AskMe were compiled with Java 8. They may run on Java 11, but that has not been tested.

Installing Java, Maven and npm on Ubuntu:

```bash
$ sudo apt-get install openjdk-8-jdk -y
$ sudo apt install npm
$ sudo apt install maven
```

Java 8 is installed in `/usr/lib/jvm/java-8-openjdk-amd64/`. The version of Maven that was installed is 3.6.3, which use Java 11 by default (use `mvn -version` to check this). To use Java 8 do

```bash
$ export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```

The npm install is needed to install Node.js, of which a recent version is required. On various webpages there are some musings on how apt-get is not so great for dealing with Node.js and to use nvm at [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm). I followed the instructions there:

```bash
$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
$ export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" 
   [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

The former does also add the latter to `/home/ubuntu/.bashrc`. And at that point you can finally install a more recent version of Node.js:

```bash
$ nvm install 20.2.0
$ node -v
v20.2.0
```

Installing RabbitMQ:

```bash
$ sudo apt install rabbitmq-server
$ service rabbitmq-server status
```

Setting up RabbitMQ:

```bash
$ sudo rabbitmqctl add_user askme askme-pw
$ sudo rabbitmqctl add_vhost askme
$ sudo rabbitmqctl set_permissions -p askme askme ".*" ".*" ".*"
```

## Setting up the instance

You need a directory `/usr/local/eager`, owned by ubuntu.

```bash
$ sudo mkdir /usr/local/eager
$ sudo chown ubuntu /usr/local/eager
```

The ubuntu user also needs to be able to write files `/tmp/askme-*.json`, this can go wrong if you ran AskMe under another user and those files already exist.

There needs to be a file `/etc/lapps/askme.ini`, readable by ubuntu.

```bash
$ sudo mkdir /etc/lapps
$ sudo emacs /etc/lapps/askme.ini
```

Contents for that file are as follows:

```
RABBIT_USERNAME=askme
RABBIT_PASSWORD=askme-pw
RABBIT_HOST=10.0.142.197/askme
RABBIT_EXCHANGE=askme-ex
ELASTIC_HOST=149.165.154.73
ELASTIC_PORT=9200
```

The RABBIT_HOST AND ELASTIC_HOST IP addresses need to be changed to reflect local reality.


## Getting the AskMe code

Several repositories are required for AskMe to work:

- [https://github.com/lapps/org.lappsgrid.maven.parent-pom](https://github.com/lapps/org.lappsgrid.maven.parent-pom)
- [https://github.com/lapps/org.lappsgrid.maven.groovy-parent-pom](https://github.com/lapps/org.lappsgrid.maven.groovy-parent-pom)
- [https://github.com/lappsgrid-incubator/org.lappsgrid.rabbitmq](https://github.com/lappsgrid-incubator/org.lappsgrid.rabbitmq)
- [https://github.com/lappsgrid-incubator/askme-core](https://github.com/lappsgrid-incubator/askme-core)

These all need to be install with Maven, in the order listed above (assuming all repositories were cloned into the same directory, also assuming the main branch is checked out):

```bash
$ cd org.lappsgrid.maven.parent-pom
$ mvn install
$ cd org.lappsgrid.maven.groovy-parent-pom
$ mvn install
$ cd org.lappsgrid.rabbitmq
$ mvn install
$ cd askme-core
$ mvn install
```

The four core AskMe packages are:

- [https://github.com/lappsgrid-incubator/askme-elastic](https://github.com/lappsgrid-incubator/askme-elastic)
- [https://github.com/lappsgrid-incubator/askme-query](https://github.com/lappsgrid-incubator/askme-query)
- [https://github.com/lappsgrid-incubator/askme-ranking](https://github.com/lappsgrid-incubator/askme-ranking)
- [https://github.com/lappsgrid-incubator/askme-web](https://github.com/lappsgrid-incubator/askme-web)

We again use the main branch for all, except for askme-elastic, for which we check out the xdd branch. These repositories depend on the installations above and for all these you need to create the package

```bash
$ mvn package
```

Then copy/ftp the jar files to the instance where you want to install AskMe.

> Note: soon there will be a link to docloadable packages, this will make getting the code much easier. This does however rely on having tested the xdd branch of askme-elastic.

Finally we need the web front-end:

- [https://github.com/lappsgrid-incubator/askme-web-next](https://github.com/lappsgrid-incubator/askme-web-next)


## Starting AskMe

With the current versions on the main branch we would have created the following jars when running `mvn package`:

```
elastic-1.1.0-v1.1.0-1-g58ab523.jar
query-1.2.0-v1.2.0.jar
ranking-1.1.0-v1.1.0.jar
web-2.1.0-v2.1.0.jar
```

To start these jars do

```bash
export JAVA=/usr/lib/jvm/java-8-openjdk-amd64/bin/java
$JAVA -Xmx4G -jar elastic-1.1.0-v1.1.0-1-g58ab523.jar &
$JAVA -Xmx4G -jar query-1.2.0-v1.2.0.jar &
$JAVA -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=30 -XX:+UseCMSInitiatingOccupancyOnly -Xms4g -Xmx4G -jar ranking-1.1.0-v1.1.0.jar &
$JAVA -Xmx4G -jar web-2.1.0-v2.1.0.jar &
```

Due to a bug in the database code the databse needs to be flushed when restarting the web jar:

```bash
$ rm -rf /usr/local/eager/db
```

To start the web page you change directories into askme-web-next. The following three steps only need to be done once:

1. Create `.env.local` in root and add in route to API (see `.env.local.example` for example environment variables file, typically you can just copy that file).
2. Run `$ npm install` to install packages
3. Run `$ npm run build` to build the page

To start the page do

```bash
$ npm run start &
```

Access the page at port 3000 of local host (or use a public IP address.

To stop first get the process id:

```bash
$ ps g | grep start
3124492 pts/4    Sl     0:00 npm run start
3124503 pts/4    S      0:00 sh -c next start
3124504 pts/4    Sl     0:00 node /home/ubuntu/askme/git/askme-web-next/node_modules/.bin/next start
3124714 pts/4    S+     0:00 grep --color=auto start
```

Then kill the node process.
