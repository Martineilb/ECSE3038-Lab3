# ECSE3038-Lab3

The aim of this laboratory is to design a RESTful API such that a user may create a user profile. However, only one user profile can be created at any given time.
The user profile allows the user to set his/her username, role and favourite colour. Also, the user may update his/her profile after the data has been posted.
The server will generate the time and date at which the profile was created or updated.

The RESTful API should also allow for IoT monitoring of water tanks. The embedded circuit affixed to the water tanks should measure the water level within the tanks and 
report the values to the server. The water level will then be displayed on a webpage. The user should also be able to set the location and the coordinates (latitude and longitude)
of the water tanks. The user is also able to read, update and delete a water tank's data from the system. The information will then be stores with a mongo database which is secures by
Schema Validation.
