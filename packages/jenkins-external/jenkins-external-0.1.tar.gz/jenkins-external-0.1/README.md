# `jenkins-external`

`jenkins-external` is a Python script that spawns a command, records
its output and exit code, and then logs this information to Jenkins
in an external job.

Currently, SSH is the only supported method to send output to Jenkins.
Therefore, you must go to *Configure Global Security* → SSH Server, and
enable the SSH server on a fixed port.

## Installation

```
pip install jenkins-external
```

## Usage

```
usage: jenkins-external [-h] [-d DISPLAY_NAME] [-s SSH_COMMAND]
                        [-x EXECUTABLE] [-q]
                        host port job command [args [args ...]]

Runs a command, and passes its output to Jenkins as an external job.

positional arguments:
  host                  Jenkins hostname (for Jenkins SSH server)
  port                  Jenkins SSH server port
  job                   Jenkins job name
  command               command to be run under this script
  args                  arguments to pass to the command

optional arguments:
  -h, --help            show this help message and exit
  -d DISPLAY_NAME, --display-name DISPLAY_NAME
                        display name of the build
  -s SSH_COMMAND, --ssh-command SSH_COMMAND
                        ssh command
  -x EXECUTABLE, --executable EXECUTABLE
                        the executable to actually use
  -q, --no-job-id       do not print the job ID in the end
```

### Example

```
# Sends 'Hello, World!' to a job called `my-job` on a Jenkins instance
# running on `jenkins.example.com`, whose SSH port is 12345.
jenkins-external jenkins.example.com 12345 my-job echo 'Hello, World!'
```
