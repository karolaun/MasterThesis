**Tracking multiple dots over two layers**

The code is influenced by previous code in the repository, with this being a combination of the code for tracking two dots, and the grid tracking. 

Results from the first implementation of this code was this:

![frame75](https://github.com/karolaun/MasterThesis/assets/166374797/3b9b6f23-9304-453f-b086-00aa3896f2b3 | width=100)

This is of the better results, but is quite consistent in the video. However, some of the first frames missed values or added centers where there were none. Like this one:

![frame9](https://github.com/karolaun/MasterThesis/assets/166374797/0bf7d04d-de4e-423c-bbde-87383f217386 | width=100)

The plots of this first video shows this more clearly:
![Green](https://github.com/karolaun/MasterThesis/assets/166374797/67f15a10-7ac2-451e-b523-ab7634fdbc5a | width=100)
![Red](https://github.com/karolaun/MasterThesis/assets/166374797/56d134ae-f192-43ed-b841-eeb8d6a04de2 | width=100)

In the video, the layer with red dots were moving while the green was static. The original video can be seen below:
[TrackingVideo](https://www.youtube.com/watch?v=eEMUSFy1HLg)
