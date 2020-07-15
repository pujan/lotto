BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `superszansa` (
	`system_id`	INTEGER NOT NULL UNIQUE,
	`date`	DATE NOT NULL,
	`numbers`	varchar ( 20 ) NOT NULL,
	PRIMARY KEY(`system_id`)
);
CREATE TABLE IF NOT EXISTS `lottoplus` (
	`system_id`	INTEGER NOT NULL UNIQUE,
	`date`	DATE NOT NULL,
	`numbers`	VARCHAR ( 20 ) NOT NULL,
	PRIMARY KEY(`system_id`)
);
CREATE TABLE IF NOT EXISTS `lotto` (
	`system_id`	INTEGER NOT NULL UNIQUE,
	`date`	DATE NOT NULL,
	`numbers`	VARCHAR ( 20 ) NOT NULL,
	PRIMARY KEY(`system_id`)
);
COMMIT;
