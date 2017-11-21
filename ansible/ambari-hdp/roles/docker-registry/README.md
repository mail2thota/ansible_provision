# Ansible Role: Docker

An Ansible Role that installs [Docker](https://www.docker.com) on Linux and Launch docker-registry.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    # Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
    docker_edition: 'ce'
    docker_package: "docker-{{ docker_edition }}"
    docker_package_state: present

The `docker_edition` should be either `ce` (Community Edition) or `ee` (Enterprise Edition). You can also specify a specific version of Docker to install using a format like `docker-{{ docker_edition }}-<VERSION>`. And you can control whether the package is installed, uninstalled, or at the latest version by setting `docker_package_state` to `present`, `absent`, or `latest`, respectively.

    docker_install_compose: true
    docker_compose_version: "1.16.1"
    docker_compose_path: /usr/local/bin/docker-compose
    docker_registry: "docker-distribution"

(Used only for RedHat/CentOS.)

## Dependencies

None.

## Example Playbook

```yaml
- hosts: docker-registry
  roles:
    - docker-registry
```

## License

mdr_platform_bare_metal - ansible - Copyright (c) 2016 BAE Systems Applied Intelligence.
