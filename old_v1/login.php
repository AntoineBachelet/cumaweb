<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Vérification des informations d'identification
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Connexion à la base de données (à adapter à votre configuration)
    $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");

    // Sélection de l'utilisateur en fonction du nom d'utilisateur
    $query = "SELECT id, nom_utilisateur, mot_de_passe FROM utilisateurs WHERE nom_utilisateur = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    // Vérification du mot de passe
    if ($user && password_verify($password, $user['mot_de_passe'])) {
    // Informations d'identification correctes, démarrez une session
        $_SESSION['user'] = $username;
        $_SESSION['last_activity'] = time();
        header('Location: liste_materiels.php'); // Redirigez l'utilisateur vers la page de la liste de matériels
    } else {
        echo "Identifiant ou mot de passe incorrect.";
    }
}
?>