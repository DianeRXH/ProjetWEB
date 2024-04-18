

from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

# ------------------
# application Flask
# ------------------

app = Flask(__name__)

# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/propos')
def propos():
    return render_template('propos.html')

###############################################################################
########         AGILean           ############################################
###############################################################################

@app.route('/agilean')
def afficher_commandes_agilean():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT commande_client.id,temps,etat,voiture.type,option_1,option_2,option_3 \
    FROM voiture \
    JOIN commande_client ON commande_client.voiture=voiture.id \
    WHERE commande_client.etat==2")
    lignes_commandes = cur.fetchall()
    con.close()
    return render_template('agilean.html', les_commandes=lignes_commandes)

@app.route('/agilean_popup', methods=['POST'])
def livrer_agilean():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute(f'UPDATE commande_client SET etat = 3 WHERE ID = ?', (valeur,))
        con.commit()
        con.close()
        return 'Vehicule livrés'
    except ValueError:
        return 'Valeur de la commande non connue'

@app.route('/verifier_commande_lean', methods=['POST'])
def verifier_commande_lean():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        # Vérifier l'état de la commande
        cur.execute("SELECT etat FROM commande_client WHERE ID = ?", (valeur,))
        etat_commande = cur.fetchone()
        con.close()
        if etat_commande and etat_commande['etat'] == 2:
            return "etat_2"
        else:
            return 'Commande NON disponible chez Agilean'
    except ValueError:
        return 'Valeur de la commande non connue'


##############################################################################
########         AGILOG           ############################################*
##############################################################################

@app.route('/agilog')
def agilog():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    # Sélectionner les ID des commandes à l'état 0
    cur.execute("SELECT id FROM commande_client WHERE etat=1")
    commandes_etat_un = cur.fetchall()

    kits_par_commande = []

    # Pour chaque commande à l'état 0, récupérer les kits associés
    for commande in commandes_etat_un:
        cur.execute(f"SELECT c.id, c.temps, kdv.kit, k.nom \
                      FROM kit_dans_voiture kdv \
                      JOIN commande_client c ON c.voiture=kdv.voiture \
                      JOIN kit k ON k.ID=kdv.kit \
                      WHERE c.id=?", (commande['id'],))
        lignes_kits = cur.fetchall()
        kits_par_commande.append(lignes_kits)

    con.close()

    return render_template('agilog.html', liste_kits=kits_par_commande)

def kit_par_voiture_log(id_voiture):
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT kit_dans_voiture.kit,kit_dans_voiture.nombre \
        FROM kit_dans_voiture \
        WHERE kit_dans_voiture.voiture=type_voiture")
    lignes_kits = cur.fetchall()
    con.close()
    return render_template('agilog.html', kits=lignes_kits)


@app.route('/agilog_popup', methods=['POST'])
def livrer_agilog():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute(f'UPDATE commande_client SET etat = 2 WHERE ID = ?', (valeur,))
        con.commit()
        con.close()
        return 'Kits livrés'
    except ValueError:
        return 'Valeur de la commande non connue'


@app.route('/verifier_commande_log', methods=['POST'])
def verifier_commande_log():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        # Vérifier l'état de la commande
        cur.execute("SELECT etat FROM commande_client WHERE ID = ?", (valeur,))
        etat_commande = cur.fetchone()
        con.close()
        if etat_commande and etat_commande['etat'] == 1:
            return "etat_1"
        else:
            return 'Commande NON disponible chez Agilog'
    except ValueError:
        return 'Valeur de la commande non connue'

##############################################################################
################ Agigreen ##############################################
##############################################################################

