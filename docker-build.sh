#!/usr/bin/env sh

# Get the tag
if [ "$#" -gt 0 ] ; then
    export TAG="$1"
else
    export TAG="latest"
fi

# Get the build
if [ -n "$GITHUB_SHA" ] ; then
    GIT_HASH=${GITHUB_SHA}
    GIT_BRANCH=${GITHUB_REF#refs/heads/}
else
    GIT_HASH=$(git rev-parse HEAD)
    GIT_BRANCH=$(git symbolic-ref --short HEAD)
fi
GIT_HASH_SHORT=$(git rev-parse --short "$GIT_HASH")
export BUILD=${GIT_BRANCH}.${GIT_HASH_SHORT}

echo "Building mrsarm/django-coleman:${TAG} with image_build $BUILD ..."

set -x
#docker-compose build
docker build --build-arg=BUILD="$BUILD" -t mrsarm/django-coleman:${TAG} .
