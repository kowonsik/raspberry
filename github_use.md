
sudo apt-get install git

mkdir ~/workspace

cd ~/workspace
git init

git config --global user.name [유저이름]
git config --global user.email [이메일주소]

git remote add origin https://github.com/kowonsik/raspberry.git

git push -u origin master

git add [생성한파일]

git commit -m "메세지"