@app.route('/agigreen')
# Fonction pour récupérer id des commadnes etat 0
@app.route('/agigreen')
@app.route('/agigreen')
def agigreen():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    # Sélectionner les ID des commandes à l'état 1
    cur.execute("SELECT id FROM commande_client WHERE etat=0")
    commandes = cur.fetchall()

    # Récupérer les détails de chaque commande et les pièces associées
    commandes_details = []
    for commande in commandes:
        commande_id = commande['id']
        cur.execute("SELECT temps, voiture FROM commande_client WHERE ID=?", (commande_id,))
        commande_details = cur.fetchone()

        if commande_details:
            temps_livraison, voiture_id = commande_details
            cur.execute("SELECT type, option_1, option_2, option_3 FROM voiture WHERE ID=?", (voiture_id,))
            voiture_details = cur.fetchone()
            if voiture_details:
                type_vehicule, option_1, option_2, option_3 = voiture_details

                cur.execute("SELECT kit FROM kit_dans_voiture WHERE voiture=?", (voiture_id,))
                kits_voiture = cur.fetchall()

                kits = []
                total_pieces = 1
                for kit_voiture in kits_voiture:
                    kit_id = kit_voiture[0]
                    cur.execute("SELECT piece, nombre FROM piece_dans_kit WHERE kit=?", (kit_id,))
                    pieces_kit = cur.fetchall()

                    pieces = []
                    for piece_kit in pieces_kit:
                        piece_id, quantite = piece_kit
                        cur.execute("SELECT nom FROM piece WHERE ID=?", (piece_id,))
                        piece_nom = cur.fetchone()[0]
                        pieces.append({'nom': piece_nom, 'quantite': quantite})
                        total_pieces += 1

                    kits.append({'id': kit_id, 'pieces': pieces})

                commandes_details.append({
                    'ID': commande_id,
                    'temps': temps_livraison,
                    'type': type_vehicule,
                    'option_1': option_1,
                    'option_2': option_2,
                    'option_3': option_3,
                    'kits': kits,
                    'total_pieces': total_pieces
                })

    con.close()
    return render_template('agigreen.html', commandes=commandes_details)


@app.route('/agigreen_popup', methods=['POST'])
def livrer_agigreen():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute(f'UPDATE commande_client SET etat = 1 WHERE ID = ?', (valeur,))
        con.commit()
        con.close()
        return 'Pièces livrées'
    except ValueError:
        return 'Valeur de la commande non connue'


@app.route('/verifier_commande_green', methods=['POST'])
def verifier_commande_green():
    valeur = request.form['champ_texte']
    try:
        valeur = int(valeur)
        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        # Vérifier l'état de la commande
        cur.execute("SELECT etat FROM commande_client WHERE ID = ?", (valeur,))
        etat_commande = cur.fetchone()
        con.close()
        if etat_commande and etat_commande['etat'] == 0:
            return "etat_0"
        else:
            return 'Commande NON disponible chez Agigreen'
    except ValueError:
        return 'Valeur de la commande non connue'

##############################################################################
################ Client ##############################################
##############################################################################

@app.route('/client')
def commandes_livrees():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT commande_client.id,temps,etat,voiture.type,option_1,option_2,option_3 \
    FROM voiture \
    JOIN commande_client ON commande_client.voiture=voiture.id \
    WHERE commande_client.etat=3")
    lignes_commandes1 = cur.fetchall()

    cur.execute("SELECT commande_client.id,temps,etat,voiture.type,option_1,option_2,option_3 \
        FROM voiture \
        JOIN commande_client ON commande_client.voiture=voiture.id \
        WHERE commande_client.etat=0 or commande_client.etat=1 or commande_client.etat=2")
    lignes_commandes2 = cur.fetchall()
    con.close()
    return render_template('client.html', commandes_passees=lignes_commandes1, commandes_en_cours=lignes_commandes2)

@app.route('/traiter_commande', methods=['POST'])
def traiter_commande():
    # Récupérer les données du corps de la requête
    data = request.json

    # Extraire les données nécessaires
    heure_livraisons = data['heureLivraison']
    vehicule = data['vehicule']
    options = data['options']

    # Connexion à la base de données
    con = lite.connect('base_donnees_OREXA_v2.db')
    cur = con.cursor()

    # Assembler l'ID du véhicule en fonction des options
    vehicule_name = vehicule+"".join(options)
    print(vehicule_name)

    cur.execute("SELECT ID FROM voiture WHERE voiture.name=?", (vehicule_name,))
    vehicule_id = cur.fetchall()
    cur.fetchone()

    # Insérer les données dans la table commande_client
    cur.execute("INSERT INTO commande_client (voiture, temps, etat) VALUES (?, ?, ?)",(vehicule_id[0][0], heure_livraisons, 0))

    # Commit et fermeture de la connexion à la base de données
    con.commit()
    con.close()
    return "Commande inserte"

##############################################################################
################ Contact ##############################################
##############################################################################


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', form=request.form)

@app.route('/envoyer_message', methods=['GET', 'POST'])
def envoi_message():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        entreprise = request.form['entreprise']
        email = request.form['email']
        message = request.form['message']

        # Connexion à la base de données
        con = lite.connect('base_donnees_OREXA_v2.db')
        con.row_factory = lite.Row
        cur = con.cursor()
        # Insérer les données dans la table de contact
        cur.execute("INSERT INTO messages (nom, prenom, entreprise, email, message) VALUES (?, ?, ?, ?, ?)",
                       (nom, prenom, entreprise, email, message))
        con.commit()
        con.close()
        return 'Message envoyé avec succès !'
    else :
        return 'Nous avons rencontré un problème !'





# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5678)