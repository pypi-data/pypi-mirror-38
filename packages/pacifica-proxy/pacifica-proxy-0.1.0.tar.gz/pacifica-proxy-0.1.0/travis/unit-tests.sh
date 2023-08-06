#!/bin/bash -xe

export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
pushd travis/metadata
MetadataServer.py &
MD_PID=$!
popd
pushd travis/archivei
ArchiveInterfaceServer.py &
AI_PID=$!
popd
MAX_TRIES=60
HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
while [[ $HTTP_CODE != 200 && $MAX_TRIES > 0 ]] ; do
  sleep 1
  HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
  MAX_TRIES=$(( MAX_TRIES - 1 ))
done
TOP_DIR=$PWD
MD_TEMP=$(mktemp -d)
git clone https://github.com/pacifica/pacifica-metadata.git ${MD_TEMP}
pushd ${MD_TEMP}
python test_files/loadit.py
popd

curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file README.md http://127.0.0.1:8080/104
readme_size=$(stat -c '%s' README.md)
readme_sha1=$(sha1sum README.md | awk '{ print $1 }')
echo '{ "hashsum": "'$readme_sha1'", "hashtype": "sha1", "size": '$readme_size'}' > /tmp/file-104-update.json
curl -X POST -H 'content-type: application/json' -T /tmp/file-104-update.json 'http://localhost:8121/files?_id=104'

export PYTHONPATH=$PWD
coverage run --include='proxy/*' -m pytest -v
coverage run --include='proxy/*' -a ProxyServer.py --stop-after-a-moment

coverage report -m --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
kill -9 ${MD_PID} ${AI_PID} || true
wait ${MD_PID} ${AI_PID} || true
kill $(cat nginx.pid) || true
