
sudo apt-get install git

mkdir ~/workspace

cd ~/workspace

git init

git config --global user.name [유저이름]
git config --global user.email [이메일주소]

git remote add origin https://github.com/kowonsik/raspberry.git

git pull -u origin master

git add [생성한파일]

git commit -m "메세지"

git push -u origin master

-----
origin url 설정이 잘못되서 origin을 삭제(수정)해야할 경우

git remote rm origin

git remote rename origin origin_re

----
git 용어정리(http://dimdim.tistory.com/entry/GIT에-대한-내용정리-정리중)
