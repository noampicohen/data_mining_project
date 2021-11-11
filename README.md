# data_mining_project-
Our first project at Israel Tech Challenge, scrapping of the website rottentomatoes.

We scrapped the rottentomatoes site, we went through a classic path taking as much data as possible. The data of the page of the recent releases or rankings, then the pages of the films it contains. 

The code is run by simply calling its name or directly with the run feature. Then the program ask the user the path of chromedriver in his computer that the user should have install in his computer, in the version corresponding to its version of Chrome.
The constants are stored in the conf.py file. 

History of the difficulties and the solutions chosen to get around them. 

We finally chose rotten tomato.
https://www.rottentomatoes.com

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

