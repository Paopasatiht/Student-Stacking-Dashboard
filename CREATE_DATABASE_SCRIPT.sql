CREATE DATABASE scim252_StudentStacks;

USE scim252_StudentStacks;

CREATE TABLE `Company` (
  `company_id` varchar(80) NOT NULL,
  `company_name` varchar(80) DEFAULT NULL,
  `company_location` varchar(80) DEFAULT NULL,
  `preference` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Courses` (
  `course_id` varchar(80) NOT NULL,
  `course_name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Enrollment` (
  `enroll_id` varchar(80) NOT NULL,
  `student_id` varchar(80) DEFAULT NULL,
  `stack_id` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`enroll_id`),
  KEY `student_id` (`student_id`),
  KEY `stack_id` (`stack_id`),
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Students` (`student_id`),
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`stack_id`) REFERENCES `Stacking` (`stack_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Lecturer` (
  `lecturer_id` varchar(80) NOT NULL,
  `fName` varchar(80) DEFAULT NULL,
  `lName` varchar(80) DEFAULT NULL,
  `uni_id` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`lecturer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Lecturer_Courses` (
  `session_id` varchar(80) NOT NULL,
  `lecturer_id` varchar(80) DEFAULT NULL,
  `course_id` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`session_id`),
  KEY `course_id` (`course_id`),
  KEY `lecturer_id` (`lecturer_id`),
  CONSTRAINT `lecturer_courses_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`),
  CONSTRAINT `lecturer_courses_ibfk_2` FOREIGN KEY (`lecturer_id`) REFERENCES `Lecturer` (`lecturer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Skill_Types` (
  `skill_id` varchar(80) NOT NULL,
  `skill_name` varchar(80) DEFAULT NULL,
  `skill_type` varchar(80) DEFAULT NULL,
  `skill_score` int DEFAULT NULL,
  PRIMARY KEY (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Stacking` (
  `stack_id` varchar(80) NOT NULL,
  `course_id` varchar(80) DEFAULT NULL,
  `skill_id` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`stack_id`),
  KEY `course_id` (`course_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `stacking_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`),
  CONSTRAINT `stacking_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `Skill_Types` (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Students` (
  `student_id` varchar(80) NOT NULL,
  `uni_id` varchar(80) DEFAULT NULL,
  `student_fName` varchar(80) DEFAULT NULL,
  `student_lName` varchar(80) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(80) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `preference` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  KEY `uni_id` (`uni_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`uni_id`) REFERENCES `University` (`uni_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `University` (
  `uni_id` varchar(80) NOT NULL,
  `uni_name` varchar(80) DEFAULT NULL,
  `uni_department` varchar(80) DEFAULT NULL,
  `uni_program` varchar(80) DEFAULT NULL,
  `uni_location` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`uni_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
