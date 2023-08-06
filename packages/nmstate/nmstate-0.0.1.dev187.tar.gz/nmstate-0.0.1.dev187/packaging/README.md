# Distribute and Install nmstate
The packaging and distribution of nmstate is currently implemented through
PyPI and Docker images.

First prepare and upload to PyPI and then build and upload the docker image.
 

## Package and Upload to PyPI
The following procedures can be reviewed in detail [here](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives).
```
cd <project-path>
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Build a new container image and push to the docker hub

- CentOS 7:
```
cd <project-path/packaging>
sudo docker build --rm -t local/centos7-nmstate .
docker tag local/centos7-nmstate-dev nmstate/centos7-nmstate:<ver>
docker tag local/centos7-nmstate-dev nmstate/centos7-nmstate:latest
docker push nmstate/centos7-nmstate:<ver>
docker push nmstate/centos7-nmstate:latest
```
