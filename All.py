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

def kit_par_voiture(type_voiture,options): #ex : options =[0,0,1] à que l'option 3
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
    return render_template('agilean.html')

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