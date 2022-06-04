The purpose of this script is to download zip files asynchronously from a list of URLs. It will extract the contents and then delete then original zip files

#### Setup
1. Change directories at the command line to be inside the `GetFiles` folder;
   
2. Run `docker build --tag=get-files .` to build the `Docker` image;

3. Change the 'urls_list' located in main.py if necessary;

4. Run the command `docker-compose up run` to execute the script.


### Expected behavior
1. Create the directory `downloads` if it doesn't exist
2. Download files from the list asynchronously, then unzip, then delete the original zip files.
3. All steps logged in the files.log file

