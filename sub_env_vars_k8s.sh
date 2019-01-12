#!/usr/bin/env bash

# Replaces all the env var required in kubernetes files

for k8s_file in kubernetes/*
do
  envsubst < ${k8s_file} > "${k8s_file%%.*}_patched.yaml"
  rm -f ${k8s_file}
done