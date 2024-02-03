<?php
session_start();

// Vérification si le formulaire a été soumis
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nom_utilisateur = $_POST['username'];
    $nom = $_POST['nom'];
    $prenom = $_POST['prenom'];
    $email = $_POST['email'];
    $mot_de_passe = password_hash($_POST['mot_de_passe'], PASSWORD_DEFAULT);

    // Connexion à la base de données (à adapter à votre configuration)
    $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");

    // Vérification si le nom d'utilisateur est déjà utilisé
    $query = "SELECT id FROM utilisateurs WHERE nom_utilisateur = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$nom_utilisateur]);

    if ($stmt->fetch()) {
        // Nom d'utilisateur déjà utilisé, gérer l'erreur
        echo "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.";
    } else {
        // Nom d'utilisateur disponible, procéder à l'inscription
        $query = "INSERT INTO utilisateurs (nom_utilisateur, nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$nom_utilisateur, $nom, $prenom, $email, $mot_de_passe]);

        // Rediriger l'utilisateur vers la page de connexion
        header('Location: login.html');
    }
} else {
    // Si la soumission du formulaire n'est pas valide, gérer l'erreur
    echo "Soumission de formulaire non valide.";
}
?>