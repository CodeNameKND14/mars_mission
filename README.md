# mars_mission
# Mission to Mars

In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.

# Step 1 - Scraping
Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.


### NASA Mars News

- Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

### JPL Mars Space Images - Featured Image


- Visit the url for JPL Featured Space Image here.


### Mars Weather

- Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.


### Mars Facts


- Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.


- Use Pandas to convert the data to a HTML table string.



### Mars Hemispheres


- Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.




### Step 2 - MongoDB and Flask Application
- Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.


