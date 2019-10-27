# HALLOWEEN CANDY DISPENSER
This is the Python code for a Halloween dispensing robot head, optionally
covered by a scary mask.

### EXPERIENCE
When someone at a distance is detected, the head will whisper a phrase
like one of the following:

- “Come closer”
- “Hey you. Yeah. Over here”
- “I have something for you”

When someone gets very close the head will make a regurgitating 
sound + dispense a candy pack for each person detected at this range, once 
the candy is dispensed it will say something like one of the following:

- “Those are fresh, I ate them with the last trick-or-treater”
- “You should dry that off before you eat”
- “Hope you enjoy those more than I did”

### REQUIREMENTS
Valid alwaysAI credentials to use the alwaysAI computer vision platform.
This allows for rapid development and deployment of the app onto an edge 
device (like a raspberry pi) without requiring it to have internet access.

To sign up, goto [this page](https://learn.alwaysai.co/beta)

### VOLUME CONTROL
```
amixer scontrols
amixer sset 'Master' 100%
```

### DEPENDENCIES
alwaysAI
`npm install -g alwaysai`
Simple Audio
`pip3 install simpleaudio`
`sudo apt-get install libasound2-dev`

#### ALWAYSAI REQUIREMENTS
When adding dependencies, additional info most be provided for the resultant docker image to build correctly. See [this page](https://dashboard.alwaysai.co/docs/application_development/handling_app_dependencies.html) for more info. Note that you'll need valid beta credentials to log into the alwaysai docs.

To get versions of the pip dependencies to add the `requirements.txt` file
`pip3 list --format columns`


### TROUBLESHOOTING
ERROR:
```
WARNING: The directory '/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
```
SOLUTION:
Make sure you're using the `==` symbol in your `requirements.txt` file. ie `simpleaudio==1.0.2 ` and not `simpleaudio=1.0.2 `