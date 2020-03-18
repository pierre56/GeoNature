parentdir="$(dirname "$(pwd)")"
currentdir=${PWD##*/}
myrootpath=`pwd`/..

cd $myrootpath/frontend

#make nvm available 
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

npm run start

nvm install
nvm uses

echo " ############"
echo "Installation des paquets npm"
npm ci --only=prod