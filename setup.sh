#!/bin/bash
sudo apt update && sudo apt install -y locales
sudo locale-gen pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
export LANG=pt_BR.UTF-8
export LANGUAGE=pt_BR.UTF-8
