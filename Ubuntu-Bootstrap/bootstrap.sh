#!/bin/bash

if [[ $(id -u) -ne 0 ]]; 
  then echo "Ubuntu dev bootstrapper, Install the things I want -- run as root...";
  exit 1; 
fi

# https://www.google.com/linuxrepositories/
# https://www.microsoft.com/net/core#linuxubuntu
# https://code.visualstudio.com/docs/setup/linux
# https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions
# https://yarnpkg.com/lang/en/docs/install/
# https://golang.org/doc/install#tarball

# TODO:
# Configure git
# Pull scripts from my github
# Add stuff to bash.rc
# Config tmuxinator and tmux

echo -e "**************************************************"
echo -e "*              Updating repositories             *"
echo -e "**************************************************"

sudo apt -y update

echo -e ".................................................."
echo -e ".             Upgrading repositories             ."
echo -e ".................................................."

sudo apt -y upgrade

echo -e ".................................................."
echo -e ".                 Auto Cleanup                   ."
echo -e ".................................................."

sudo apt -y autoclean && sudo apt -y autoremove

echo -e ".................................................."
echo -e ".                 Upgrade Dist                   ."
echo -e ".................................................."

sudo apt -y dist-upgrade

echo -e ".................................................."
echo -e ".                 Auto Cleanup                   ."
echo -e ".................................................."

sudo apt -y autoclean && sudo apt -y autoremove

echo -e ".................................................."
echo -e ".              Install Essentials                ."
echo -e ".................................................."

echo "Some essentials..."
sudo apt-get install -y curl wget git xclip vim tmux tmuxinator\
  apt-transport-https ca-certificates gnupg gnupg-agent build-essential \
  lsb-release software-properties-common ssh

# Chrome setup
echo -e ".................................................."
echo -e ".                Install Chrome                  ."
echo -e ".................................................."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt build-dep -y ./google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Docker setup - https://docs.docker.com/engine/install/ubuntu/
echo -e ".................................................."
echo -e ".                Install Docker                  ."
echo -e ".................................................."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y build-dep docker-ce docker-ce-cli containerd.io
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

# Docker Compose - https://docs.docker.com/compose/install/
echo -e ".................................................."
echo -e ".             Install Docker Compose             ."
echo -e ".................................................."
sudo apt -y update
sudo apt -y upgrade
curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# VS Code setup - https://code.visualstudio.com/docs/setup/linux
echo -e ".................................................."
echo -e ".                Install VS Code                 ."
echo -e ".................................................."
sudo snap install --classic code

# Node setup - https://github.com/nodesource/distributions/blob/master/README.md
#curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
#apt-get install -y nodejs

#curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
#apt-get install -y nodejs

# build tools
echo -e ".................................................."
echo -e ".              Install Build Tools               ."
echo -e ".................................................."
sudo apt-get build-dep -y gcc g++ make
sudo apt-get install -y gcc g++ make

# Yarn setup - https://yarnpkg.com/lang/en/docs/install/#debian-stable
echo -e ".................................................."
echo -e ".                 Install Yarn                   ."
echo -e ".................................................."
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt-get update -y
sudo apt build-dep yarn -y
sudo apt install yarn -y

# Go
echo -e ".................................................."
echo -e ".                  Install Go                    ."
echo -e ".................................................."
VERSION=1.15
OS=linux
ARCH=amd64
wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz -O /tmp/go$VERSION.$OS-$ARCH.tar.gz
tar -C /usr/local -xzf /tmp/go$VERSION.$OS-$ARCH.tar.gz

# Using "~" in sudo context will get "/root" so wild guess the profile path:
USERS_PROFILE_FILENAME=/home/${SUDO_USER}/.profile
if grep -Fq "/usr/local/go/bin" $USERS_PROFILE_FILENAME
then
    echo "GO path found in $USERS_PROFILE_FILENAME"
else
    echo '
export PATH=$PATH:/usr/local/go/bin
' >> $USERS_PROFILE_FILENAME
fi

# adds the cuurent user who is sudo'ing to a docker group:
groupadd docker
usermod -aG docker $SUDO_USER
service docker restart
# note that typically you still need a logout/login for docker to work...

echo -e ".................................................."
echo -e ".                 Auto Cleanup                   ."
echo -e ".................................................."

sudo apt -y autoclean
sudo apt -y autoremove

cat << EOF
# now....
code --install-extension ms-dotnettools.csharp
code --install-extension golang.go
code --install-extension dbaeumer.vscode-eslint
code --install-extension HookyQR.beautify
code --list-extensions
# git setup:
git config --global user.email "bousborne@pivot3.com"
git config --global user.name "Benjamin Ousborne"
ssh-keygen -t rsa -b 4096 -C "bousborne@pivot3.com"
eval "\$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub
# now go to https://github.com/settings/keys
# also check docker... you may need to login again for groups to sort out
# try >> docker run hello-world
# To use GO straight up, get the path:
source ~/.profile
EOF
