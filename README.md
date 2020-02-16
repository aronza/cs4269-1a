# CS-4269 Project Part 1a

Team Number: 10

Members: Noah Popham, Arda Turkmen, Mark Weinstein, Harry Wilson 

## To set up the project:
  Make sure your system has python3 and git installed by running these commands:
    "git --version" and "python3 --version", they should return something similar to "Python 3.7.4" and "git version 2.21.1"
  If you don't have python3 you can find detailed instructions on installing python3 on your system here:
    https://realpython.com/installing-python/
  If you don't have git you can find instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
  
  Then you will need to clone our repository for which you should have the command line pointing to where you want to download the project
  and then run "git clone https://github.com/aronza/cs4269-1a.git"

## To run the project: 

To run the scheduler with the default catalog(the one given in the specifications) and ('CS', 'major') as the only goal, execute command "python3 course_scheduler_test.py"

To test the course_scheduler against our custom unit tests, execute command "python3 course_scheduler_test.py test"

To debug and see the indiviual steps the scheduler is taking, execute command "python3 course_scheduler_test.py debug". 
This option will print out messages to show the progress of the search function

## Changing goal conditions and initial state:

You can modify our course_scheduler_test.py main function to change the goal_conditions and initial_state of the course_scheduler.
You can add any valid course from the catalog to variables named goal and courses_taken to change goal_conditions and initial_state respectively.

On the other hand,  you can call the course_scheduler(course_descriptions, goal_conditions, initial_state) function in course_scheduler.py from your own code as well.
