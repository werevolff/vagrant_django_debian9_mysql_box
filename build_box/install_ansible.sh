#!/bin/bash

# Install required packages
sudo apt update
sudo apt install -y build-essential libssl-dev libffi-dev python3.5 \
  build-essential python3.5-dev python3-pip python3-ndg-httpsclient libpq-dev \
  python3-virtualenv virtualenv libjpeg-dev zlib1g-dev libpng-dev libjpeg-dev \
  bzip2 libbz2-dev

# Export environment variables
set -o allexport
[[ -f /vagrant/.env ]] && source /vagrant/.env
set +o allexport

# Install pyenv
rm -rf ${PYENV_ROOT}
cp -f /vagrant/new_profile /home/vagrant/.profile
export PATH="${PYENV_ROOT}/bin:$PATH"
cd ${PYENV_DOWNLOAD_DIR} && curl -L ${PYENV_DOWNLOAD_URL} | bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install python with target version
pyenv install ${PYTHON_SYSTEM_VERSION}
sudo update-alternatives --install /usr/bin/python python ${PYENV_ROOT}/versions/${PYTHON_SYSTEM_VERSION}/bin/python 1
sudo ln -s ${PYENV_ROOT}/versions/${PYTHON_SYSTEM_VERSION}/bin/pip /usr/bin/pip

# Install Ansible
sudo pip3 install -U pip setuptools
sudo pip3 install pyOpenSSL==19.1.0
sudo pip3 install ansible==2.9.9
