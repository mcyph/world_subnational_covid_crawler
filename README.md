This repo contains a collection of scrapers for COVID-19 data.
Things are changing fast as of writing this, so they may or 
may not be functional.

* hospitals/get_hospitals.py gets COVID-19 hospital/clinic information 
  from the state websites. As of this The WA data needs to be updated 
  to a different URL.
  
* vic_power_bi_grabber/grab.py gets Victorian regional statistics etc
  from https://app.powerbi.com/view?r=eyJrIjoiODBmMmE3NWQtZWNlNC00OWRkLTk1NjYtMjM2YTY1MjI2NzdjIiwidCI6ImMwZTA2MDFmLTBmYWMtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9
  
* get_total_cases_tests.py gets the total number of cases tested to 
  date from state press releases. Has stopped working a few times
  due to changes in the government websites.
  
* state_news_releases/ is not finished - it will get for each 
  state from press releases and other pages, and is derived from the 
  get_total_cases_tests.py script.

