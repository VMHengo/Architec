<h1>Architec - Image Editing Software</h2>

## Description
This is a small personal project I created to explore my new interest in Computer Vision in combination with my hobby architectural sketching. 
I first created the project to automate the process of preparing a reference image for sketching by finding the vanishing point, greyscaling the image
and creating a grid for orientation.

## Features
Currently the project is in its baby stage. It is coded in QTCreator and only contains a few functions
- Load Image to Display and Saving it
- Drawing Grid with configurable resolution, thickness, color
- Apply Canny Edge to Image (Live Updates possible by Slider)

## Current tasks

### Vanishing Point Detection
- The first problem is in the feature extraction as the amount of clutter in images lead to many undesired edges 
when detecting them with Canny Edge detector for example.
- The second problem is the prediction of the vanishing point as RANSAC isnt accurate with the current features
### Color picker enhancements
- maybe implementation of a color wheel
- give preselected colors and remember previously used colors
