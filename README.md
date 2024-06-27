# Projet Tool Box

Ce projet Tool Box contient plusieurs scripts Python pour diverses tâches de sécurité informatique, y compris des scans de réseau, des keyloggers, des reverse shells, des attaques par force brute, et des vérifications de vulnérabilités CVE.

## Table des Matières

1. [Installation](#installation)
2. [Scripts Inclus](#scripts-inclus)
    - [Menu.py](#menupy)
    - [shellreverse.py](#shellreversepy)
    - [keylog.py](#keylogpy)
    - [nmap_scan.py](#nmap_scanpy)
    - [bruteforce.py](#bruteforcepy)
    - [cve.py](#cvepy)
3. [Utilisation](#utilisation)
4. [Rapport Complet](#rapport-complet)

## Installation

Pour installer les dépendances nécessaires pour exécuter ces scripts, vous devez exécuter le fichier `packages.bat` fourni. Ce fichier installera toutes les bibliothèques Python nécessaires.

### Instructions

1. Assurez-vous que Python est installé sur votre système.
2. Téléchargez ou clonez ce dépôt.
3. Exécutez le fichier `packages.bat` en double-cliquant dessus ou en utilisant la ligne de commande.

### Menu.py

Ce script offre une interface utilisateur graphique (GUI) pour sélectionner et exécuter les différents scripts du projet.

### Fonctions Principales:
- Lancer le script Nmap (`nmap_scan.py`)
- Lancer le script de Keylogger (`keylog.py`)
- Lancer le script Reverse Shell (`shellreverse.py`)
- Lancer le script de Force Brute (`bruteforce.py`)
- Lancer le script de Détection de Vulnérabilités (`cve.py`)
- Générer un rapport HTML complet de tous les résultats

### shellreverse.py

Ce script génère du code de reverse shell en PowerShell pour Windows ou en Python pour Linux, basé sur une IP et un port fournis par l'utilisateur via une interface GUI.

### Fonctions Principales:
- Génération de code de reverse shell PowerShell
- Génération de code de reverse shell Python

### keylog.py

Ce script implémente un keylogger qui capture les frappes de touches et les enregistre dans un fichier log. Il utilise une interface GUI pour démarrer et arrêter le keylogger.

### Fonctions Principales:
- Démarrer et arrêter le keylogger
- Enregistrer les frappes de touches dans un fichier log
- Ouvrir et effacer le fichier log

### nmap_scan.py

Ce script utilise Nmap pour scanner des réseaux et des machines, avec une interface GUI pour entrer les adresses IP et les ports à scanner. Il génère également des rapports XML et HTML.

### Fonctions Principales:
- Scan de réseau (liste des machines)
- Scan de ports spécifiques sur une machine
- Génération de rapports XML et HTML

### bruteforce.py

Ce script effectue une attaque par force brute sur un serveur SSH en utilisant une liste de mots de passe fournie par l'utilisateur. Il génère également des variantes de mots de passe basées sur des informations utilisateur.

### Fonctions Principales:
- Génération de variantes de mots de passe
- Attaque par force brute SSH
- Enregistrement des résultats dans un fichier log

### cve.py

Ce script effectue une vérification des vulnérabilités CVE pour les logiciels installés sur une machine. (Les détails de ce script doivent être fournis par l'utilisateur).

### Fonctions Principales:
- Vérification des vulnérabilités CVE (détails à compléter)

## Utilisation

1. Exécutez `Menu.py` pour ouvrir l'interface GUI principale.
2. Sélectionnez le script que vous souhaitez exécuter depuis le menu déroulant.
3. Suivez les instructions à l'écran pour chaque script spécifique.

## Rapport Complet

Le script `Menu.py` inclut une option pour générer un rapport HTML complet contenant les résultats de tous les scripts exécutés. Ce rapport est stocké dans le répertoire `resultats` et peut être ouvert directement depuis l'interface GUI.

## Note

- Assurez-vous que tous les scripts sont dans les emplacements spécifiés dans le code.
- Les chemins de fichiers peuvent nécessiter des ajustements en fonction de votre environnement.
- En cas de problèmes, consultez les commentaires dans les scripts individuels pour plus de détails et de dépannage.
