CREATE DATABASE IF NOT EXISTS `web_cms_database`;

USE `web_cms_database`;

-- LOGIN
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    middle_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    user_role VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
);

CREATE TABLE IF NOT EXISTS `appointment` (
	`reference_number` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`receptionistID` INT(10) NOT NULL,
	`doctorID` INT(10) NOT NULL,
	`doctorName` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`date_appointment` DATE NULL DEFAULT NULL,
	`time_appointment` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`status_` VARCHAR(20) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`book_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`first_name` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`middle_name` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_name` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`sex` VARCHAR(10) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`birth_date` DATE NULL DEFAULT NULL,
	`contact_number` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`email` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`address` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`date_updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`date_created` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`reference_number`) USING BTREE,
	UNIQUE INDEX `ref_number_uniq` (`reference_number`) USING BTREE,
	INDEX `receptionistID` (`receptionistID`) USING BTREE,
	INDEX `doctorID` (`doctorID`) USING BTREE,
	CONSTRAINT `fk_appointment_doctor` FOREIGN KEY (`doctorID`) REFERENCES `users` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT `fk_appointment_receptionist` FOREIGN KEY (`receptionistID`) REFERENCES `users` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;


CREATE TABLE IF NOT EXISTS `schedule` (
    `scheduleID` INT NOT NULL AUTO_INCREMENT,
    `date_appointment` DATE,
    `time_appointment`  VARCHAR(30) NOT NULL,
    `slots` INT NOT NULL,
    `doctorID` INT(10) NOT NULL,
    `doctorName` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',	
    UNIQUE INDEX `schedule_id_UNIQUE` (`scheduleID`) USING BTREE,
    PRIMARY KEY (`scheduleID`) USING BTREE,
    INDEX `doctorID` (`doctorID`) USING BTREE,
    CONSTRAINT `fk_schedule_doctor` FOREIGN KEY (`doctorID`) REFERENCES `users` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
) COLLATE='utf8mb4_0900_ai_ci' ENGINE=InnoDB;

-- PATIENT INFORMATION
CREATE TABLE IF NOT EXISTS `patientinfo` (
    `patientID` INT NOT NULL AUTO_INCREMENT,
    `firstName` VARCHAR(50) NOT NULL,
    `midName` VARCHAR(50) NOT NULL,
    `lastName` VARCHAR(50) NOT NULL,
    `age` INT NOT NULL,
    `civilStatus` VARCHAR(20) NOT NULL,
    `gender` VARCHAR(10) NOT NULL,
    `bloodType` VARCHAR(10) NOT NULL,
    `birthPlace` VARCHAR(100) NOT NULL,
    `birthDate` DATE NOT NULL,
    `p_address` VARCHAR(255) NOT NULL,
    `nationality` VARCHAR(20) NOT NULL,
    `religion` VARCHAR(50) NOT NULL,
    `eContactName` VARCHAR(20) NOT NULL,
    `relationship` VARCHAR(20) NOT NULL,
    `eContactNum` VARCHAR(20) NOT NULL,
    `occupation` VARCHAR(50) NOT NULL,
    `p_email` VARCHAR(50) NOT NULL,
    `p_contactNum` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`patientID`),
    UNIQUE KEY `patient_id_UNIQUE` (`patientID`)
);

-- DOCTOR-PATIENT RELATION
CREATE TABLE IF NOT EXISTS `docpatient_relation` (
    `relationID` INT NOT NULL AUTO_INCREMENT,
    `doctorID` INT NOT NULL,
    `patientID` INT NOT NULL,
    PRIMARY KEY (`relationID`),
    UNIQUE KEY `relation_id_UNIQUE` (`relationID`),
    FOREIGN KEY (`doctorID`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`patientID`) REFERENCES `patientinfo` (`patientID`) ON DELETE CASCADE
);

-- MEDICAL HISTORY
CREATE TABLE IF NOT EXISTS `medicalhistory` (
    `historyID` INT NOT NULL AUTO_INCREMENT,
    `patientID` INT NOT NULL,
    `bcgCheckbox` BOOLEAN,
    `dtpCheckbox` BOOLEAN,
    `pcvCheckbox` BOOLEAN,
    `influenzaCheckbox` BOOLEAN,
    `hepaCheckbox` BOOLEAN,
    `ipvCheckbox` BOOLEAN,
    `mmrCheckbox` BOOLEAN,
    `hpvCheckbox` BOOLEAN,
    `asthmaCheckbox` BOOLEAN,
    `diabetesCheckbox` BOOLEAN,
    `heartCheckbox` BOOLEAN,
    `birthCheckbox` BOOLEAN,
    `boneCheckbox` BOOLEAN,
    `alzheimerCheckbox` BOOLEAN,
    `cancerCheckbox` BOOLEAN,
    `thyroidCheckbox` BOOLEAN,
    `tuberculosisCheckbox` BOOLEAN,
    `eyeCheckbox` BOOLEAN,
    `clotsCheckbox` BOOLEAN,
    `mentalCheckbox` BOOLEAN,
    `kidneyCheckbox` BOOLEAN,
    `anemiaCheckbox` BOOLEAN,
    `muscleCheckbox` BOOLEAN,
    `highbloodCheckbox` BOOLEAN,
    `epilepsyCheckbox` BOOLEAN,
    `skinCheckbox` BOOLEAN,
    `hivCheckbox` BOOLEAN,
    `pulmonaryCheckbox` BOOLEAN,
    `specifications` TEXT,
    `others` TEXT,
    `past_c1` VARCHAR(255),
    `medication1` VARCHAR(255),
    `dosage1` VARCHAR(255),
    `h_date1` DATE,
    `past_c2` VARCHAR(255),
    `medication2` VARCHAR(255),
    `dosage2` VARCHAR(255),
    `h_date2` DATE,
    `past_c3` VARCHAR(255),
    `medication3` VARCHAR(255),
    `dosage3` VARCHAR(255),
    `h_date3` DATE,
    `habitually` VARCHAR(10),
    `yearsDrunk` INT,
    `frequencyDrink` VARCHAR(255),
    `quitDrinking` INT,
    `frequently` VARCHAR(10),
    `yearsSmoked` INT,
    `frequencySmoke` VARCHAR(255),
    `quitSmoking` INT,
    `often` VARCHAR(10),
    `exerciseType` VARCHAR(255),
    `frequencyExercise` VARCHAR(255),
    `durationActivity` VARCHAR(255),
    `sexActive` VARCHAR(10),
    `sexPartner` VARCHAR(10),
    `numSexPartner` INT,
    `contraception` VARCHAR(255),
    `useDrugs` VARCHAR(10),
    `specifyDrugs` VARCHAR(255),
    `frequencyDrugs` VARCHAR(255),
    `surgeryDate1` DATE,
    `surgeryProcedure1` VARCHAR(255),
    `hospital1` TEXT,
    `surgeryDate2` DATE,
    `surgeryProcedure2` VARCHAR(255),
    `hospital2` TEXT,
    `surgeryDate3` DATE,
    `surgeryProcedure3` VARCHAR(255),
    `hospital3` TEXT,
    `medications` TEXT,
    `allergies` TEXT,
    PRIMARY KEY (`historyID`),
    UNIQUE KEY `history_id_UNIQUE` (`historyID`),
    FOREIGN KEY (`patientID`) REFERENCES `patientinfo` (`patientID`) ON DELETE CASCADE
);

-- MEDICAL ASSESSMENT
CREATE TABLE IF NOT EXISTS `assessment` (
    `assessmentID` INT NOT NULL AUTO_INCREMENT,
    `patientID` INT NOT NULL,
    `subject` VARCHAR(255) NOT NULL,
    `complaints` TEXT,
    `illnessHistory` VARCHAR(255),
    `bloodPressure` VARCHAR(100),
    `pulseRate` VARCHAR(100),
    `temperature` VARCHAR(100),
    `respRate` VARCHAR(100),
    `height` VARCHAR(50),
    `weight` VARCHAR(50),
    `bmi` VARCHAR(50),
    `normal_head` VARCHAR(50),
    `abnormalities_head` VARCHAR(255),
    `normal_ears` VARCHAR(50),
    `abnormalities_ears` VARCHAR(255),
    `normal_eyes` VARCHAR(50),
    `abnormalities_eyes` VARCHAR(255),
    `normal_nose` VARCHAR(50),
    `abnormalities_nose` VARCHAR(255),
    `normal_skin` VARCHAR(50),
    `abnormalities_skin` VARCHAR(255),
    `normal_back` VARCHAR(50),
    `abnormalities_back` VARCHAR(255),
    `normal_neck` VARCHAR(50),
    `abnormalities_neck` VARCHAR(255),
    `normal_throat` VARCHAR(50),
    `abnormalities_throat` VARCHAR(255),
    `normal_chest` VARCHAR(50),
    `abnormalities_chest` VARCHAR(255),
    `normal_abdomen` VARCHAR(50),
    `abnormalities_abdomen` VARCHAR(255),
    `normal_upper` VARCHAR(50),
    `abnormalities_upper` VARCHAR(255),
    `normal_lower` VARCHAR(50),
    `abnormalities_lower` VARCHAR(255),
    `normal_tract` VARCHAR(50),
    `abnormalities_tract` VARCHAR(255),
    `comments` TEXT,
    `diagnosis` TEXT,
    `consultationDate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`assessmentID`),
    UNIQUE KEY `assessment_id_UNIQUE` (`assessmentID`),
    FOREIGN KEY (`patientID`) REFERENCES `patientinfo` (`patientID`) ON DELETE CASCADE
);

