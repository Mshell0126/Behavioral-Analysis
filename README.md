# Behavioral-Analysis
Snapshot of the software used to generate graphs of data collected in JSU's behavioral analysis department.
The package consists of several files. FIGURES is a folder containing expected output from Matplotlib

Main.py pulls things together to run from a centeral application.

helper.py has some useful funcitons including an iterative function caller so you can write a 
loop once and forget it.

csv_gen.py is a helper that prints arrays to csv incase you need to use the built in plotting tools
in Excel instead of using matplotlib

database.py handles the creation, saving, and loading of a database. when you first start an experiment, 
data will be housed in a plethora of binary files. database.py seeks to organize these into a large
dictionary. A future implementation may break it into 4 files rather than one large file, but for now, 
it saves a database as a .pickle or .json file. The current version of the software uses the .pickle format.

fileHandler.py is an adaptation of an older python script written by former JSU Alumnus Ted Chandler.
fileHandler.py is different from it's namesake in how it organizes it's data, but it still utilizes Ted's 
functions for reading bytes into integer, string, and date values to make the header and data for each fiile.
database.py callse on fileHandler.py to fetch the data from binary. For each file retrieved this way,
database then stores the data in an organized way.

dbEditor.py is a file used strictly for manual adaptations to the database. For example, at one point
some tables in the database had erroneous header information. dbEditor.py is where quuick fix scripts
are run to go through and make changes. Having it in it's own file is important so that it isn't run 
on accident. Further security is ensured by commenting out one time only scripts. They are preserved
for historical logging so we know what sort of changes have been made.

There are two main categories of Sessions run in the experiment: Static and Dynamic.
Because of their differences, two separate algorithms were needed. For readability, the files were
sepaarated into their own individual files. 

static_stability.py and dynamic_stability.py both collect data over a session, calculate an average
frequency for a certain event, and then plot the average frequency over the course of all sessions
for a particular category.

static_dot_plots.py and dynamic_dot_plots.py both look at the types of events in a session and show a 
scatter plot of the main event over time, delimited by a secondary event.

In both cases, dynamic has several different sections that can be examined within a single session. 
For the dynamic scripts, an extra argument is taken to determine which sections should be analyzed.

In both cases of dot plots, sessions are combined over an entire category.
