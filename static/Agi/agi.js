// Fonction pour traiter la commande
function livrer(event) {
    // Empêcher la soumission du formulaire par défaut
    event.preventDefault();

    // Récupérer la valeur du champ texte
    var valeurCommande = document.getElementById("champ_texte").value;

    // Envoyer une requête AJAX vers le serveur pour traiter la commande
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/agilean", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Créer un élément div pour afficher le message
                var messageDiv = document.createElement("div");
                messageDiv.textContent = xhr.responseText;
                messageDiv.classList.add("message"); // Ajouter une classe CSS pour le style

                // Ajouter le message après le formulaire
                var formElement = document.getElementById("livrerForm");
                formElement.parentNode.insertBefore(messageDiv, formElement.nextSibling);
            } else {
                alert("Une erreur s'est produite lors du traitement de la commande.");
            }
        }
    };
    xhr.send("champ_texte=" + encodeURIComponent(valeurCommande));
}

// Ajouter un écouteur d'événement au formulaire
document.addEventListener("DOMContentLoaded", function() {
    var formulaire = document.getElementById("livrerForm");
    if (formulaire) {
        formulaire.addEventListener("submit", function(event) {
            livrer(event);
            // Empêcher la soumission du formulaire par défaut
            event.preventDefault();
        });
    }
});
