#!/bin/bash

# Installation des dépendances système
apt-get update
apt-get install -y python3 python3-pip

# Installation des packages Python
pip3 install -r requirements.txt

# Création des répertoires nécessaires
mkdir -p .streamlit
