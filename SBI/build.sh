#!/bin/bash
export PATH="$PATH:/usr/local/bin"
export USERID=$(id -u)
export GROUPID=$(id -g)

cd $(dirname $0)

CONTAINER_NAME="tester-$(echo ${JOB_NAME} | tr '/ ' '._').${BRANCH_NAME}"
[ -n "$CHANGE_ID" ] && CONTAINER_NAME="${CONTAINER_NAME}-PR${CHANGE_ID}"
CONTAINER_NAME="${CONTAINER_NAME}-${BUILD_ID}"

docker-compose -f builder.yml run \
      --rm -w "$WORKSPACE" \
      --name "$CONTAINER_NAME" \
      -e ARCH=$ARCH -e REGION=$REGION \
      jenkins-fleet
