## S3 select

### Motivation
[Amazon S3 select](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html) is one of the coolest features AWS released in 2018. It allows you to return only subset of file contents from S3 using limited SQL select query. Since filtering of the data takes place on AWS machine where S3 file resides, network data transfer can be significantly limited depending on query issued. This also dramatically improves query speeds. It's also very [cheap](https://aws.amazon.com/s3/pricing/#Request_pricing_.28varies_by_region.29) at $0.002 per GB scanned and $0.0007 per GB returned<br>
Great intro to S3 select is available [here](https://www.youtube.com/watch?v=uxcyoc6uaLM).<br>
Unfortunately S3 select API query call is limited to only one file on S3 and syntax is quite cumbersome, making it very impractical for daily usage. These are and more flaws are intended to be fixed with this s3select command.    

### Features at a glance
Most important features:
 1) Queries all files beneath given S3 prefix
 2) Whole process is multi threaded and fast. Scan of 1.1TB of data in stored in 20,000 files takes 5 minutes). Threads don't slow down client much as heavy lifting is done on AWS.
 3) Format of the file is automatically inferred for you picking GZIP or plain text depending on file extension 
 4) Real time progress
 5) Exact cost of the query returned for each run
 6) Ability to only count records matching the filter in fast and efficient manner
 7) You can easily limit number of results returned while still keeping multi threaded execution
 8) Failed requests are properly handled and repeated if they are retriable (e.g. throttled calls) 

### Installation
The easiest way to install s3select is to use [pip](http://www.pip-installer.org/en/latest/):
<pre>
$ pip install s3select
</pre>

### Authentication

S3 select uses boto3, so authentication and endpoint configuration is the same. For more details see [aws-cli](https://github.com/aws/aws-cli#getting-started) documentation.
 
### Example usage


### License

Distributed under the MIT license. See `LICENSE` for more information.
