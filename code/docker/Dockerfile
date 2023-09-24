FROM openjdk:8-jdk

# We need git, wget and rabbitmq. In the future we may want to add Maven so we can
# build straight from Git repositories. The tree command is there for debugging
# convenience only. 
RUN apt-get update && apt-get install -y \
  git \
  rabbitmq-server \
  tree \
  wget \
  && rm -rf /var/lib/apt/lists/*

# Sepearating out Node Js and npm (Javascript Node Package Manager) because those have
# been a bit tricky. This is based on downloading https://deb.nodesource.com/setup_20.x 
# and then editing the download a bit to remove spurious deprecation warnings. The result
# of that is in code/docker/install-nodejs.sh.
# NOTE: we may strip this and have a separate container for the website, based on an
# official published node image (https://hub.docker.com/_/node/).
COPY ./install-nodejs.sh ./
RUN bash install-nodejs.sh
RUN apt-get install nodejs -y

# Creating the needed directories
RUN mkdir /home/askme /home/askme/jars /home/askme/git /usr/local/eager /etc/lapps

WORKDIR /home/askme

# These should be updated for newer versions. Probably get these from the environment.
ARG ELASTIC=elastic-1.1.0-v1.1.0.jar
ARG QUERY=query-1.2.0-v1.2.0.jar
ARG RANKING=ranking-1.1.0-v1.1.0.jar
ARG WEB=web-2.1.0-v2.1.0.jar

# Getting the AskMe component jars and web interface code
RUN wget https://www.cs.brandeis.edu/~marc/downloads/askme/jars/$ELASTIC \
	&& wget https://www.cs.brandeis.edu/~marc/downloads/askme/jars/$QUERY \
	&& wget https://www.cs.brandeis.edu/~marc/downloads/askme/jars/$RANKING \
	&& wget https://www.cs.brandeis.edu/~marc/downloads/askme/jars/$WEB \
	&& git clone https://github.com/lappsgrid-incubator/askme-web-next \
	&& mv *.jar jars \
	&& mv askme-web-next git

# Building the web server
RUN cd git/askme-web-next \
	&& cp .env.local.example .env.local \
	&& npm install \
	&& npm run build

# Uploading initialization file, startup file and some extra aliases
COPY ./alias.sh ./askme.ini ./start.sh ./
RUN cp askme.ini /etc/lapps \
	&& cat alias.sh >> /root/.bashrc

# Starting AskMe
# TODO: still testing the startup script
# CMD ["/home/askme/start.sh"]
