-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 10 jan. 2024 à 16:00
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `cuma_de_la_plaine`
--

-- --------------------------------------------------------

--
-- Structure de la table `heures_utilisation`
--

CREATE TABLE `heures_utilisation` (
  `ID` int(11) NOT NULL,
  `heure_debut` float NOT NULL,
  `heure_fin` float NOT NULL,
  `id_materiel` int(11) NOT NULL,
  `utilisateur` text NOT NULL,
  `commentaires` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `heures_utilisation`
--

INSERT INTO `heures_utilisation` (`ID`, `heure_debut`, `heure_fin`, `id_materiel`, `utilisateur`, `commentaires`) VALUES
(1, 120, 124, 2, 'admin', 'Test commentaire'),
(2, 124, 126, 2, 'admin', 'Test'),
(4, 126, 128, 2, 'admin', ''),
(5, 128, 129, 2, 'admin', ''),
(6, 129, 140, 2, 'admin', ''),
(8, 140, 142, 2, 'admin', ''),
(9, 142, 145, 2, 'admin', ''),
(10, 0, 10, 1, 'admin', ''),
(11, 10, 15, 1, 'admin', ''),
(12, 145, 149, 2, 'test', ''),
(13, 149, 154, 2, 'test', ''),
(14, 154, 156, 2, 'admin', '');

-- --------------------------------------------------------

--
-- Structure de la table `materiels`
--

CREATE TABLE `materiels` (
  `id` int(11) NOT NULL,
  `nom_materiel` varchar(100) DEFAULT NULL,
  `image_path` text DEFAULT NULL,
  `responsable` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `materiels`
--

INSERT INTO `materiels` (`id`, `nom_materiel`, `image_path`, `responsable`) VALUES
(1, 'Charrue', 'img/charrue.jpg', 'admin'),
(2, 'Déchaummeur', 'img/dechaummeur.png', 'admin');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `id` int(11) NOT NULL,
  `nom_utilisateur` varchar(255) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `nom_utilisateur`, `mot_de_passe`, `nom`, `prenom`, `email`) VALUES
(1, 'admin', '$2y$10$Y8LGrEdNgT1M6iEL7JH14.mBdUhDg/Yb0nYwFPHuOvIRRaImyVS0K', 'Bachelet', 'Antoine', 'a.bachelet708@gmail.com'),
(2, 'test', '$2y$10$HczOBqE99BrHAaCp3c/Zn.9adQ5SNNkt9Vrv7rhMvh5CSt81fMWR2', 'Squee', 'Zie', 'test@gmail.com');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `heures_utilisation`
--
ALTER TABLE `heures_utilisation`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `materiels`
--
ALTER TABLE `materiels`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `heures_utilisation`
--
ALTER TABLE `heures_utilisation`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `materiels`
--
ALTER TABLE `materiels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
