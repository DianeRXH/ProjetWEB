function openPopupagi() {
    let popup = document.getElementById("popup");

    // Récupérer la valeur du champ texte
    let commande = document.getElementById("champ_texte").value;

    if (commande === "") {
        // Afficher la popup d'erreur si aucun numéro de commande n'est entré
        document.getElementById("popupTitle").innerText = "Erreur";
        document.getElementById("popupMessage").innerText = "Aucun numéro de commande rentré";
        document.getElementById("icon").src = "../static/Contact/no_icon.png";
        // Afficher la popup
        popup.classList.add("popup-open");

        // Fermer la popup après 2 secondes
        setTimeout(function() {
            closePopupagi();
        }, 1000);
    } else {
        // Effectuer une requête AJAX vers la route Python pour vérifier l'état de la commande
        $.ajax({
            type: "POST",
            url: "/verifier_commande_log",
            data: { champ_texte: commande },
            success: function (response) {
                if (response === "etat_1") {
                    // Si la commande est à l'état 0, continuer avec la requête pour livrer
                    livrerCommande(commande);
                } else {
                    // Sinon, afficher un message d'erreur dans la popup
                    document.getElementById("popupTitle").innerText = "Erreur";
                    document.getElementById("popupMessage").innerText = "Erreur lors de la vérification de la commande";
                    document.getElementById("icon").src = "../static/Contact/no_icon.png";
                     // Afficher la popup
                    popup.classList.add("popup-open");

                    // Fermer la popup après 2 secondes
                    setTimeout(function() {
                        closePopupagi();
                        window.location.reload();
                    }, 1000);

                }
            },
            error: function (xhr, status, error) {
                // Afficher une erreur en cas d'échec de la requête
                document.getElementById("popupTitle").innerText = "Erreur";
                document.getElementById("popupMessage").innerText = "Erreur lors de la vérification de la commande";
                document.getElementById("icon").src = "../static/Contact/no_icon.png";
                // Afficher la popup
                popup.classList.add("popup-open");

                // Fermer la popup après 2 secondes
                setTimeout(function() {
                    closePopupagi();
                    window.location.reload();
                }, 1000);

            }
        });
    }
}

function livrerCommande(commande) {
    // Effectuer une requête AJAX vers la route Python pour livrer la commande
    $.ajax({
        type: "POST",
        url: "/agilog_popup",
        data: { champ_texte: commande },
        success: function (response) {
            // Afficher la réponse dans la popup
            document.getElementById("popupTitle").innerText = "Validé";
            document.getElementById("popupMessage").innerText = response;
            document.getElementById("icon").src = "../static/Contact/ok_icon.png";
             // Afficher la popup
            popup.classList.add("popup-open");

            // Fermer la popup après 2 secondes
            setTimeout(function() {
                closePopupagi();
                window.location.reload();
            }, 1000);

        },
        error: function (xhr, status, error) {
            // Afficher une erreur en cas d'échec de la requête
            document.getElementById("popupTitle").innerText = "Erreur";
            document.getElementById("popupMessage").innerText = "Erreur lors de la livraison de la commande";
            document.getElementById("icon").src = "../static/Contact/no_icon.png";
             // Afficher la popup
            popup.classList.add("popup-open");

            // Fermer la popup après 2 secondes
            setTimeout(function() {
                closePopupagi();
                window.location.reload();
            }, 1000);

        }
    });
}

function closePopupagi() {
    let popup = document.getElementById("popup");
    popup.classList.remove("popup-open");
}
