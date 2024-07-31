# Graphene_Finder
<a href="#"><img src="https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow" /></a>

Deep Learning-based Automatic Searching for Graphene

----

## Summary
An automated graphene scanning robotic system. The system uses a USB-controlled microscope platform to automatically scan samples and a custom-designed simple auto-focusing program. Additionally, a deep learning model is employed to recognize graphene, accelerating the preparation process. This robotic system will save researchers several hours, with the task of scanning graphene samples being entirely handled by the robot.

## Motivation
Graphene is currently one of the most popular two-dimensional materials. It is only one atom thick but has a hardness exceeding that of diamond. Its discovery could potentially lead to the invention of quantum computers. Currently, the Advanced Quantum Technology Research Center at Cheng Kung University primarily uses mechanical exfoliation to prepare graphene. However, this method requires researchers to spend several hours observing multiple samples under a microscope (Figure 1) and searching for the light purple target material in the samples (Figure 2). These steps are highly standardized, and if computerized, it would save researchers a significant amount of time.

![mono layer graphene](https://i.imgur.com/TnGdzdg.png)

## objectives
1. **Control the Microscope**: Scan the entire sample and take photos.
2. **Graphene Detection**: Use a deep learning model to recognize whether graphene is present in the photos.
3. **Save Detection Results**: Store the detection results in a specified folder, which includes the recognized images and the coordinates of the target on the microscope platform.
4. **Coordinate Navigation**: Allow the user to input coordinates to move the microscope to the specified position.

microscope automatic scanning and focusing [video](https://youtu.be/ObPmyX3FzXE)

## Architecture
The program is divided into three parts: Coordinate Creator, Microscope Controller, and TensorFlow Object Detection.
1. **Coordinate Creator**: The main program first calls the Coordinate Creator to plan the microscope scanning path. The microscope will scan the entire sample in an S-shaped pattern according to this path.
2. **Microscope Controller**: This part is responsible for moving and focusing the microscope, and it returns the captured images to the main program.
3. **TensorFlow Object Detection**: The main program sends the images to TensorFlow Object Detection for recognition. The recognition results are then stored in a designated folder.

![Architecture](https://i.imgur.com/w70vTOD.png)

## Demo
Below are the recognition results output by the deep learning model, which include target locations (bounding boxes), object classes (class labels), and confidence scores (confidences).
In the example image:
- Green Box: Indicates the position of the graphene.
- Object Class: The identified class is "graphene".
- Confidence Score: The confidence level is 94%.

![物件偵測結果](https://i.imgur.com/SXpvCkP.png)

## Design
1. coordinate creator

    The Coordinate Creator allows users to set the microscope's magnification, the substrate's edge length, and the microscope's starting position. With these three parameters, the program will return a one-dimensional array containing the coordinates of the positions to be scanned.
    ![coordinate creator](https://i.imgur.com/gcjoe6W.png)

2. microscope controller

    The microscope controller communicates with the microscope's moving platform via USB, successfully moving the microscope to the specified coordinates. However, an unexpected issue arose: the stage was tilted, causing the captured photos to be out of focus. To address this, I decided to design my own focusing module. First, I adjusted the focus at the same position and captured multiple photos. Using OpenCV, I assessed the clarity of each photo and adjusted the focus to the position with the highest clarity. This simple autofocus system was thus completed.
    ![microscope controller](https://i.imgur.com/ugvOTMX.png)

3. TensorFlow Object Detection

    Google provides a comprehensive Object Detection API, allowing for the flexible replacement of object detection algorithms. In this case, I used the Hourglass Network to extract target features and the CenterNet algorithm for object detection.

## Concept
The system controls the microscope to scan the entire sample and take photos. After scanning, TensorFlow is used to check for the presence of graphene. The detection results are stored in the "Detection result" folder, which contains the recognized images and a text file (txt) that records the coordinates of the images. Users can input these coordinates to move the microscope to the specified position.
To achieve this goal, the program consists of three main parts:
1. Microscope Movement: Controls the microscope to scan the sample according to the predefined path.
2. Focusing and Capturing Photos: Adjusts the focus and captures images, storing them for analysis.
3. Recognition: Uses TensorFlow Object Detection to identify graphene in the captured images and stores the results.

## File Descriptions
- coordinate_creator.py
    - Plans the microscope scanning path.
    - After entering the starting coordinates, the program will display the intended scanning path.
- getCCDphoto.py
    - Captures images from the microscope.
	- Includes a feature for clarity analysis.
- microscope_controller.py
    - Controls the microscope module and includes an autofocus function.
	- Uses clarity analysis to find the optimal focus position.
- graphene_detection.py
    - Identifies graphene and saves the results.
- main.py
    - The main program.
    - Users run this file to start the scanning process.

## Installation
- Pandas
- PyWin32
- OpenCV
- PySerial
- TensorFlow 2 Object Detection API

In vscode, it can be installed with pip:

    python -m pip install -r requirements.txt

## Note
Before running this file, you should replace the folder named my_model by your own model
