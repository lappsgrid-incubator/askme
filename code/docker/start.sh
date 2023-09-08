ELASTIC=elastic-1.1.0-v1.1.0.jar
QUERY=query-1.2.0-v1.2.0.jar
RANKING=ranking-1.1.0-v1.1.0.jar
WEB=web-2.1.0-v2.1.0.jar

JAVA=/usr/local/openjdk-8/bin/java

# Setting up RabbitMQ
service rabbitmq-server start
rabbitmqctl add_user askme askme-pw
rabbitmqctl add_vhost askme
rabbitmqctl set_permissions -p askme askme ".*" ".*" ".*"
# include for now the admin console
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl set_user_tags askme administrator

# Starting components
echo '\n>>>>> starting elastic component'
$JAVA -Xmx4G -jar jars/$ELASTIC &
echo '\n>>>>> starting query component'
$JAVA -Xmx4G -jar jars/$QUERY &
echo '\n>>>>> starting ranking component'
$JAVA -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=30 -XX:+UseCMSInitiatingOccupancyOnly -Xms4g -Xmx4G -jar jars/$RANKING &
echo '\n>>>>> starting web component'
$JAVA -Xmx4G -jar jars/$WEB &

# web server
echo '\n>>>>> starting the webserver'
cd git/askme-web-next
npm run start &
