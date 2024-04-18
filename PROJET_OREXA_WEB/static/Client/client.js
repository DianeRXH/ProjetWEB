function openPopupclient() {
    let popup = document.getElementById("popup");
    popup.classList.add("popup-open");
}

function submitFormclient() {

    // Récupérer les données à envoyer
    let heureLivraison = document.getElementById("heure").value;
    let vehiculeSelectionne = document.querySelector('input[name="vehicule"]:checked').value;
    let optionsSelectionnees = Array.from(document.querySelectorAll('input[name="option"]:checked')).map(option => option.value);

    // Créer un objet contenant les données à envoyer
    let data = {
        heureLivraison: heureLivraison,
        vehicule: vehiculeSelectionne,
        options: optionsSelectionnees
    };

    // Envoyer les données à votre serveur Flask
    fetch('/traiter_commande', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

        // Fermer la pop-up
    closePopupclient();
    window.location.reload();
}
function closePopupclient() {
    let popup = document.getElementById("popup");
    popup.classList.remove("popup-open");
    window.location.reload();
}




// Sélectionner toutes les images des véhicules
const Options = document.querySelectorAll('.option');

// Parcourir chaque image et ajouter un écouteur d'événements au clic
Options.forEach(image => {
    image.addEventListener('click', function() {
        // Retirer la couleur de fond de toutes les images
        Options.forEach(img => {
            img.style.backgroundColor = 'transparent';
        });
        // Ajouter la couleur de fond à l'image cliquée
        this.style.backgroundColor = 'deeppink';
    });
});