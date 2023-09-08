"""upload.py

Takes the four AskMe component jars from the target directory and creates a bash
script to upload them to Jetstream. To see the script:

$ python3 upload.py all|elastic|query|ranking|web SEARCH_TERM?

The search term is optional and has to be used when you have more than one jar in
the target directory of the repository. This might be a tricky thing when you are
trying to upload all components since you can use only one search term.

Typically you would pipe the result into a shell, for example:

$ python3 upload.py elastic | sh

"""

import os, sys
import config


def print_command(target_dir, jar):
    jar_path = os.path.join(target_dir, jar)
    host = config.askme_host
    upload_directory = config.upload_directory
    command = f'scp -i ~/.ssh/askme-marc {jar_path} ubuntu@{host}:{upload_directory}'
    print(command)


def upload(component, search_term):
    target_dir = os.path.join(config.eager_directory, f'askme-{component}', 'target')
    jars = [f for f in os.listdir(target_dir)
            if f.endswith('.jar') and f.startswith(component) and 'javadoc' not in f]
    if search_term is not None:
        jars = [f for f in jars if search_term in f]
    if len(jars) == 1:
        print_command(target_dir, jars[0])
    elif(jars):
        print('WARNING: you have more than one jar, try using a search term')
        for jar in jars:
            print(jar)
    else:
        print('WARNING: no jar was found')


if __name__ == '__main__':

    component = sys.argv[1]
    search_term = sys.argv[2] if len(sys.argv) > 2 else None
    if component in config.components:
        upload(component, search_term)
    elif component == 'all':
        for component in config.components:
            upload(component, search_term)
    else:
        print('Nothing to do')    
