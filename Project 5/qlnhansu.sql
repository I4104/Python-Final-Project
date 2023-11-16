-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2023 at 07:31 AM
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
-- Database: `qlnhansu`
--

-- --------------------------------------------------------

--
-- Table structure for table `quanlycongviec`
--

CREATE TABLE `quanlycongviec` (
  `ID` int(11) NOT NULL,
  `Ten` varchar(255) NOT NULL,
  `soluongnhanluc` int(255) NOT NULL,
  `Tuoi` varchar(255) NOT NULL,
  `mucluong` varchar(255) NOT NULL,
  `thoigian` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quanlycongviec`
--

INSERT INTO `quanlycongviec` (`ID`, `Ten`, `soluongnhanluc`, `Tuoi`, `mucluong`, `thoigian`) VALUES
(1, 'User22', 2147483647, '1822', 'CEO22', '029232');

-- --------------------------------------------------------

--
-- Table structure for table `quanlynhansu`
--

CREATE TABLE `quanlynhansu` (
  `ID` int(11) NOT NULL,
  `Ten` varchar(255) NOT NULL,
  `Cc` int(255) NOT NULL,
  `Ngaysinh` date NOT NULL,
  `Nganh` varchar(255) NOT NULL,
  `Sdt` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quanlynhansu`
--

INSERT INTO `quanlynhansu` (`ID`, `Ten`, `Cc`, `Ngaysinh`, `Nganh`, `Sdt`) VALUES
(1, 'user', 2147483647, '2004-08-01', 'Hà Nộiii22', '034476020322');

-- --------------------------------------------------------

--
-- Table structure for table `taikhoan`
--

CREATE TABLE `taikhoan` (
  `ID` int(11) NOT NULL,
  `tendangnhap` varchar(255) NOT NULL,
  `matkhau` varchar(255) NOT NULL,
  `gmail` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `taikhoan`
--

INSERT INTO `taikhoan` (`ID`, `tendangnhap`, `matkhau`, `gmail`) VALUES
(8, 'longxa', '123', 'longcsc@gmail.com'),
(9, 'longxaqq', '212', 'longalos222o@gmail.com'),
(10, 'longxaxx', '123', 'longaloso@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `quanlycongviec`
--
ALTER TABLE `quanlycongviec`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `quanlynhansu`
--
ALTER TABLE `quanlynhansu`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `quanlycongviec`
--
ALTER TABLE `quanlycongviec`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `quanlynhansu`
--
ALTER TABLE `quanlynhansu`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `taikhoan`
--
ALTER TABLE `taikhoan`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
