<?php
// Initialisation de la session
session_start();

// Déconnexion de l'utilisateur
unset($_SESSION['user_id']); // Supprimez l'ID de l'utilisateur ou toute autre donnée de session que vous utilisez

// Destruction de la session
session_destroy();

// Redirection vers la page de connexion ou une autre page de votre choix
header('Location: login.html'); // Vous pouvez remplacer "login.php" par la page vers laquelle vous souhaitez rediriger après la déconnexion
exit();
?>