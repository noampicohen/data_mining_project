import mysql.connector
import sys


def create_database(password):
    mydb = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password=password)

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE  rotten ")
    mycursor.execute("USE rotten")

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `languages` (
      `id_language` INT NOT NULL AUTO_INCREMENT,
      `name_language` VARCHAR(255) NULL,
      PRIMARY KEY (`id_language`));
    
    
    CREATE TABLE IF NOT EXISTS `synopsis` (
      `id_synopsis` INT NOT NULL AUTO_INCREMENT,,
      `text_synopsis` VARCHAR(1000) NULL,
      PRIMARY KEY (`id_synopsis`));''', multi=True)

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `languages` (
      `id_language` INT NOT NULL AUTO_INCREMENT,
      `name_language` VARCHAR(255) NULL,
      PRIMARY KEY (`id_language`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `synopsis` (
      `id_synopsis` INT NOT NULL AUTO_INCREMENT,
      `text_synopsis` VARCHAR(1000) NULL,
      PRIMARY KEY (`id_synopsis`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies` (
      `id_movies` INT NOT NULL AUTO_INCREMENT,
      `name_movie` VARCHAR(255) NULL,
      `url_page` VARCHAR(255) NULL,
      `release_date_streaming` DATE NULL,
      `release_date_theater` DATE NULL,
      `rate_tomato` INT NULL,
      `rate_audience` INT NULL,
      `boxoffice` INT NULL,
      `languages_id_language` INT  NULL,
      `synopsis_id_synopsis` INT  NULL,
      PRIMARY KEY (`id_movies`),
      CONSTRAINT `fk_movies_languages`
        FOREIGN KEY (`languages_id_language`)
        REFERENCES `languages` (`id_language`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_synopsis1`
        FOREIGN KEY (`synopsis_id_synopsis`)
        REFERENCES `synopsis` (`id_synopsis`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE INDEX `fk_movies_languages_idx` ON `movies` (`languages_id_language` ASC) VISIBLE;''')

    mycursor.execute('''CREATE INDEX `fk_movies_synopsis1_idx` ON `movies` (`synopsis_id_synopsis` ASC) VISIBLE;''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `genre` (
      `id_genre` INT NOT NULL AUTO_INCREMENT,
      `name_genre` VARCHAR(255) NULL,
      PRIMARY KEY (`id_genre`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_genre` (
      `movies_id_movies` INT NOT NULL,
      `genre_id_genre` INT NOT NULL,
      INDEX `fk_movies_has_genre_genre1_idx` (`genre_id_genre` ASC) VISIBLE,
      INDEX `fk_movies_has_genre_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_genre_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_genre_genre1`
        FOREIGN KEY (`genre_id_genre`)
        REFERENCES `genre` (`id_genre`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `directors` (
      `id_director` INT NOT NULL AUTO_INCREMENT,
      `name_director` VARCHAR(255) NULL,
      PRIMARY KEY (`id_director`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `actors` (
      `id_actor` INT NOT NULL AUTO_INCREMENT,
      `name_actor` VARCHAR(255) NULL,
      PRIMARY KEY (`id_actor`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `producers` (
      `id_producer` INT NOT NULL AUTO_INCREMENT,
      `name_producer` VARCHAR(255) NULL,
      PRIMARY KEY (`id_producer`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `writers` (
      `id_writer` INT NOT NULL AUTO_INCREMENT,
      `name_writer` VARCHAR(255) NULL,
      PRIMARY KEY (`id_writer`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `distributors` (
      `id_distributor` INT NOT NULL AUTO_INCREMENT,
      `name_distributor` VARCHAR(255) NULL,
      PRIMARY KEY (`id_distributor`));''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_writers` (
      `movies_id_movies` INT NOT NULL,
      `writers_id_writer` INT NOT NULL,
      INDEX `fk_movies_has_writers_writers1_idx` (`writers_id_writer` ASC) VISIBLE,
      INDEX `fk_movies_has_writers_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_writers_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_writers_writers1`
        FOREIGN KEY (`writers_id_writer`)
        REFERENCES `writers` (`id_writer`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_actors` (
      `movies_id_movies` INT NOT NULL,
      `actors_id_actor` INT NOT NULL,
      INDEX `fk_movies_has_actors_actors1_idx` (`actors_id_actor` ASC) VISIBLE,
      INDEX `fk_movies_has_actors_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_actors_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_actors_actors1`
        FOREIGN KEY (`actors_id_actor`)
        REFERENCES `actors` (`id_actor`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_producers` (
      `movies_id_movies` INT NOT NULL,
      `producers_id_producer` INT NOT NULL,
      INDEX `fk_movies_has_producers_producers1_idx` (`producers_id_producer` ASC) VISIBLE,
      INDEX `fk_movies_has_producers_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_producers_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_producers_producers1`
        FOREIGN KEY (`producers_id_producer`)
        REFERENCES `producers` (`id_producer`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_directors` (
      `movies_id_movies` INT NOT NULL,
      `directors_id_director` INT NOT NULL,
      INDEX `fk_movies_has_directors_directors1_idx` (`directors_id_director` ASC) VISIBLE,
      INDEX `fk_movies_has_directors_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_directors_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_directors_directors1`
        FOREIGN KEY (`directors_id_director`)
        REFERENCES `directors` (`id_director`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS `movies_to_distributors` (
      `movies_id_movies` INT NOT NULL,
      `distributors_id_distributor` INT NOT NULL,
      INDEX `fk_movies_has_distributors_distributors1_idx` (`distributors_id_distributor` ASC) VISIBLE,
      INDEX `fk_movies_has_distributors_movies1_idx` (`movies_id_movies` ASC) VISIBLE,
      CONSTRAINT `fk_movies_has_distributors_movies1`
        FOREIGN KEY (`movies_id_movies`)
        REFERENCES `movies` (`id_movies`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_movies_has_distributors_distributors1`
        FOREIGN KEY (`distributors_id_distributor`)
        REFERENCES `distributors` (`id_distributor`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);''')


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print('usage: ERD.py [SQL PASSWORD]  ')
        sys.exit(1)
    password = args[0]
    create_database(password)


if __name__ == '__main__':
    main()
