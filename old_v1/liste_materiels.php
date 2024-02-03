<!DOCTYPE html>
<html>
<head>
    <title>Liste de Matériels</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css">
    <style>
        .card {
            height: 100%;
        }

        .card-title {
            margin-top: auto;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Liste des matériels de la Cuma</h1>
        <div class="row">
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
            // Connexion à la base de données (à adapter à votre configuration)
            $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");

            // Récupération des informations sur les matériels
            $query = "SELECT id, nom_materiel, image_path FROM materiels";
            $stmt = $pdo->query($query);
            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $materiel_id = $row['id'];
                $nom_materiel = $row['nom_materiel'];
                $image = $row['image_path'];

                echo '<div class="col-md-3 mb-3">';
                echo '<a href="saisir_heures.php?id=' . $materiel_id . '" class="card text-decoration-none">'; // Ajout de la classe et enveloppement dans un élément <a>
                echo '<img src="' . $image . '" class="card-img-top" alt="' . $nom_materiel . '">';
                echo '<div class="card-body d-flex flex-column">';
                echo '<h5 class="card-title text-center mt-auto">' . $nom_materiel . '</h5>'; // Alignement avec le bas de la carte
                echo '</div>';
                echo '</a>';
                echo '</div>';
            }
            ?>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>