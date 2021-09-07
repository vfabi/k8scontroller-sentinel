# k8scontroller-sentinel

Kubernetes controller to manage some special tasks.

## Status

Beta

## Features

- handler to remove pods with status phase=Failed and reason=Shutdown
- helper method to send messages to Slack

## Technology stack

- Python 3.8+
- KOPF - Kubernetes OPerators Framework

## Configuration

### Environment variables

Name | Description | Mandatory | Default | Example
--- | --- | --- | --- | ---
SLACK_URL | Slack incoming web hook URL. For sending message to Slack. | true | | https://hooks.slack.com/services/T127SJ7LZJ5/A12D22SFPD3/11gEI9FlguRBPvLVkydtDs22k |
SLACK_CHANNEL | Slack channel. For sending message to Slack. | true | | #alerts |

## Usage

### Deployment

1. Check configuration: environment variables in `deployment/kubernetes/configmap.yaml`
2. Just apply all yaml files from `deployment/kubernetes/` folder.

## Docker

[![Generic badge](https://img.shields.io/badge/hub.docker.com-vfabi/k8scontroller-sentinel-<>.svg)](https://hub.docker.com/repository/docker/vfabi/k8scontroller-sentinel)

## Contributing

Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## License

Apache 2.0
