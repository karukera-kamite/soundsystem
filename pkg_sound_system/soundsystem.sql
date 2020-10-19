-- SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
-- SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
-- SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema soundsystem
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `soundsystem` ;

-- -----------------------------------------------------
-- Schema soundsystem
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `soundsystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE `soundsystem` ;

-- -----------------------------------------------------
-- Table `soundsystem`.`users`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `soundsystem`.`users` ;

CREATE TABLE IF NOT EXISTS `soundsystem`.`users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `login` VARCHAR(255) NULL,
    `password` VARCHAR(255) NULL,
    `firstname` VARCHAR(255) NOT NULL,
    `lastname` VARCHAR(255) NOT NULL,
    `birth` DATE NOT NULL,
    `sex` TINYINT(4) NOT NULL,
    PRIMARY KEY (`user_id`)
)
ENGINE = MyISAM;
-- DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soundsystem`.`albums`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `soundsystem`.`albums` ;

CREATE TABLE IF NOT EXISTS `soundsystem`.`albums` (
    `album_id` INT NOT NULL AUTO_INCREMENT,
    `image_album` VARCHAR(255) NULL,
    `artist` VARCHAR(45) NULL,
    `title_album` VARCHAR(255) NULL,
    `genre` VARCHAR(44) NULL,
    `album_tracks` JSON NULL,
    PRIMARY KEY (`album_id`)
)
ENGINE = MyISAM;
-- DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soundsystem`.`selected_albums`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `soundsystem`.`selected_albums` ;

CREATE TABLE IF NOT EXISTS `soundsystem`.`selected_albums` (
    `selected_album_id` INT NOT NULL AUTO_INCREMENT,
    `first_time_selected` DATE NULL,
    `last_time_selected` DATE NULL,
    `how_many_times` INT(8) NOT NULL,
    `users_user_id` INT NOT NULL,
    `albums_album_id` INT NOT NULL,
    PRIMARY KEY (`selected_album_id`),
    CONSTRAINT `fk_selected_albums_users_idx`
        FOREIGN KEY (`users_user_id`) REFERENCES users (`user_id`),
    CONSTRAINT `fk_selected_albums_albums1_idx`
        FOREIGN KEY (`albums_album_id`) REFERENCES albums (`album_id`)
)
ENGINE = MyISAM;
-- DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soundsystem`.`track_listened`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `soundsystem`.`track_listened` ;

CREATE TABLE IF NOT EXISTS `soundsystem`.`track_listened` (
    `track_listened_id` INT NOT NULL AUTO_INCREMENT,
    `track_name` VARCHAR(45) NULL,
    `track_data` VARCHAR(60) NULL,
    `track_listened_to_end` VARCHAR(45) NULL,
    `track_listened_x_times` INT NULL,
    `selected_albums_selected_album_id` INT NOT NULL,
    PRIMARY KEY (`track_listened_id`),
    CONSTRAINT `fk_track_listened_selected_albums1_idx`
        FOREIGN KEY (`selected_albums_selected_album_id`) REFERENCES selected_albums (`selected_album_id`)
)
ENGINE = MyISAM;
-- DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soundsystem`.`playlist`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `soundsystem`.`playlist` ;

CREATE TABLE IF NOT EXISTS `soundsystem`.`playlist` (
    `playlist_id` INT NOT NULL AUTO_INCREMENT,
    `playlist_name` VARCHAR(45) NULL,
    `users_user_id` INT NOT NULL,
    `track_listened_track_listened_id` INT NOT NULL,
    PRIMARY KEY (`playlist_id`),
    CONSTRAINT `fk_playlist_users1_idx` 
        FOREIGN KEY (`users_user_id`) REFERENCES users (`user_id`),
    CONSTRAINT `fk_track_listened_playlist_idx` 
        FOREIGN KEY (`track_listened_id`) REFERENCES track_listened (`track_listened_id`)
)
ENGINE = MyISAM;
-- DEFAULT CHARACTER SET = utf8mb4;

-- SET SQL_MODE=@OLD_SQL_MODE;
-- SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
-- SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
