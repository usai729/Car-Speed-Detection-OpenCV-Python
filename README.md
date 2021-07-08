# Car-Speed-Detection-OpenCV-Python

Hi!

The `tracker.py` and the `HAAR Cascade` content *doesn't belong to me*
*tracker.py* has been taken from https://pysource.com/ and the cascade XML file from another GitHub repo.

For this project I've used `Python` and `OpenCV` library


The concept is simple.<br>


`speed=(distance/time taken)`


Make 2 points on the road. Let's say `pt1` and `pt2`, when a car crosses pt1, the timer starts and the time is stored in an variable `time_i` (initial time) and when the car crosses pt2, the timer stops and the time is calculated and stored in an variable `time_f` (final time).<br>
The difference of *time_i* and *time_f* will give time taken.<br>

To calculate the avarage speed the speeds detected are taken and stored in a `list` and formula `average = sum of all items/total number of items` has been used.<br>

Note that the first few cars speeds in my video are not accurate as the cars are already in between *pt1* and *pt2*. The cars that come after the few first cars have been detected of accurate speed.
