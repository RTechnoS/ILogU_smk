-- phpMyAdmin SQL Dump
-- version 4.6.6deb4+deb9u2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 14, 2020 at 11:50 PM
-- Server version: 10.3.23-MariaDB-0+deb10u1
-- PHP Version: 7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `covidtrack`
--

-- --------------------------------------------------------

--
-- Table structure for table `camera`
--

CREATE TABLE `camera` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `lokasi` text NOT NULL,
  `link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `camera`
--

INSERT INTO `camera` (`id`, `nama`, `lokasi`, `link`) VALUES
(1, 'Kelas XII TKJ 1', 'xiitkj1', 'videoContoh/ringan.mp4'),
(2, 'Kelas XII MM 1', 'xiimm1', 'videoContoh/ringan3.mp4');

-- --------------------------------------------------------

--
-- Table structure for table `dataSiswa`
--

CREATE TABLE `dataSiswa` (
  `id` int(11) NOT NULL,
  `nama` text NOT NULL,
  `kelas` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dataSiswa`
--

INSERT INTO `dataSiswa` (`id`, `nama`, `kelas`) VALUES
(1, 'Rusman Tobyakta Siregar', 'XII TKJ 1'),
(2, 'Bang Jago', 'XII TKJ 1'),
(3, 'Bang Jago', 'sadas'),
(4, 'dasdw3 ', '12sd3'),
(5, 'Cicak', 'XII MM 1');

-- --------------------------------------------------------

--
-- Table structure for table `logSiswa`
--

CREATE TABLE `logSiswa` (
  `id` int(11) NOT NULL,
  `nama` text NOT NULL DEFAULT 'unkown',
  `tanggal` date NOT NULL,
  `waktu` time NOT NULL,
  `lokasi` varchar(100) NOT NULL DEFAULT 'None',
  `terdekat` text DEFAULT NULL,
  `interaksi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `logSiswa`
--

INSERT INTO `logSiswa` (`id`, `nama`, `tanggal`, `waktu`, `lokasi`, `terdekat`, `interaksi`) VALUES
(1, 'Rusman', '2020-11-11', '00:05:14', 'rumah', 'None', 'None'),
(2, 'Rusman', '2020-11-15', '09:42:43', 'kantin1', 'riski, joni', 'jabatan'),
(53, 'Rusman', '2020-11-15', '10:46:38', 'kantin1', '', 'makan'),
(54, 'Rusman', '2020-11-15', '10:46:39', 'kantin1', '', 'makan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `camera`
--
ALTER TABLE `camera`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dataSiswa`
--
ALTER TABLE `dataSiswa`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `logSiswa`
--
ALTER TABLE `logSiswa`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `camera`
--
ALTER TABLE `camera`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `dataSiswa`
--
ALTER TABLE `dataSiswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `logSiswa`
--
ALTER TABLE `logSiswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=444;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
