CREATE TABLE `collector` (
 `id` int(8) NOT NULL AUTO_INCREMENT,
 `protocol` varchar(4) NOT NULL,
 `src_address` varchar(128) NOT NULL,
 `bytes` int(10) NOT NULL,
 `packets` int(1) NOT NULL DEFAULT '1',
 `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci