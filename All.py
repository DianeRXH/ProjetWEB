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

@app.route('/agilean')
def afficher_commandes_agilean():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT commande_client.id,temps,etat,voiture.type,option_1,option_2,option_3 \
    FROM voiture \
    JOIN commande_client ON commande_client.voiture=voiture.id \
    WHERE commande_client.etat!=3")
    lignes_commandes = cur.fetchall()
    con.close()
    return render_template('agilean.html', les_commandes=lignes_commandes)


@app.route('/agilog')
def agilog():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    # Sélectionner les ID des commandes à l'état 0
    cur.execute("SELECT id FROM commande_client WHERE etat=0")
    commandes_etat_zero = cur.fetchall()

    kits_par_commande = []

    # Pour chaque commande à l'état 0, récupérer les kits associés
    for commande in commandes_etat_zero:
        cur.execute(f"SELECT c.id, c.etat, kdv.kit, k.nom \
                      FROM kit_dans_voiture kdv \
                      JOIN commande_client c ON c.voiture=kdv.voiture \
                      JOIN kit k ON k.ID=kdv.kit \
                      WHERE c.id=?", (commande['id'],))
        lignes_kits = cur.fetchall()
        kits_par_commande.append(lignes_kits)

    con.close()

    return render_template('agilog.html', liste_kits=kits_par_commande)

def kit_par_voiture(id_voiture):
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT kit_dans_voiture.kit,kit_dans_voiture.nombre \
        FROM kit_dans_voiture \
        WHERE kit_dans_voiture.voiture=type_voiture")
    lignes_kits = cur.fetchall()
    con.close()
    return render_template('agilog.html', kits=lignes_kits)



@app.route('/agilog', methods=['POST'])
def livrer():
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
        return ('Kits livrés')
    except ValueError:
        return ('Valeur de la commande non connue')


@app.route('/agigreen')
def agigreen():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    # Sélectionner les ID des commandes à l'état 0
    cur.execute("SELECT id FROM commande_client WHERE etat=0")
    commandes_etat_zero = cur.fetchall()

    kits_par_commande = []

    # Pour chaque commande à l'état 0, récupérer les kits associés
    for commande in commandes_etat_zero:
        cur.execute(f"SELECT c.id, c.etat, kdv.kit, k.nom \
                          FROM kit_dans_voiture kdv \
                          JOIN commande_client c ON c.voiture=kdv.voiture \
                          JOIN kit k ON k.ID=kdv.kit \
                          WHERE c.id=?", (commande['id'],))
        lignes_kits = cur.fetchall()
        kits_par_commande.append(lignes_kits)

    con.close()

    return render_template('agilog.html', liste_kits=kits_par_commande)


def kit_par_voiture(id_voiture):
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT kit_dans_voiture.kit,kit_dans_voiture.nombre \
            FROM kit_dans_voiture \
            WHERE kit_dans_voiture.voiture=type_voiture")
    lignes_kits = cur.fetchall()
    con.close()
    return render_template('agilog.html', kits=lignes_kits)


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
    # Récupérer les données du formulaire
    heure_livraison = request.form['heure_livraison']
    autres_options = request.form.getlist('option')
    vehicule =  request.form['all_vehicules']

    # Connexion à la base de données
    con = lite.connect('base_donnees_OREXA_v2.db')
    cur = con.cursor()

    # Assembler l'ID du véhicule en fonction des options
    options = {'option1': 0, 'option2': 0, 'option3': 0}
    vehicule_id = assembler_vehicule(vehicule, options)

    # Insérer les données dans la table commande_client
    cur.execute("INSERT INTO commande_client (voiture, temps, etat) VALUES (?, ?, ?)",
            (vehicule_id, heure_livraison, 0))

    # Récupérer l'ID de la dernière commande insérée
    commande_id = cur.lastrowid

    # Insérer les autres options dans une autre table ou les traiter comme nécessaire
    for autre_option in autres_options:
        cur.execute("INSERT INTO autres_options (commande_id, option) VALUES (?, ?)",
                    (commande_id, autre_option))

    # Commit et fermeture de la connexion à la base de données
    con.commit()
    con.close()

    return "Commande enregistrée avec succès !"

def assembler_vehicule(vehicule, options):
    vehicule_id = vehicule
    if options['option1'] == 1:
        vehicule_id += '1'
    if options['option2'] == 1:
        vehicule_id += '2'
    if options['option3'] == 1:
        vehicule_id += '3'
    return vehicule_id


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