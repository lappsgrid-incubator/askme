"""Starting AskMe components.                                                                                                                                              
                                                                                                                                                                           
Build a string that when piped into a shell command will start AskMe components.                                                                                           
                                                                                                                                                                           
$ python3 start.py                                                                                                                                                         
$ python3 start.py (elastic|query|ranking|web)                                                                                                                             
                                                                                                                                                                           
In the second invocation only the selected component will be started. This is all                                                                                          
dependent on uploads to jars_directory.                                                                                                                                    
                                                                                                                                                                           
Typically you pipe the result into the shell command:                                                                                                                      
                                                                                                                                                                           
$ python3 start.py query                                                                                                                                                   
                                                                                                                                                                           
"""


import os, sys, string


# EDIT THESE AS NEEDED                                                                                                                                                     
jars_directory = '/media/volume/sdb/askme/jars/current'
elastic_jar = ('elastic-1.0.0-v1.0.0.jar', 'elastic-1.0.0-ac21123.jar')[1]
query_jar = ('query-1.1.0-v1.1.0.jar',)[0]
ranking_jar = ('ranking-1.0.0-v1.0.0.jar',)[0]
web_jar = ('web-2.0.0-v2.0.0.jar',)[0]


template = string.Template('''                                                                                                                                             
export JAVA=/usr/lib/jvm/java-8-openjdk-amd64/bin/java                                                                                                                     
$$JAVA -Xmx4G -jar $elastic_jar &                                                                                                                                          
$$JAVA -Xmx4G -jar $query_jar &                                                                                                                                            
$$JAVA -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=30 -XX:+UseCMSInitiatingOccupancyOnly -Xms4g -Xmx4G -jar $ranking_jar &    
$$JAVA -Xmx4G -jar $web_jar &                                                                                                                                              
''')


def build_path(jar):
    return os.path.join(jars_directory, jar)

def build_shell_script():
    return template.substitute(elastic_jar=build_path(elastic_jar),
                               query_jar=build_path(query_jar),
                               ranking_jar=build_path(ranking_jar),
                               web_jar=build_path(web_jar))


if __name__ == '__main__':

    component = sys.argv[1] if len(sys.argv) > 1 else None
    script = build_shell_script()
    for line in script.split('\n'):
        if '$JAVA' in line:
            if component is None or component in line:
                print(line)
        elif line:
            print(line)
