# Thumbnail extractor

This script extracts thumbnails from video in given path.

## Requirements
Install project requirements with pip install -r requirements.txt

### Explanation

* As a non-empty frame I consider a frame that is not below a certain threshold of the 
average darkness of pixels in a given image frame
* Script takes last 10% of all frames.
* I am monitoring a fade out by checking a 15 point threshold in mean frame values