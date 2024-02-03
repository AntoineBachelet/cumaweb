<!DOCTYPE html>
<html>
<head>
    <title>Gestion du Matériel</title>
    <!-- Inclure les fichiers CSS de Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <?php
        session_start();
        if (isset($_SESSION['user'])) {
            if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity'] > 180)) {
                session_unset();
                session_destroy();
                header("Location: login.html");
            }
            $_SESSION['last_activity'] = time();
        }else{
            header('Location: login.html');
            exit();
        }

        if (isset($_GET['id'])) {
            $id_materiel = $_GET['id'];
        }
        $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");
        $query = "SELECT * FROM materiels WHERE id = ?";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$id_materiel]);
        $data = $stmt->fetch();

        $query = "SELECT h.*, u.nom, u.prenom FROM heures_utilisation h
                JOIN utilisateurs u ON h.utilisateur = u.nom_utilisateur
                WHERE h.id_materiel = ?
                ORDER BY h.heure_debut ASC";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$id_materiel]);
        $heures_utilisation = $stmt->fetchAll();
    ?>
    <header>
        <!-- En-tête de la page -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Gestion du Matériel</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="liste_materiels.php">Retour à la liste de matériel</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="deconnexion.php">Déconnexion</a>
                    </li>
                </ul>
            </div>
        </nav>
    </header>

    <main class="container">
        <!-- Contenu principal de la page -->
        <h3 class="card-title"><?php echo $data["nom_materiel"]; ?></h3>

        <div class="mt-3">
            <h4>Heures d'utilisation du matériel</h4>
            <ul>
                <?php foreach ($heures_utilisation as $heure) { ?>
                    <li>
                    <strong><?php echo $heure["nom"] . " " . $heure["prenom"]; ?>:</strong>
                    <?php echo $heure["heure_debut"] . " / " . $heure["heure_fin"]; ?>
                    <!-- Ajoutez d'autres informations relatives aux heures ici -->
                </li>
                <?php } ?>
            </ul>
        </div>

        <!-- Ajoutez des fonctionnalités pour gérer le matériel, comme la modification ou la suppression -->
        <div class="mt-3">
            <a href="modifier_materiel.php?id=[ID du Matériel]" class="btn btn-primary">Modifier le Matériel</a>
            <a href="supprimer_materiel.php?id=[ID du Matériel]" class="btn btn-danger">Supprimer le Matériel</a>
            <!-- Ajoutez d'autres actions ici -->
        </div>
        <div class="mt-3">
            <a href="export_excel.php?nom=<?php echo $data["nom_materiel"]; ?>&data=<?php echo base64_encode(serialize($heures_utilisation)); ?>" class="btn btn-success">Exporter vers Excel</a>
        </div>
    </main>

    <!-- Inclure les fichiers JavaScript de Bootstrap (facultatif) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>