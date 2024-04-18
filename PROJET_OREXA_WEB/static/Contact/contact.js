function openPopupcontact() {
    let popup = document.getElementById("popup");

    // Vérifier si le formulaire est rempli
    let nom = document.getElementById("nom").value;
    let prenom = document.getElementById("prenom").value;
    let email = document.getElementById("email").value;
    let message = document.getElementById("message").value;

    if (nom === "" || prenom === "" || email === "" || message === "") {
        // Afficher la popup d'erreur
        document.getElementById("popupTitle").innerText = "Erreur";
        document.getElementById("popupMessage").innerText = "Veuillez remplir tous les champs!";
        document.getElementById("icon").src = "../static/Contact/no_icon.png";
    } else {
        // Afficher le message de succès dans la popup
        document.getElementById("popupTitle").innerText = "Validé";
        document.getElementById("popupMessage").innerText = "Votre réponse a bien été enregistrée!";
        document.getElementById("icon").src = "../static/Contact/ok_icon.png";

        // Effectuer une requête AJAX vers la route Python
        $.ajax({
            type: "POST",
            url: "/envoyer_message",
            data: $("form").serialize(), // Sérialiser les données du formulaire
            success: function (response) {
                document.getElementById("popupTitle").innerText = "Validé";
                document.getElementById("popupMessage").innerText = "Votre réponse a bien été enregistrée!";
                document.getElementById("icon").src = "../static/Contact/ok_icon.png";
            },
            error: function (xhr, status, error) {
                document.getElementById("popupTitle").innerText = "Erreur";
                document.getElementById("popupMessage").innerText = "Erreur lors de l'appel de la fonction Python.";
                document.getElementById("icon").src = "../static/Contact/no_icon.png";
            }
        });
    }

    // Afficher la popup
    popup.classList.add("popup-open");

    // Fermer la popup après 2 secondes
    setTimeout(function() {
        closePopupcontact();
    }, 1500);
}
function closePopupcontact() {
    let popup = document.getElementById("popup");
    popup.classList.remove("popup-open");
}

