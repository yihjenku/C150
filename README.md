C150
====

Columbia Lightweight Rowing Database

The goal of this web application is to allow the Columbia Lightweight Rowing team and coaching staff to view the statistics, results, and graphs of individual team members. Importing raw data from csv files, the translator scripts written in Python upload all of the team data into MongoDB. These Python scripts also run analytics on this data in order to compare individual rowers to the team and to Olympic lightweight rowers. Using Flask, HTML, and CSS, c150.yihjen.com was created for Columbia lightweights and friends to view the progress we are making as a team toward winning a national championship. 


Project To Do List
------------------
- [x] make methods that make split change graphs for 20 and 40 minute tests
	- [x] average team splits
	- [x] insert graphs into template
	- Finished 1/12/15
- [x] split differences
	- [x] sort by date
	- [x] make split differences into strings
	- [x] some intervals incorrect
	- Finished 1/13/15
- [x] test pages
	- Finished 1/15/15
- [x] search case sensitivity
	- Finished 1/14/15
- [x] individual rower info for each page
	- Finished 1/19/15
- [ ] photos of rowers 
- [ ] Add links to invidiual rower pages from team pages
- [ ] Fix bug with McGrattan double-capitalization
- [ ] Add new templates for new workouts
