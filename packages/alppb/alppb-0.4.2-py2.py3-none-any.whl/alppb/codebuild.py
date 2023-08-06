"""
Administration of AWS CodeBuild Resources through a boto3 client.
"""
import time
import yaml


def determine_image(py_version):
    """
    Determines which Docker image to use for CodeBuild based on the Python
    version being used on AWS Lambda.

    Parameters
    ----------
    py_version : str
        Python version being used. Must be one of "2.7", "3.6", or "3.7"

    Returns
    -------
    str
        URI of the Docker image.
    """
    if py_version == "2.7":
        return "irlrobot/alppb-python27"
    if py_version == ("3.6" or "None"):
        return "irlrobot/alppb-python36"
    if py_version == "3.7":
        return "irlrobot/alppb-python37"

    # We should never get here, but fallback to Python 3.6.
    return "irlrobot/alppb-python36"


def pip_to_use(py_version):
    """
    Determines which pip command to use for CodeBuild based on the Python
    version being used on AWS Lambda.

    Parameters
    ----------
    py_version : str
        Python version being used. Must be one of "2.7", "3.6", or "3.7"

    Returns
    -------
    str
        Pip command that should be used.
    """
    if py_version == "2.7":
        return "pip-2.7"
    if py_version == ("3.6" or "None"):
        return "pip-3.6"
    if py_version == "3.7":
        return "pip3.7"

    # We should never get here, but fallback to pip-3.6.
    return "pip-3.6"


def generate_buildspec(package, py_version):
    """
    Creates a valid Buildspec, from a template, for an AWS CodeBuild project.
    The template requires a valid PyPi package to be specified.

    Parameters
    ----------
    package : str
        Name of the PyPi package to be built by AWS CodeBuild.

    py_version: str
        Python version being used. Must be one of "2.7", "3.6", or "3.7"

    Returns
    -------
    str
        The Buildspec in YAML.
    """
    return yaml.dump({
        "version": 0.2,
        "phases": {
            "build": {
                "commands": [
                    "{} install {} -t alppb".format(pip_to_use(py_version),
                                                    package),
                    "cd alppb/",
                    "zip -r ../alppb.zip *"
                ]
            }
        },
        "artifacts": {
            "files": [
                "alppb.zip"
            ]
        }
    })


def create_build_project(client, role, bucket, buildspec, image):
    """
    Creates a new AWS CodeBuild Project to build the PyPi package(s).

    Parameters
    ----------
    client : botocore.client.S3
        A boto3 client for S3.
    role : str
        Name of the IAM Role the AWS CodeBuild project should use.
    bucket : str
        Name of the bucket the build artifact will be put in.
    buildspec : str
        A valid AWS CodeBuild Buildspec in YAML. Use s3.generate_buildspec().
    image : str
        The Docker image to use for the CodeBuild project.

    Returns
    -------
    dict
        boto3 response object. See https://boto3.amazonaws.com/v1/documentation
        /api/latest/reference/services
        /codebuild.html#CodeBuild.Client.create_project for more information.
    """
    print("Creating CodeBuild project...")
    try:
        response = client.create_project(
            name='alppbBuilder',
            source={
                'type': 'NO_SOURCE',
                'buildspec': buildspec,
            },
            artifacts={
                'type': 'S3',
                'location': bucket,
            },
            environment={
                'type': 'LINUX_CONTAINER',
                'image': image,
                'computeType': 'BUILD_GENERAL1_SMALL',
            },
            serviceRole=role,
        )
    except client.exceptions.ResourceAlreadyExistsException:
        print(">>alppbBuilder project already exists, overwriting...")
        response = client.update_project(
            name='alppbBuilder',
            source={
                'type': 'NO_SOURCE',
                'buildspec': buildspec,
            },
            artifacts={
                'type': 'S3',
                'location': bucket,
            },
            environment={
                'type': 'LINUX_CONTAINER',
                'image': image,
                'computeType': 'BUILD_GENERAL1_SMALL',
            },
            serviceRole=role,
        )

    return response


def delete_build_project(client):
    """
    Deletes the alppb AWS CodeBuild project.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    Returns
    -------
    """
    print("Deleting CodeBuild project...")
    client.delete_project(name="alppbBuilder")


def wait_for_build_to_complete(client, build_id):
    """
    Keeps checking until a build completes.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    build_id : str
        The ID of the AWS CodeBuild job to poll.

    Returns
    -------
    """
    response = client.batch_get_builds(ids=[build_id])
    # batch_get_builds() will return an array with one element.
    status = str(response.get('builds')[0].get('buildStatus'))
    if status == 'SUCCEEDED':
        print("Build completed...")
        return
    elif status == 'IN_PROGRESS':
        print(">>Build {}, waiting 10 seconds...".format(status))
        time.sleep(10)
        # Recursively call until the build is done.
        return wait_for_build_to_complete(client, build_id)
    else:
        print("ERROR: Build did not complete, status is: {}. Check "
              "the AWS console for more information on {}".format(
                  status, build_id
              ))
        exit(1)


def build_artifact(client):
    """
    Start a build and wait until it's done.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    Returns
    -------
    """
    print("Submitting a build job for the specified package(s)...")
    response = client.start_build(projectName='alppbBuilder')
    build_id = str(response.get('build').get('id'))
    print(">>Build ID is {}".format(build_id))
    wait_for_build_to_complete(client, build_id)
