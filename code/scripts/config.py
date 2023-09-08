"""config.py

Configurstion settings for utility scripts.

Written for one particular setup for one person.

TODO: generalize this.

"""

from utils import get_sources_dir

components = ('elastic', 'query', 'ranking', 'web')

source_dirs = (
	'/Users/marc/Desktop/projects/lapps/code/eager',
	'/Users/marc/Documents/git/lapps/incubator/askme')

askme_host = '149.165.173.91'
askme_host = '149.165.155.140'

upload_directory = '/media/volume/sdb/askme/jars/current'
upload_directory = '/home/ubuntu/askme/jars'

eager_directory = get_sources_dir(source_dirs)

parent_poms = (
	'/Users/marc/Desktop/projects/lapps/code/lapps/org.lappsgrid.maven.parent-pom/pom.xml',
	'/Users/marc/Desktop/projects/lapps/code/lapps/org.lappsgrid.maven.groovy-parent-pom/pom.xml')

parent_poms = (
	'/Users/marc/Documents/git/lapps/lapps/org.lappsgrid.maven.parent-pom/pom.xml',
	'/Users/marc/Documents/git/lapps/lapps/org.lappsgrid.maven.groovy-parent-pom/pom.xml')
