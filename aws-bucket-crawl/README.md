The purpose of this script is to download an object from a public S3 bucket (using boto3), fetch an URI inside that object, then use it to retrieve another file and stream it`s contents to stdout. 
The process should occur in memory, and no temporary file will be created. 

#### Setup
1. Change directories at the command line to be inside the `aws-bucket-crawl` folder;
   
2. Run `docker build --tag=bucket-crawl .` to build the `Docker` image;

3. Run the command `docker-compose up run` to execute the script.

PS. AWS credentials should be set up before running the script. Boto3 will scan the directory looking for the credentials file.

#### Expected behavior
1. USe `boto3` to download the file in memory from s3 located at bucket `commoncrawl` and key `crawl-data/CC-MAIN-2022-05/wet.paths.gz`
2. Extract and open this file with Python (hint, it's just text).
3. Pull the `uri` from the first line of this file.
4. Again, download the that `uri` file from `s3` using `boto3` again.
5. Print each line, iterate to stdout/command line/terminal.


Original exercise repository: 

https://github.com/danielbeach/data-engineering-practice/tree/main/Exercises/Exercise-3