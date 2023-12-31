# Learning_Docker
A repository where I put my notes and tests while I learn to use Docker as an absolute beginner.

## Terminology
*Docker Deamon*: the process taking place in the host remote operating system. It is responsible for building, running and distributing the containers.  

*Docker Client*: the command line tool (or app with GUI) which allows th euser to interact with the Deamon.  

*Containers*: the isolated environments in which the application can run, containing all the necessary dependencies.  

*Images*: the blueprints of the application which form the basis of containers. The are divided into ***Base Images*** and ***Child Images***.  

*Dockerfile*: a text file whichis used to construct the images (this is the file which we actually write in, together with the code of the application).

## Files in the directory
- test.py : containes the actualy python code which is run in the container.
- Dockerfile: the file used to build the image.

## How to create and run the app 
- Run the command ***sudo docker build -t test .*** to build the image
- Run the command ***sudo docker run test*** to run the app
