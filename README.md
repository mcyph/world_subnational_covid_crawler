# Introduction

This repo contains a collection of scrapers I wrote for both Australian and 
international COVID-19 data. As far as I know it's the most comprehensive 
automatic collection system of its kind in the world. 

It also includes a basic web interface for 
monitoring its status, and parsing for statistics which can be overlayed 
with COVID-19 data, such as economic and other data from the Australian 
Bureau of Statistics. 

It mainly differs from other similar projects because it not only provides national 
data, it also crawls data on sub-national and sub-state/province/territory 
levels where it is available. It also includes statistics on age group breakdowns 
and infection sources in many cases. The outputted data is updated periodically and 
can be obtained from https://github.com/mcyph/global_subnational_covid_data,
which is updated automatically. This project page also contains information 
about the websites which are crawled and the possible datatypes/schemas.  

It was intended to automatically obtain statistics related to COVID-19 for the 
[COVID-19 Case Tracker Australia](https://covid-19-au.com/) website which was 
started by Dr. Chunyang Chen and a group of volunteers at Monash and other 
Australian universities.

Currently there are hardcoded paths etc which need to be refactored to allow 
easier deployment (as I'm mostly using it on my own server), but if you'd like 
to use these scripts, by all means let me know by direct messaging me or opening 
a new GitHub issue! 

See also the [potential_sources.md](potential_sources.md) file for various 
resources related to GeoData and COVID-19.

## Source code layout

* `output_data.py` 
  > is the main output and conversion script. It crawls 
  > each enabled crawler in 
  > `covid_crawlers/_base_classes/OverseasDataSources.py`.
  >
  > Some sources which need selenium or are otherwise more 
  > bandwidth/CPU-intensive aren't crawled unless the 
  > `--run-infrequent-jobs` flag is specified.

* `_utility/`: 
  > various scripts which allow getting the path on disk of the 
  datafiles, extracting numbers from words such as "twenty-four", 
  normalizing place names, etc.

* `covid_crawlers/` 
  > contains the different crawlers, arranged by region.
  For instance, Australian crawlers are under `covid_crawlers/oceania/au_data`

* `covid_db/` 
  > contains an SQLite database system for efficient storage and 
   management of statistic revisions over time.

    * `covid_db/datatypes/` 
      > contains the datatypes which allow storing 
      individual covid-19 and other statistics categorized by age group,
      region (region schema/parent/child), datatype 
      (like total cases or deaths), source URL, source ID etc.

* `world_geodata/` 
  > provides processing and normalization of various different 
  GeoJSON data files that can be used with mapping software. 
  This is one of the biggest compilations of its type online. 
  I've needed to make a number of modifications to the data because of 
  updates to the ISO-3166-2 and other geographic schemas.

* `misc_data_scripts/` 
  > has a number of miscellaneous scripts and data:

    * `misc_data_scripts/hospitals/get_hospitals.py` 
      > Used to get COVID-19 hospital/clinic information 
        from the state websites, however is out-of-date and 
        needs to be refactored. 
  
* `web_monitor/` 
  > a web monitoring interface using `cherrypy` which 
  shows the status of previous runs and allows browsing statistics.
  Automatically schedules statistics gathering every hour or two 
  during Australian Eastern Standard Time.
