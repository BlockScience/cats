git add .
git commit -m "catNode: add py deps"
git push origin deps
docker build --no-cache -t cats . --build-arg GIT_PAS=${GIT_PAS}