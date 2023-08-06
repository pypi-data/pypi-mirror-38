# Machine Learning CLI

This is an attempt to abstract lots of the repeatedly used commands in training and testing machine learning projects.

## Motivation

Docker is very helpful in packaging machine learning environments. With support of Nvidia, we could train models on the GPU from docker.
That solves of problems with the existing way of working with existing research projects.
Research projects are here to stay.
They are static. Once published, they don't change often.
Therefore, packaging your python packages in your normal `requirements.txt` file for use in `virutalenv` or your `environment.yml` for use in `conda` is not a long-term solution.
Packages change fast; Python versions change even faster; Operating systems vary. Your packages might be compatbile wiht Ubuntu 14.0LTS but not Ubuntu 18 LTS.
If you work off Mac OS X, other researchers might be working off Windows or Ubuntu.
Therefore, I highly recommend developing research in contained docker containers.
When reproducing a papers's result, I often spend more time trying to get the environment setup than actually working on the research paper itself or its traiing.
`ml-cli` aims at replacing your bash `scripts` folder. It provides an easy, customizable, and portable (across different projects) solution for your machine learning environments.

## Usage

### Installation

To  install, the following package, run the following:
```
pip install --upgrade ml-cli
```

## Usage

Initialize a new docker project.
```
ml-cli init --repository {name-of-your-docker-image/repository}
```

If you need root access to run docker, you could use the following:
```
ml-cli --root init --repository {name-of-your-docker-image/repository}
```

### Building your Docker Container

```
ml-cli docker-build
```
If you need root access, use the following:
```
ml-cli --root docker-build
```

### Bash-ing into your Docker Container

To SSH/BASH into your container, use the following command:
```
ml-cli docker-bash
```

If you need root access, run the following:
```
ml-cli --root docker-bash
```

## Bugs & Contribution

If you encounter any issues or have any improvements, don't hesitate to contact me!
