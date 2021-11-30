# data_mining_project-
The first project at Israel Tech Challenge, scrapping of the website rottentomatoes. By Noam Cohen and Nissiel.

We scrapped the rottentomatoes site, we went through a classic path taking as much data as possible. The data of the page of the recent releases or rankings, then the pages of the films it contains. 


Runnning of the code :
When running the code for the first name, creating the associated database is needed, either by using the ERD script attached or directly by using the ERD.py file attached, launching it from the terminal specifying your password in first argument. (format: ERD.py [SQL PASSWORD])
Then the code is run by calling its name from the terminal following by three arguments : the type of movie we want to scrap, then the number of movies we want to scrap and then the password of its mysql root access. (format: rotten_tomatoes_scrapper.py [category] [number of movies] [SQL PASSWORD])Then the program asks the user the path of chromedriver in his computer that the user should have install in his computer, in the version corresponding to its version of Chrome. 
The list of movies types are ('ALL','ACTION','ANIMATION','ART_FOREIGN','CLASSIC','COMEDY','DOCUMENTARY','DRAMA','HORROR','FAMILY','MISTERY','ROMANCE','SCIFI'). The use of upper or lower case for the type of film is indifferent.
If the number of movies that user want to scrap is bigger than the number of movies on the website, only the movies available will be scrapped.
The constants are stored in the conf.py file. 
The scraped data will be aded to the corresponding database named rotten. 


Database documentation: 
The tables contained in the database are :
- movies containing the name, url, release date in straming and theaters, rates of tomato website and audience, and box office.
- genre containing the genre of movies.
- languages containing the genre of movies.
- synopsis containing the synopsis of movies.
- writers containing the name of the writers.
- actors containing the name of the actors.
- producers containing the name of the producers.
- directors containing the name of the directors.
- distributors containing the name of the distributors.
_ The many-to-many tables that is relating the table movies with others movies_to_genre , movies_to_writers , movies_to_actors , movies_to_producers , movies_to_directors , movies_to_distributors ,

[ERD_rotten_tomatoes.pdf](https://github.com/noampicohen/data_mining_project/files/7628305/ERD_rotten_tomatoes.pdf)


History of the difficulties and the solutions chosen to get around them :

After a long reflexion on the website to scrap we finally chose rotten tomato because of a common interest for the cinema, the variety, quantity and constant updating of the site's data. (https://www.rottentomatoes.com)

- What to scrap :
  Beginning on the top movies page we decided to scrap informations about the new movies like title and release date and then go on the dedicated page of the movie   to scrap more information.

- Two steps of scrapping
  First : “classement page”
  Name
  Url of dedicated page
  Second :”movies pages”
  Rate by audience
  Type of movie
  Length of movie
  Critic by Rotten Tomato 
  Movie info : Synopsys + more details 
  Cast/crew including list of actors

- We figured that there was a problem because we didn't have the same information on the chrome inspector and on the source page. And we couldn’t find on the          sources page the information needed. We understood after many tries and searches that it was because the website changes its page content dynamically and we need   our scraper to execute javascript. We found a way to do it with selenium.
  With this solution we could scraped the informations of the first page “classement” but the page display only a part of the classement so we need to click on the   “show more” button few times to have the full list
  
 - We had some issues to find a way to click on the show more button because the functions we found were not usable by the current version of python like               find_elements_by_xpath. But at the end we could do it with the more general function "find_elements" and "BY from" selenium.webdriver.
  We then wanted to click few time on the button and found a way to do it by using sleep function to le the time the page need to be loaded.
  We could then click on the showmore button until it's not possible.
  
 - When we tried our first complet tests on a bigger number we figured that some problems could appear when we try to scrap a specific information that each movie   should have but some doesn't have in reality. To solve this problem we set up exceptions with passe inside the loop.
  
 - We tried to find a way to automaticly find the path to chrome driver to don't have to ask the user to enter it, but didn't find a general way working with all     devices
 
 - Command interface : in order to give to the user more possibilities in the scrapping we decided to add two functionalities : first the type of movie to scrap and second the number of movies to scrap 
 
 - Construction of the database : We designed the database on mysql workbench and then run the code on big sizes of movies in order to fix the particular problems than can occured with a non usal type of data for a specific movies. 




