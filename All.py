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
@app.route('/agilog')
def afficher_commandes_agilog():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT commande_client.id,temps,etat,voiture.type,option_1,option_2,option_3 \
    FROM voiture \
    JOIN commande_client ON commande_client.voiture=voiture.id")
    lignes_commandes = cur.fetchall()
    con.close()
    return render_template('agilog.html', les_commandes=lignes_commandes) #stock=lignes_stock

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
@app.route('/agilean')
def agilean():
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

    return render_template('agilean.html', liste_kits=kits_par_commande)

@app.route('/agilean', methods=['POST'])
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
    return render_template('agigreen.html')

@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        return render_template('Client.html', form=request.form)


"""

@app.route('/agilean', methods=['GET', 'POST'])
def afficher_commandes_agigreen():
    con = lite.connect('base_donnees_OREXA_v2.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT nom, prenom, role FROM personnes")
    lignes = cur.fetchall()
    con.close()
    return render_template('Agilean.html', personnes=lignes)



@app.route('/agilean', methods=['GET', 'POST'])
def ajouter_personne():
    if not request.method == 'POST':
        return render_template('formulaire_personne.html', msg="", nom="", prenom="", role=0)
    else:
        nom = request.form.get('nom', '')
        prenom = request.form.get('prenom', '')
        role = request.form.get('role', 0, type=int)

        if (nom != "" and prenom != "" and role > 0 and role < 4):
            con = lite.connect('exemples.db')
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom, prenom, role))
            conn.commit()
            conn.close()
            return redirect(url_for('afficher_personnes'))
        else:
            return render_template('formulaire_personne.html', msg="Mauvaise saisie !", nom="", prenom="", role=0)

"""

"""
def ajouter_personne():
    if not request.method == 'POST':
        return render_template('formulaire_personne.html', msg="", nom="", prenom="", role=0)
    else:
        nom = request.form.get('nom', '')
        prenom = request.form.get('prenom', '')
        role = request.form.get('role', 0, type=int)

        if (nom != "" and prenom != "" and role > 0 and role < 4):
            con = lite.connect('exemples.db')
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom, prenom, role))
            con.commit()
            con.close()
            return redirect(url_for('afficher_personnes'))
        else:
            return render_template('formulaire_personne.html', msg="Mauvaise saisie !", nom="", prenom="", role=0)
"""
# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5678)