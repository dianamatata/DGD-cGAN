FROM nvidia/cuda:12.2.2-base-ubuntu20.04
#FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYENV_ROOT=/opt/pyenv \
    PATH=/opt/pyenv/shims:/opt/pyenv/bin:$PATH

# Install dependencies for SSH, git, pyenv build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        curl \
        git \
        git-lfs \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libffi-dev \
        liblzma-dev \
        openssh-server \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/sshd

# Add non-root user
RUN useradd -m -d /myhome -s /bin/bash user && \
    usermod -p '' user

# Configure OpenSSH
RUN printf '%s\n' \
        'PasswordAuthentication no' \
        'KbdInteractiveAuthentication no' \
        'ChallengeResponseAuthentication no' \
        'UsePAM no' \
        'PermitRootLogin no' \
        'PubkeyAuthentication yes' \
        'AllowTcpForwarding yes' \
        'AllowAgentForwarding yes' \
    > /etc/ssh/sshd_config.d/10-container.conf && \
    ssh-keygen -A

# Install pyenv
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT && \
    git clone https://github.com/pyenv/pyenv-virtualenv.git $PYENV_ROOT/plugins/pyenv-virtualenv

# Install Python version and set global
RUN pyenv install 3.11.7 && pyenv global 3.11.7

# Set shell environment for pyenv
SHELL ["/bin/bash", "-c"]

# Install Python packages
WORKDIR /myhome
COPY requirements_docker.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements_docker.txt

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]
