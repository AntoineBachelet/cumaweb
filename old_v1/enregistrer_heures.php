<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $heure_debut = $_POST['heure_debut'];
    $heure_fin = $_POST['heure_fin'];
    $commentaires = $_POST['commentaires'];
    $id_materiel = $_POST['id_materiel']; // Récupération de l'ID du matériel depuis la requête GET
    $utilisateur = $_SESSION['user']; // Récupération de l'ID de l'utilisateur connecté depuis la session

    // Connexion à la base de données (à adapter à votre configuration)
    $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");

    $query = "SELECT id FROM heures_utilisation WHERE id_materiel = ? 
          AND ((heure_debut >= ? AND heure_debut <= ?) OR (heure_fin > ? AND heure_fin <= ?))";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$id_materiel, $heure_debut, $heure_fin, $heure_debut, $heure_fin]);
    $existing_hours = $stmt->fetch();

    if ($existing_hours || $heure_fin == 0 || $heure_fin < $heure_debut) {
        header('Location: saisir_heures.php?id=' . $id_materiel . '&error=existing_hours');
        exit();
    } else {
        $query = "INSERT INTO heures_utilisation (heure_debut, heure_fin, id_materiel, utilisateur, commentaires) VALUES (?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$heure_debut, $heure_fin, $id_materiel, $utilisateur, $commentaires]);
        header('Location: liste_materiels.php');
    }
} else {
    echo "Soumission de formulaire non valide.";
}
?>