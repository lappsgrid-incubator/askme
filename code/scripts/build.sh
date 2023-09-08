# build.sh
#
# Build the four AskMe components.
#
# Assumes that the needed askme-core version is installed.


divider="================================================================================="

export eager_directory=/Users/marc/Desktop/projects/lapps/code/eager
#export eager_directory=/Users/marc/Documents/git/lapps/incubator/askme

build()
{
    cd $eager_directory/askme-$1
    echo
    echo $divider
    echo "Building `pwd`"
    echo $divider
    mvn package
}

if [[ "$1" =~ ^(elastic|query|ranking|web)$ ]]; then
    build $1
else
    for component in elastic query ranking web;
    do
        build $component
    done
fi