-- PRESCRIPTION 
CREATE TABLE IF NOT EXISTS `prescription` (
    `prescriptionID` INT NOT NULL AUTO_INCREMENT,
    `assessmentID` INT NOT NULL,
    PRIMARY KEY (`prescriptionID`),
    UNIQUE KEY `prescription_id_UNIQUE` (`prescriptionID`),
    FOREIGN KEY (`assessmentID`) REFERENCES `assessment` (`assessmentID`) ON DELETE CASCADE
);

-- PRESCRIPTION DETAILS 
CREATE TABLE IF NOT EXISTS `prescriptiondetails` (
    `detail_id` INT NOT NULL AUTO_INCREMENT,
    `prescriptionID` INT NOT NULL,
    `medication_name` VARCHAR(255),
    `dosage` VARCHAR(255),
    `p_quantity` VARCHAR(255),
    `duration` VARCHAR(255),
    `instructions` VARCHAR(255),
    PRIMARY KEY (`detail_id`),
    UNIQUE KEY `detail_id_UNIQUE` (`detail_id`),
    FOREIGN KEY (`prescriptionID`) REFERENCES `prescription` (`prescriptionID`) ON DELETE CASCADE
);

-- LABORATORY JOB ORDER
CREATE TABLE IF NOT EXISTS `labrequest` (
    `orderID` INT NOT NULL AUTO_INCREMENT,
    `patientID` INT NOT NULL,
    `patientName` VARCHAR(255) NOT NULL,
    `labSubject` VARCHAR(255) NOT NULL,
    `gender` VARCHAR(10) NOT NULL,
    `age` VARCHAR(10) NOT NULL,
    `physician` VARCHAR(255) NOT NULL,
    `orderDate` DATE NOT NULL,
    `otherTest` VARCHAR(255),
    PRIMARY KEY (`orderID`),
    UNIQUE KEY `order_id_UNIQUE` (`orderID`),
    FOREIGN KEY (`patientID`) REFERENCES `patientinfo` (`patientID`) ON DELETE CASCADE
);


