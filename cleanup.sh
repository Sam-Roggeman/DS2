docker kill $(docker ps -q)
docker container prune
docker rm $(docker ps --filter "name=ds2_files" -q)
docker rmi -f $(docker images -q)
docker volume prune
docker network prune
docker volume prune -a
