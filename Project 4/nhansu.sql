-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2023 at 02:55 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nhansu`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gmail` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID`, `username`, `password`, `gmail`) VALUES
(1, 'longaloso', '123', 'longaloso@gmail.com'),
(2, 'Phananh', '', 'phananh@gmail.com'),
(3, 'longaloso11', '123', 'long@gmail.com'),
(4, 'Long', '1', 'Longg@gmail.com'),
(5, 'Longxx', '1280', 'Lonxx@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `danhsachthuctap`
--

CREATE TABLE `danhsachthuctap` (
  `ID` int(11) NOT NULL,
  `Ten` varchar(255) NOT NULL,
  `Cc` int(255) NOT NULL,
  `Tuoi` varchar(255) NOT NULL,
  `home` varchar(255) NOT NULL,
  `Sdt` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `danhsachthuctap`
--

INSERT INTO `danhsachthuctap` (`ID`, `Ten`, `Cc`, `Tuoi`, `home`, `Sdt`) VALUES
(1, 'Ngô Văn Long', 22201212, '18', 'CEO', '0344760203'),
(14, 'Đinh Quang Chung', 2221212, '21', 'gg', '332');

-- --------------------------------------------------------

--
-- Table structure for table `quanlynhansu`
--

CREATE TABLE `quanlynhansu` (
  `ID` int(11) NOT NULL,
  `Ten` varchar(255) NOT NULL,
  `Cc` int(255) NOT NULL,
  `Ngaysinh` date NOT NULL,
  `Que` varchar(255) NOT NULL,
  `Sdt` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quanlynhansu`
--

INSERT INTO `quanlynhansu` (`ID`, `Ten`, `Cc`, `Ngaysinh`, `Que`, `Sdt`) VALUES
(1, 'Longgg', 22122222, '2004-08-08', 'Hà Nộiii', '0344760203');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `danhsachthuctap`
--
ALTER TABLE `danhsachthuctap`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `quanlynhansu`
--
ALTER TABLE `quanlynhansu`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `danhsachthuctap`
--
ALTER TABLE `danhsachthuctap`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `quanlynhansu`
--
ALTER TABLE `quanlynhansu`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