-- HEMATOLOGY
CREATE TABLE IF NOT EXISTS `hematology` (
    `hematologyID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `cbcplateCheckbox` BOOLEAN,
    `hgbhctCheckbox` BOOLEAN,
    `protimeCheckbox` BOOLEAN,
    `APTTCheckbox` BOOLEAN,
    `bloodtypingCheckbox` BOOLEAN,
    `ESRCheckbox` BOOLEAN,
    `plateCheckbox` BOOLEAN,
    `hgbCheckbox` BOOLEAN,
    `hctCheckbox` BOOLEAN,
    `cbcCheckbox` BOOLEAN,
    `reticsCheckbox` BOOLEAN,
    `CTBTCheckbox` BOOLEAN,
    PRIMARY KEY (`hematologyID`),
    UNIQUE KEY `hematology_id_UNIQUE` (`hematologyID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- BACTERIOLOGY
CREATE TABLE IF NOT EXISTS `bacteriology` (
    `bacteriologyID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `culsenCheckbox` BOOLEAN,
    `cultureCheckbox` BOOLEAN,
    `gramCheckbox` BOOLEAN,
    `KOHCheckbox` BOOLEAN,
    PRIMARY KEY (`bacteriologyID`),
    UNIQUE KEY `bacteriology_id_UNIQUE` (`bacteriologyID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- HISTOPATHOLOGY
CREATE TABLE IF NOT EXISTS `histopathology` (
    `histopathologyID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `biopsyCheckbox` BOOLEAN,
    `papsCheckbox` BOOLEAN,
    `FNABCheckbox` BOOLEAN,
    `cellCheckbox` BOOLEAN,
    `cytolCheckbox` BOOLEAN,
    PRIMARY KEY (`histopathologyID`),
    UNIQUE KEY `histopathology_id_UNIQUE` (`histopathologyID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- CLINICAL MIRCROSCOPY & PARASITOLOGY
CREATE TABLE IF NOT EXISTS `microscopy` (
    `microscopyID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `urinCheckbox` BOOLEAN,
    `stoolCheckbox` BOOLEAN,
    `occultCheckbox` BOOLEAN,
    `semenCheckbox` BOOLEAN,
    `ELISACheckbox` BOOLEAN,
    PRIMARY KEY (`microscopyID`),
    UNIQUE KEY `microscopy_id_UNIQUE` (`microscopyID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- SEROLOGY
CREATE TABLE IF NOT EXISTS `serology` (
    `serologyID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `ASOCheckbox` BOOLEAN,
    `AntiHBSCheckbox` BOOLEAN,
    `HCVCheckbox` BOOLEAN,
    `C3Checkbox` BOOLEAN,
    `HIVICheckbox` BOOLEAN,
    `HIVIICheckbox` BOOLEAN,
    `NS1Checkbox` BOOLEAN,
    `VDRLCheckbox` BOOLEAN,
    `PregCheckbox` BOOLEAN,
    `RFCheckbox` BOOLEAN,
    `QuantiCheckbox` BOOLEAN,
    `QualiCheckbox` BOOLEAN,
    `TyphidotCheckbox` BOOLEAN,
    `TubexCheckbox` BOOLEAN,
    `HAVIgMCheckbox` BOOLEAN,
    `DengueCheckbox` BOOLEAN,
    PRIMARY KEY (`serologyID`),
    UNIQUE KEY `serology_id_UNIQUE` (`serologyID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- IMMUNOCHEMISTRY
CREATE TABLE IF NOT EXISTS `immunochem` (
    `immunochemID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `AFPCheckbox` BOOLEAN,
    `ferritinCheckbox` BOOLEAN,
    `HBcIgMCheckbox` BOOLEAN,
    `AntiHBECheckbox` BOOLEAN,
    `CA125Checkbox` BOOLEAN,
    `PROBNPCheckbox` BOOLEAN,
    `CA153Checkbox` BOOLEAN,
    `CA199Checkbox` BOOLEAN,
    `PSACheckbox` BOOLEAN,
    `CEACheckbox` BOOLEAN,
    `FreeT3Checkbox` BOOLEAN,
    `ANA2Checkbox` BOOLEAN,
    `FreeT4Checkbox` BOOLEAN,
    `HBsAGCheckbox` BOOLEAN,
    `TroponiniCheckbox` BOOLEAN,
    `HbACheckbox` BOOLEAN,
    `HBAeAgCheckbox` BOOLEAN,
    `BetaCheckbox` BOOLEAN,
    `T3Checkbox` BOOLEAN,
    `T4Checkbox` BOOLEAN,
    `TSHCheckbox` BOOLEAN,
    PRIMARY KEY (`immunochemID`),
    UNIQUE KEY `immunochem_id_UNIQUE` (`immunochemID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- CLINICAL CHEMISTRY
CREATE TABLE IF NOT EXISTS `clinicalchem` (
    `clinicalchemID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `ALPCheckbox` BOOLEAN,
    `AmylaseCheckbox` BOOLEAN,
    `BUACheckbox` BOOLEAN,
    `BUNCheckbox` BOOLEAN,
    `CreatinineCheckbox` BOOLEAN,
    `SGPTCheckbox` BOOLEAN,
    `SGOTCheckbox` BOOLEAN,
    `FBSCheckbox` BOOLEAN,
    `RBSCheckbox` BOOLEAN,
    `HPPCheckbox` BOOLEAN,
    `OGCTCheckbox` BOOLEAN,
    `HGTCheckbox` BOOLEAN,
    `OGTTCheckbox` BOOLEAN,
    `NaCheckbox` BOOLEAN,
    `MgCheckbox` BOOLEAN,
    `LipidCheckbox` BOOLEAN,
    `TriglyCheckbox` BOOLEAN,
    `CholCheckbox` BOOLEAN,
    `ClCheckbox` BOOLEAN,
    `TPAGCheckbox` BOOLEAN,
    `TotalCheckbox` BOOLEAN,
    `GlobCheckbox` BOOLEAN,
    `AlbCheckbox` BOOLEAN,
    `CKMBCheckbox` BOOLEAN,
    `CKTotalCheckbox` BOOLEAN,
    `LDHCheckbox` BOOLEAN,
    `KCheckbox` BOOLEAN,
    `CaCheckbox` BOOLEAN,
    `IonizedCheckbox` BOOLEAN,
    `PhosCheckbox` BOOLEAN,
    PRIMARY KEY (`clinicalchemID`),
    UNIQUE KEY `clinicalchem_id_UNIQUE` (`clinicalchemID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- LABORATORY REPORT
CREATE TABLE IF NOT EXISTS `labreport` (
    `reportID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `medtech` VARCHAR(255) NOT NULL,
    `reportDate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`reportID`),
    UNIQUE KEY `report_id_UNIQUE` (`reportID`),
    FOREIGN KEY (`orderID`) REFERENCES `labrequest` (`orderID`) ON DELETE CASCADE
);

-- LABORATORY TEST RESULTS
CREATE TABLE IF NOT EXISTS `labtest` (
    `testID` INT NOT NULL AUTO_INCREMENT,
    `reportID` INT NOT NULL,
    `processName` VARCHAR(255) NOT NULL,
    `testResult` VARCHAR(255) NOT NULL,
    `refValue` VARCHAR(255) NOT NULL,
    `diagnosisReport` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`testID`),
    UNIQUE KEY `test_id_UNIQUE` (`testID`),
    FOREIGN KEY (`reportID`) REFERENCES `labreport` (`reportID`) ON DELETE CASCADE
);
