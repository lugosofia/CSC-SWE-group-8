-- Table structure for table `answers`
CREATE TABLE `answers` (
  `answer_id` int NOT NULL AUTO_INCREMENT,
  `quest_id` int DEFAULT NULL,
  `answer_text` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `fk_answer_quest_id` (`quest_id`),
  CONSTRAINT `fk_answer_quest_id` FOREIGN KEY (`quest_id`) REFERENCES `questions` (`quest_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `polls` 
CREATE TABLE `polls` (
  `poll_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `description` varchar(400) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `quest_type` varchar(100) DEFAULT NULL,
  `creation` int DEFAULT NULL,
  PRIMARY KEY (`poll_id`),
  KEY `fk_user_poll_id` (`creation`) 
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `questions`
CREATE TABLE `questions` (
  `quest_id` int NOT NULL AUTO_INCREMENT,
  `poll_id` int DEFAULT NULL,
  `quest_txt` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`quest_id`),
  KEY `fk_quest_poll_id` (`poll_id`),
  CONSTRAINT `fk_quest_poll_id` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`poll_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `users` 
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_type` varchar(11) DEFAULT NULL,
  `f_name` varchar(45) DEFAULT NULL,
  `l_name` varchar(45) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `reg_date` date DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `votes`
CREATE TABLE `votes` (
  `vote_id` int NOT NULL AUTO_INCREMENT,
  `poll_id` int DEFAULT NULL,
  `answer_id` int DEFAULT NULL,
  `vote_timestamp` timestamp NULL DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`vote_id`),
  KEY `fk_votes_poll_id` (`poll_id`),
  KEY `fk_votes_user_id` (`user_id`),
  KEY `fk_votes_answer_id` (`answer_id`),
  CONSTRAINT `fk_votes_answer_id` FOREIGN KEY (`answer_id`) REFERENCES `answers` (`answer_id`),
  CONSTRAINT `fk_votes_poll_id` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`poll_id`),
  CONSTRAINT `fk_votes_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
