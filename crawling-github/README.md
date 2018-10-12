# Crawling GitHub

This example shows a simple GitHub crawler which can be used to collect data about repositories and users. In this way, it can be used to perform analysis about the developers' network.

## Install

To use this application clone this repository.
```
git clone https://github.com/lab-csx-ufmg/webmedia2018.git

cd crawling-github
```

We recommend using a python virtual environment. After creating python virtual environment, activate the virtual environment and install the required packages.

```
# create virtual environment
python3 -m venv env

# activate enviroment
source ./env/bin/activate

# install required packages
pip install -e .
```

## Execute crawler
```
GIT_USER=<git_user> GIT_TOKEN=<git_token> python crawler/simple_bfs_crawler.py <output_file> <depth>
```
