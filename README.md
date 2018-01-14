Run through your PST files
--------------------------

Still a technical  prototype, 


_ get started _

* run linux and have git, have make installed
* have linux-docker installed
* be able to run 'docker ps' if not:
  * note: the make user must have docker privileges. 
  * (as sudo-user)$ sudo adduser <user> docker
  * (as user)     $ newgrp docker
   
* make run
  * (if all goes well it prompts the docker machine shell)
  * ./go.sh
  * it reports that the test pst has been processed (4 messages read)
