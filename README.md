THis is a Payment backend project

# Update system
````
sudo apt-get update
sudo apt-get upgrade
````
## pyenv
# install required dependencies for pyenv
````
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
````
# Install pyenv
````
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
````
## configure pyenv
````
Add these lines to your .bashrc
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
Install pyenv-virtualenv to manage virtualenvs
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
````

# Create a directory called Projects in $HOME if not exists already and switch
````
mkdir $HOME/Projects
cd $HOME/Projects
````
# Install pip requirements
````
pip install -r requirements.txt
````
# Run Project
````
uvicorn main:app --reload
````
# For Mail 
````
https://myaccount.google.com/apppasswords 
````
# Main Url 
````
{ip}/docs
````
