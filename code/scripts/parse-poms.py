"""Simplistic dependecy parser for POM files

Displays dependencies from a couple of POM files used in AskMe:

- org.lappsgrid.maven.parent-pom
- org.lappsgrid.maven.groovy-parent-pom
- org.lappsgrid.askme.elastic
- org.lappsgrid.askme.query
- org.lappsgrid.askme.ranking
- org.lappsgrid.askme.web

"""

import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import config


def parse_pom(pom_file: str):
	pom_name = os.path.split(os.path.split(pom_file)[-2])[-1]
	print(f'\n=== {pom_name}')
	tree = ET.parse(pom_file)
	properties = {}
	dependencies = []
	project = tree.getroot()
	for child in project:
		tag = get_tag(child)
		if tag == 'properties':
			props = parse_properties(child, properties)
			#print(properties)
		elif tag == 'dependencies':
			dependencies = parse_dependencies(child, dependencies, properties)
		elif tag == 'dependencyManagement':
			dependencies = parse_dependencies(child[0], dependencies, properties)

def parse_properties(properties: Element, properties_dict: dict):
	for property in properties:
		tag = get_tag(property)
		properties_dict[tag] = property.text

def parse_dependencies(dependencies: Element, dependencies_list: list, properties: dict):
	print('\ndependencies')
	for dependency in dependencies:
		groupId = find_tag(dependency, 'groupId').text
		artifactId = find_tag(dependency, 'artifactId').text
		version = find_tag(dependency, 'version')
		version = get_version(version, properties)
		print(f'    {groupId:30} {artifactId:40} {version}')

def get_tag(element: Element):
	# this is because the tag looks like "{http://maven.apache.org/POM/4.0.0}properties" 
	return element.tag.split('}')[-1]

def find_tag(element: Element, tagname: str):
	# again to deal with the prefix
	prefix = "{http://maven.apache.org/POM/4.0.0}"
	tag = f'{prefix}{tagname}'
	return element.find(tag)

def get_version(version: Element, properties: dict):
	if version is None:
		return 'nil'
	elif version.text.startswith('$'):
		version = version.text[2:-1]
		return properties.get(version, version)
	else:
		return version.text.strip()


if __name__ == '__main__':

	for parent_pom in config.parent_poms:
		parse_pom(parent_pom)
	parse_pom(os.path.join(config.eager_directory, 'org.lappsgrid.rabbitmq', 'pom.xml'))
	parse_pom(os.path.join(config.eager_directory, 'askme-core', 'pom.xml'))
	for component in config.components:
		parse_pom(os.path.join(config.eager_directory, f'askme-{component}', 'pom.xml'))
