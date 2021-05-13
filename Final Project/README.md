# Final Project

Using the tools and techniques you learned in this class, design, prototype and test an interactive device.

Functional check-off - May 10
 
Final Project Presentations (video watch party) - May 12

## Description + Usecase (Anam)
## Design Architecture
 ### Hardware (components used)
 ### Software (server side (Antonio), pi (smart mirror module, camera, sensors etc)
 
 #### Server
Our localhost webpage consists of your typical HTML, JS and Python files. The [javascript file](/Final%20Project/static/index.js) waits for events on the webpage and sends a message to a [python](/Final%20Project/app.py) file that serves as a bridge between the server and the pi. Simply put, there are 4 events:
1. Connect: once the webpage is up and running, the pi gets a message that the server is up and running. This triggers the pi to run a [Python script](/Final%20Project/graph.py) that will generate two graphs the describe the mirror's performance in the last 7 days. These are saved in a directory that is specified in the [HTML](/Final%20Project/templates/index.html).
2. Start: Once the webpage is up and running there is a 'Start' button at the top of the page that when clicked, sends a message to the pi to [start the "smart" part of the mirror](/Final%20Project/merged.py) (i.e. turn the camera and display on and start measuring impressions and engagements).
3. Impressions: Once the smart mirror is running, the user can click on a button that will fetch the latest performance updates related to impressions. Clicking the 'Refresh Impressions' will show the user a message that looks like: "Average impression time is X.XXs after X impression(s)."
4. Engagements: Similar to the Impressions event, the "Refresh Engagements" button will fetch the latest performance updates related to engagements. Clicking the button will only show the number of engagements.

 
 #### Pi
 - Loading of items (talk about condition)
 - Tkinter for displaying the images (talk about top, bottom, left, right frames?)
 - Original code was from SmartMirror module (find youtube link and reference OG file)
 - Teachable Machine model
 - Logic diagram for performance measurement
 
 ## labeled image, sketches
4. Detailed video
5. Demo video
6. Reflection
7. Contributions
- Anam: camera module and model, created dummy data
- Antonio: server, image display, reading dummy data logic, touch sensor logic
- Both: mirror performance logic, PhUI

## Objective

The goal of this final project is for you to have a fully functioning and well-designed interactive device of your own design.
 
## Description
Your project is to design and build an interactive device to suit a specific application of your choosing. 

## Deliverables

1. Documentation of design process
2. 
3. Archive of all code, design patterns, etc. used in the final design. (As with labs, the standard should be that the documentation would allow you to recreate your project if you woke up with amnesia.)
4. Video of someone using your project (or as safe a version of that as can be managed given social distancing)
5. Reflections on process (What have you learned or wish you knew at the start?)


## Teams

You can and are not required to work in teams. Be clear in documentation who contributed what. The total project contributions should reflect the number of people on the project.

## Examples

[Here is a list of good final projects from previous classes.](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/wiki/Previous-Final-Projects)
This version of the class is very different, but it may be useful to see these.
