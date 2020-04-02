git checkout hexo
git checkout --orphan orphan-hexo
git commit -am  "reborn"
git branch -D hexo 
git branch -m hexo 
git push -f origin hexo
choice /T 5 /C ync /CS /D y /n
