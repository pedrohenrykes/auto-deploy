# Automatic Website Deployment

Creation of a service on GNU/Linux servers, to deploy websites from versioned projects in VCS (Version Control Systems).

## Prerequisites

* GNU/Linux operation system (Tested on RHEL distributions)
* Python version 2.7.13 or higher

## Installing

To install the script on your Linux server, follow the steps below.

* Step 1: Copy the file "deployment.service" to the path "/usr/lib/systemd/system/".
* Step 2: Create a directory named "deploy" in the path "/usr/local/lib/".
* Step 3: Copy the "execute.sh" and "deploy.py" files to the "deploy" directory you just created.
* Step 4: Within "deploy.sh", enter the root path of your webserver. In my case, the root is "/var/www/html" because I put all the directories with my websites.
* Step 5: Inside the root directory of your webserver, make a clone of each versioned project you want to run, creating a "working copy" (as we can see, the script is ready for use with Subversion, but I think with some modifications it will work in your favorite VCS, because the principles are the same).
* Step 6: Set the permissions for the scripts with the command "chmod -R +x /usr/local/lib/deploy/".
* Step 7: Reload the server services, enable "deployment.service" to start along with the operating system, and start the service by executing the commands below:

```
systemctl daemon-reload
systemctl enable deployment.service
systemctl start deployment.service
```
After that, your automatic deploy should be working. Enjoy!

## Authors

* **Pedro H. Aguiar** - [pedrohenrykes](https://github.com/pedrohenrykes)

## License

This project is licensed under the GNU GPL License - see the [GNU GENERAL PUBLIC LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) for datails.
