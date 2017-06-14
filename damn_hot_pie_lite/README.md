

The graph is prettier, but now requires the user to also install plotly. (use "sudo pip install plotly" on rasberry pi)

### damn_hot_pie_lite
Run the lite version using `sudo ./run.sh`
it has the same settings as above, but does not run the server.
The lite version only logs data to the database and generates an index.html page (which can then be loaded by apache, NGINX, or another webserver). I found it was simple just to copy all of the files to the `/var/www/html` folder. Make `run.sh` executable with `sudo chmod u+x run.sh`. You can setup a cron job or bash.rc to run the bash script at startup so you have minimal work to do, just boot and go to localhost!! 

![screenshot_plot](plot.PNG "New and Improved!")
