# Open Door Data

This application was built for our group's UCD Summer Practicum course. In this research semester we attempted to create an application that was able to predict classroom occupancy based on the number of devices connected to a wireless access point associated with that particular classroom. The outcome of this project was a fully packaged application that contains displays for the occupancy data and historical data, an API and an Admin page. Here we will go over some of the different parts of the project.

We built this project using and MVC architecture pattern and a LAMP stack. Our full application architecture was based on the Flask-Peewee framework, designed using the Django methodology.

Our back-end is composed of many different files that are built to be modular and serve a specific purpose while also interaction with other the other files. 

Our front-end is composed of nine different pages:

1. The home page is a general splash page that explains the site and what it does.
2. The Api page contains our documentation for accessing and querying our sites API.
3. The Login page is a general login page that allows users to login to access specific parts of the application.
4. The Survey page allows authorized users to submit new data on how full a room is.
5. The Admin page allows authorized users to add/edit/delete certain database tables.
6. The Dashboard general page displays the occupancy of a room based on a week and occupancy level selected by a user.
7. The Dashboard building page displays information on the buildings contained in the Database
8. The Dashboard room page displays historical usage information on the rooms contained in the Database.
9. The Dashboard Module page displays information on historical room usage based on module selected by a user.




## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

To install Open Door Data either pip or easy_install the full Git address of this application. All modules required for this application will be installed as well. You will also need to have MySql running on your machine. 


## Deployment

To run a live version of this application on your own machine after installing, you will need to do the following:

1. Open the application directory
2. Run app.py to instantiate your app
3. Run models.py to create your mysql database
4. Run original_datacleaning.py to clean the original data
5. Run original_data_entry.py to enter the cleaned data into the database
6. Run main.py to launch the site on your local machine

After this if you would like to continue adding wifi log data you can send the zipped log files to the new_data folder and start new_data_cleaning.py and new_data_entry.py which will continue to check that folder every 5 minutes. 

## Versioning

All versioning of this project was done on UCD Git.

## Authors

* **Elayne Ruane** 
* **Pauline Lallinec** 
* **Jack Halpin** 
* **Don Blaine** 

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details

## Acknowledgments

* We'd like to thank everyone who created the packages that were used in this project.


