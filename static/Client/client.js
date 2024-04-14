function openPopupclient() {
    let popup = document.getElementById("popup");
    popup.classList.add("popup-open");
}

function submitFormclient() {
    // Récupérer les valeurs du formulaire
    var option = document.querySelector('input[type="radio"]:checked').value;
    var heure = document.getElementById("heure").value;
    var autres = [];
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    checkboxes.forEach(function(checkbox) {
        autres.push(checkbox.value);
    });

    // Effectuer une requête AJAX vers la route Python
    $.ajax({
        type: "POST",
        url: "/traiter_commande",
        data: { option: option, heure_livraison: heure, autres_options: autres },
        success: function(response) {
            document.getElementById("popupTitle").innerText = "Validé";
            document.getElementById("popupMessage").innerText = response;
        },
        error: function(xhr, status, error) {
            document.getElementById("popupTitle").innerText = "Erreur";
            document.getElementById("popupMessage").innerText = "Erreur lors du traitement de la commande.";
        }
    });

    // Fermer la pop-up
    closePopupclient();
}

function closePopupclient() {
    let popup = document.getElementById("popup");
    popup.classList.remove("popup-open");
}




// Sélectionner toutes les images des véhicules
const carImages = document.querySelectorAll('.all_vehicules img');

// Parcourir chaque image et ajouter un écouteur d'événements au clic
carImages.forEach(image => {
    image.addEventListener('click', function() {
        // Retirer la couleur de fond de toutes les images
        carImages.forEach(img => {
            img.style.backgroundColor = 'transparent';
        });
        // Ajouter la couleur de fond à l'image cliquée
        this.style.backgroundColor = 'deeppink';
    });
});