<!DOCTYPE html>
<html>
<head>
    <title>Saisir Heures</title>
    <meta charset="UTF-8">
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body><?php 
        if (isset($_GET['id'])) {
            $id_materiel = $_GET['id'];
        }
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
        if (isset($_GET['error']) && $_GET['error'] === 'existing_hours') {
            echo '<div class="alert alert-danger">Les heures rentrées ne peuvent pas être enregistrées, veuillez en saisir d\'autres ou contacter le responsable du matériel.</div>';
        }
        $pdo = new PDO("mysql:host=localhost;dbname=cuma_de_la_plaine", "root", "");
        $query = "SELECT MAX(heure_fin) AS derniere_heure_fin FROM heures_utilisation WHERE id_materiel = ?";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$id_materiel]);
        $last_hour = $stmt->fetch();

        // Définir la valeur par défaut de l'heure de début
        $default_heure_debut = ($last_hour['derniere_heure_fin']) ? $last_hour['derniere_heure_fin'] : 0;
    ?>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        
                        <h2 class="card-title text-center">Saisir Heures d'Utilisation</h2>
                        <form action="enregistrer_heures.php" id="formulaireEnvoi" method="post">
                            <input type="hidden" name="id_materiel" value="<?php echo $id_materiel; ?>">
                            <div class="mb-3">
                                <label for="heure_debut">Heure de Début :</label>
                                <input type="number" class="form-control" name="heure_debut" id="heure_debut" step="0.01" value="<?php echo $default_heure_debut; ?>" required>
                            </div>
                            <div class="mb-3">
                                <label for="heure_fin">Heure de Fin :</label>
                                <input type="number" class="form-control" name="heure_fin" id="heure_fin" step="0.01" required>
                            </div>
                            <div id="total_heures">Total des heures : 0.00 heures</div>
                            <div class="mb-3">
                                <label for="commentaires">Commentaires :</label>
                                <textarea class="form-control" name="commentaires" id="commentaires" rows="4"></textarea>
                            </div>                            
                        </form>
                        <div class="text-center">
                            <button id="confirmButton" class="btn btn-primary">Valider</button>
                        </div>
                        <div class="text-center">
                            <?php
                            $query = "SELECT responsable FROM materiels WHERE id = ?";
                            $stmt = $pdo->prepare($query);
                            $stmt->execute([$id_materiel]);
                            $responsable = $stmt->fetch();
                            if ($_SESSION['user'] === $responsable["responsable"]) {
                                echo '<a href="responsable_materiel.php?id=' . $id_materiel . '" class="btn btn-success">Gestion du matériel</a>';
                            }
                            ?>
                        </div>
                        
                    </div>
                </div>
                <div id="confirmationModal" class="modal" style="display: none;">
                    <div class="modal-content">
                        <h3>Confirmation</h3>
                        <p>Voulez-vous enregistrer ces heures ?</p>
                        <p id="total_heures_modal">Total des heures : 0.00 heures</p>
                        <button id="cancelButton" class="btn btn-secondary">Annuler</button>
                        <button id="confirmSaveButton" class="btn btn-primary">Valider</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        $(document).ready(function() {
            // Sélectionnez les champs d'heure de début et de fin
            var $heure_debut = $('#heure_debut');
            var $heure_fin = $('#heure_fin');
            
            // Sélectionnez l'élément où vous afficherez le total
            var $total_heures = $('#total_heures');
            var $total_heures_modal = $('#total_heures_modal');
            
            // Fonction pour mettre à jour le total
            function updateTotal() {
                var heureDebut = parseFloat($heure_debut.val()) || 0;
                var heureFin = parseFloat($heure_fin.val()) || 0;
                var totalHeures = heureFin - heureDebut;
                if (totalHeures < 0){
                    totalHeures = 0
                }
                
                $total_heures.text('Total des heures : ' + totalHeures.toFixed(2) + ' heures');
                $total_heures_modal.text('Total des heures : ' + totalHeures.toFixed(2) + ' heures');
            }
            
            // Écoutez les changements dans les champs d'heure de début et de fin
            $heure_debut.on('input', updateTotal);
            $heure_fin.on('input', updateTotal);
            updateTotal();
            $('#confirmButton').click(function() {
                $('#confirmationModal').show();
            });
            $('#cancelButton').click(function() {
                $('#confirmationModal').hide();
            });
            $('#confirmSaveButton').click(function() {
                var heureDebut = parseFloat($heure_debut.val()) || 0;
                var heureFin = parseFloat($heure_fin.val()) || 0;
                $('#formulaireEnvoi').submit();
            });
        });
        </script>
</body>
</html>