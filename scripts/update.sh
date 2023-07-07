# update.sh
#
# usage:
#
# $ sh update elastic 1.1.0-SNAPSHOT-v1.0.0-7-gbb380a1-dirty
# $ sh update core elastic 1.1.0-SNAPSHOT-v1.0.0-7-gbb380a1-dirty
#
# Speficy the component and the version of the component, the latter requires you 
# to know what version will be created by "mvn package" which you can determine
# by looking at the previous version built and the current commit.
#
# The first case does not install askme-core, use the second if you made some
# changes that you want to be used by the component.

repos=/Users/marc/Desktop/projects/lapps/code/eager
if [ ! -d "$repos" ]; then
	repos=/Users/marc/Documents/git/lapps/incubator/askme
fi

if [ "$1" == 'core' ]; then
	core=1
	component=$2
	version=$3
else
	core=0
	component=$1
	version=$2
fi


jarfile="target/$component-$version.jar"
remotedir=ubuntu@149.165.173.91:/media/volume/sdb/askme/jars/current

current=`pwd`

if [ "$core" == 1 ]; then
	cd ${repos}/askme-core
	echo '========================================================================='
	pwd
	echo "$ mvn install"
	echo '========================================================================='
	mvn install
	pwd
	ls -al target
fi;

cd ${repos}/askme-$component
echo '========================================================================='
pwd
echo "$ mvn package"
echo '========================================================================='
mvn package
ls -al target

echo '========================================================================='
pwd
echo "$ scp -i ~/.ssh/askme-marc \\"
echo "      $jarfile \\"
echo "      $remotedir"
echo '========================================================================='
scp -i ~/.ssh/askme-marc $jarfile $remotedir
