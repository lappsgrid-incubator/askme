"""find.py

Finding a term in Groovy, Java and XML files in the AskMe repositories.

"""

import os, sys

from config import eager_directory

SUBS = ('askme-core', 'askme-elastic', 'askme-nlp', 'askme-query', 'askme-ranking', 'askme-web')
SUBS = ('askme-core', 'askme-elastic', 'askme-query', 'askme-ranking', 'askme-web')

search_term = sys.argv[1]

for sub in SUBS:
    repo = os.path.join(eager_directory, sub)
    print(f'\n=== {repo}\n')
    for path, directories, files in os.walk(repo):
        # print('{} {} {}'.format(repr(path), repr(directories), repr(files)))
        for f in files:
            # if f.endswith('.groovy') or f.endswith('.java'):
            # print(os.path.splitext(f))
            if os.path.splitext(f)[-1] in ('.groovy', '.java', '.xml'): 
                full_path = os.path.join(path, f)
                short_path = full_path[len(eager_directory):]
                if f'/{sub}/target/' in full_path:
                    continue
                with open(full_path) as fh:
                    # print(full_path)
                    line_number = 0
                    for line in fh:
                        line_number += 1
                        if search_term in line:
                            print(f'{short_path}:{line_number} -- {line}')
