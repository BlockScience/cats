git add .
git commit -m "catNode: add py deps"
git push origin deps
#docker build --no-cache -t cats . --build-arg GIT_PAS=${GIT_PAS}
docker build -t cats . \
  --build-arg GIT_PAS=${GIT_PAS} \
  --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}