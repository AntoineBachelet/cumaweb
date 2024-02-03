<?php
require __DIR__ . '/../vendor/autoload.php';

// Récupérez les données sérialisées des heures d'utilisation depuis le paramètre GET
if (isset($_GET['data'])) {
    $data = unserialize(base64_decode($_GET['data']));
    $heures_utilisation = $data;
} else {
    // Gérer le cas où les données ne sont pas transmises correctement
    die('Erreur : Les données ne sont pas disponibles.');
}
$nom_materiel = "default";
if (isset($_GET['nom'])) {
    $nom_materiel = $_GET["nom"];
}

// ... Le code pour se connecter à la base de données et récupérer les données (similaire à ce que vous avez dans votre page principale)

// Créez un nouveau document Excel
$spreadsheet = new \PhpOffice\PhpSpreadsheet\Spreadsheet();

// Sélectionnez la feuille de calcul active
$sheet = $spreadsheet->getActiveSheet();

// Définissez les en-têtes des colonnes
$sheet->setCellValue('A1', 'Nom Prénom');
$sheet->setCellValue('B1', 'Heure de début');
$sheet->setCellValue('C1', 'Heure de fin');
$sheet->setCellValue('D1', 'Différence');
$sheet->setCellValue('E1', 'Nom');
$sheet->setCellValue('F1', 'Total Heures par Personne');

// Remplissez les données à partir de la base de données
for ($i = 0; $i < count($heures_utilisation); $i++) {
    // Ajoutez une colonne "Nom Prénom" à heures_utilisation
    $heures_utilisation[$i]['nom_complet'] = $heures_utilisation[$i]["nom"] . ' ' . $heures_utilisation[$i]["prenom"];

    $sheet->setCellValue('A' . ($i + 2), $heures_utilisation[$i]['nom_complet']);
    $sheet->setCellValue('B' . ($i + 2), $heures_utilisation[$i]["heure_debut"]);
    $sheet->setCellValue('C' . ($i + 2), $heures_utilisation[$i]["heure_fin"]);
    $sheet->setCellValue('D' . ($i + 2), $heures_utilisation[$i]["heure_fin"]-$heures_utilisation[$i]["heure_debut"]);
}

// Ajouter une colonne pour la formule Excel
$sheet->setCellValue('E1', 'Nom');
$sheet->setCellValue('F1', 'Total Heures par Personne');

// Identifier les noms distincts dans la colonne "Nom Prénom"
$distinct_names = array_unique(array_column($heures_utilisation, 'nom_complet'));

// Ajouter la formule SUMIFS pour chaque "Nom Prénom" distinct
$row = 2;
foreach ($distinct_names as $name) {
    $sheet->setCellValue('E' . $row, '=A' . $row);
    $sheet->setCellValue('F' . $row, '=SUMIFS(D:D, A:A, "' . $name . '")');
    $row++;
}

$today = date('Y-m-d');
$formattedDate = date_create_from_format('Y-m-d', $today)->format('d_m_Y');

// Définissez les en-têtes HTTP pour forcer le téléchargement du fichier
header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
header('Content-Disposition: attachment;filename="'.$nom_materiel."_".$formattedDate.'.xlsx"');
header('Cache-Control: max-age=0');

// Créez un écrivain pour sauvegarder le fichier Excel
$writer = new \PhpOffice\PhpSpreadsheet\Writer\Xlsx($spreadsheet);

// Sauvegardez le fichier Excel dans la sortie HTTP
$writer->save('php://output');
exit();
?>