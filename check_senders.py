import mailbox
import os
import re
from shutil import copytree, rmtree

"""
Ce script python check le nombre d'expéditeurs uniques d'une boite email,
et si ce nombre est > ou = à un seuil, execute un script bash

Conçu pour jouer à FarHorizons :p

Version du 14/11/2020
"""


"""
VARIABLES A CONFIGURER
----------------------
path_to_mailbox_new : 
path_to_fakemail : chemin vers la mailbox de type Maildir
        doit contenir les dossiers suivants:
            cur/
            new/
            tmp/
            .dossier   # (facultatif) un dossier de rangement, lui même de type MailDir
        
nb_joueurs : le nombre d'adresse mail différentes qu'il faut avoir

path_to_fh_script : fullpath du script bash de FH
        doit être un executable : chmod u+x script.sh
"""
path_to_mailbox_new = "/home/Projets/FarHorizonsTools/mailbox/FH/new"
path_to_fakemail = "/home/Projets/FarHorizonsTools/mailbox/fakemail"
nb_joueurs = 3
path_to_fh_script = "/home/Projets/FarHorizonsTools/test.sh"

# --------------
# COPIER LES FICHIERS de new vers FAKEMAILDIR
copytree(path_to_mailbox_new, path_to_fakemail+"/new", dirs_exist_ok=True)


# --------------------------------------------------
#
# extraire que l'adresse du champ FROM via une regex
pattern = r"[\w\.\+-]+@[\w\+\.-]+"
regex = re.compile(pattern)

# Accéder aux emails et créer un ensemble d'expéditeurs uniques (pas de doublon grâce à set)
box = mailbox.Maildir(path_to_fakemail)
uniques_senders = set()
for msg in box.values():
    flags = msg.get_flags()
    print(f"flags = {flags} -- {msg['From']} -- {msg['Subject']}")  # DEBUG

    # Ne prendre en compte que les messages dont le titre contient "FHORDERS"
    if "fhorders" in msg["Subject"].lower():
        # Ne prendre en compte que les messages non-lus
        if "S" in flags:
            pass
        else:
            # on ne vetu que l'adresse email "abc@example.com", pas les fioritures autour '<Example>abc@example.com'
            match = regex.search(msg["From"])
            if match:
                # on a un hit: une adresse email
                sender = match.group()
                uniques_senders.add(sender)
                print(f"   HIT = {flags} - {sender}")  # DEBUG

print(uniques_senders)  # DEBUG

# --------------
# VIDER LES FICHIERS de FAKEMAILDIR
rmtree(path_to_fakemail+"/new")


# vérifier que tous les joueurs ont envoyé leur email
# et si oui, lancer le script de FarHorizons
if len(uniques_senders) >= nb_joueurs:
    os.system(path_to_fh_script)
