# Amazon Linux Python Package Builder (alppb)
alppb builds Python packages using the same version of Amazon Linux that the AWS Lambda service uses. Using alppb helps guarantee that any PyPi package your AWS Lambda app depends on will run properly.

Why is this a problem that needs to be solved? AWS Lambda requires you to package up your Python project along with all of its dependencies in order to run. If your AWS Lambda Python project has package(s) with C extension modules (or dependencies that do), you will need to build them on Amazon Linux for your app to work. alppb uses the AWS CodeBuild service ([perpetual free tier includes 100 build minutes per month](https://aws.amazon.com/codebuild/pricing/)) to build the package(s) on Amazon Linux and download them to your local machine for you. Simply unzip the downloaded package(s) into your deployment bundle and upload to the AWS Lambda service.

# How To Use alppb

```shell
pip install alppb
alppb -h
```

Build package requests in bucket foo
`alppb requests foo`

# TODO
## Pre 1.0.0
- [X] Foundation - create a CodeBuild project with hardcoded build that puts an artifact in s3
- [X] Fix artifact so its a zip of the contents (excluding parent dir)
- [X] Download the module locally to dir alppb was run from
- [X] Move codebuild stuff to a module
- [X] Delete the artifact from s3 as part of cleanup
- [X] Add creation of IAM role for CodeBuild instead of using hardcoded, pre-built role
- [X] Add deletion of IAM role as part of cleanup
- [X] Move aws-cli stuff to boto3
- [X] Allow user specification of the desired module to be built using alppb
- [X] Cleanup existing docstrings
- [X] Remove base64 stuff in iam.py as it obscures whats happening
- [X] Axe the examples dir
- [X] Allow user specification of the bucket
## 1.0.0
- [ ] Exception handling
    - [X] Update and overwrite if resources already exist
    - [X] pre-req checking
    - [ ] Valid PyPi package
    - [X] Bucket and CodeBuild need to be in same region
    - [ ] Bucket exists (NoSuchBucket)
- [ ] Unit tests
- [ ] Integration tests
- [x] Package and Submit to PyPi
- [ ] Dockerize and submit to Dockerhub
- [x] Make CodeBuild Docker image details more clear and document
- [ ] Add verbosity levels
- [ ] Add Sphinx docs
## Planned
- [ ] One or more modules can be specified in one invocation of alppb
- [ ] Allow specification of a requirements.txt file to use as a list of all modules to build
- [ ] Specify download location of the artifact
- [ ] Create an s3 bucket when an arg is specified
- [ ] Allow user to optionally specify an IAM role
- [ ] Specify the Python version that should be used to build the package (choices come from supported AWS Lambda versions)

# FAQs
1) Why AWS CodeBuild? Why not X instead?

AWS CodeBuild has a perpetual free tier and it's super easy to spin up, and teardown, a build job. Further, we can easily specify various Docker images to use for the build that match the AWS Lambda environment. I will likely add support for other build methods/services. If you have a suggestion, please open an issue or contact me on Twitter [@irlrobot](https://twitter.com/irlrobot).

2) What image is being used for CodeBuild? Can I inspect the image being used for the build?

There are three images, one for each version of Python supported by AWS Lambda:
* Python 2.7 - https://hub.docker.com/r/irlrobot/alppb-python27/
    * Dockerfile: https://github.com/irlrobot/dockerfiles/tree/master/alppb-python27
* Python 3.6 - https://hub.docker.com/r/irlrobot/alppb-python36/
    * Dockerfile: https://github.com/irlrobot/dockerfiles/tree/master/alppb-python36
* Python 3.7 - https://hub.docker.com/r/irlrobot/alppb-python37/
    * Dockerfile: https://github.com/irlrobot/dockerfiles/tree/master/alppb-python37

Each image is running Amazon Linux 1 version 2017.03.1.20170812 which is [what AWS Lambda uses](https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html).
