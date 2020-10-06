# Thumbnail generator

This sample Django application is used to create thumbnails from video files.

## Requirements
* Docker
* docker-compose

## Running
In order to run application execute command `docker-compose -f docker-compose-local.yaml up`

### Application workflow
* Use form provided in landing page, upload sample video. 
Application will redirect to detail view of uploaded video. 

* Use form to generate thumbnail for video. 

* **threshold** is option used to detect fade-outs. Default is set to 15.  
* **limit** is a parameter used to find all frames with 
mean value of all pixels greater than said limit.
 

### Explanation

* As a non-empty frame I consider a frame that is not below a certain threshold of the 
average darkness of pixels in a given image frame
* Script takes last 10% of all frames.
* I am monitoring a fade out by checking a 15 point threshold in mean frame values