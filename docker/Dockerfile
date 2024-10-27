FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Add vscode user with same UID and GID as your host system
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.config

# Set up sudo
RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Switch from root to user
USER $USERNAME

# Install dependencies
RUN sudo apt-get update \
    && sudo apt-get install -y \
    pip \
    curl \
    libglib2.0-dev \
    xvfb \
    && sudo rm -rf /var/lib/apt/lists/*

# Create the X11 socket directory
RUN sudo mkdir /tmp/.X11-unix \
    && sudo chmod 1777 /tmp/.X11-unix 

# Install Microsoft packages
RUN sudo curl -sSL -O https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb \
    && sudo dpkg -i packages-microsoft-prod.deb \
    && sudo rm packages-microsoft-prod.deb \
    && sudo apt-get update \
    && sudo ACCEPT_EULA=Y apt-get install -y \
    libk4a1.4 \
    libk4a1.4-dev \
    && sudo rm -rf /var/lib/apt/lists/*

ENV PATH=/home/$USERNAME/.local/bin:${PATH}

# Install Python packages
RUN pip install pyk4a open3d opencv-python numpy==1.26.4

# Create the .bash_history file and set permissions
RUN touch /home/$USERNAME/.bash_history \
    && chown $USERNAME:$USERNAME /home/$USERNAME/.bash_history

# Set environment variables for bash history
ENV HISTFILE=/home/$USERNAME/.bash_history

# Copy the package into the container
ENV WORKSPACE_ROOT=/home/${USERNAME}/azure-kinect-mkv-extractor
COPY --chown=${USERNAME}:${USERNAME} .. ${WORKSPACE_ROOT}

# Make entrypoint.sh executable and set it as the entrypoint
RUN sudo chmod +x ${WORKSPACE_ROOT}/docker/entrypoint.sh
ENTRYPOINT ["sh", "/home/vscode/azure-kinect-mkv-extractor/docker/entrypoint.sh"]