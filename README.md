# Reinforcement Learning Robot
The goal of this project is to create a program which uses reinforcement learning to control a robot. The robot is tasked with reaching a randomized goal point in a static environment. The environment is cluttered with obstacles, and the robot is penalized for any collisions that it causes by moving through the environment.

This project was built for Professor Robert Platt's Robotics Systems class at Northeastern University.

## Setup and Operation
1) Install [pybrain](http://pybrain.org/docs/)
2) Install [v-rep](http://www.coppeliarobotics.com/downloads.html)
3) Depending on your os, you may need to follow [these instructions](http://www.coppeliarobotics.com/helpFiles/en/remoteApiClientSide.htm) to get python talking to vrep.

Once all of this is installed, [start v-rep](http://www.coppeliarobotics.com/helpFiles/en/commandLine.htm). Then, run `python rl_robot/train.py <SOME_DIRECTORY>`. This will start training of a model, which should be visible in your v-rep instance. This will also auto-save the trained models every couple iterations. _However, it appears that reloading saved models does not currently do anything._ This needs to be fixed.

## The Simulation
V-rep is used to simulate both the robot and its environment in this simulation. V-rep has capabilities to simulate dynamics, but we've opted to turn this off to reduce inconsistencies caused by latency.

We set up a generic 7DoF robotic arm and placed it in a scene with a table, chair, and two items on top of the table. Goal positions are randomly generated at the start of each simulation in specific areas that require the robot to avoid these obstacles (eg. under the table, behind the objects on the table, etc.).

To give the robot information about its surroundings, we've attached 11 proximity sensors to it at varying points on its body. These are displayed in v-rep as red "laser beams" which flash yellow when they are detecting a nearby object.

## Methods
We used pybrain's reinforcement learning capabilities to teach the robot to perform the task. The specific algorithm that we ended up using is called "Policy Gradients with Parameter Exploration", though to be honest, we're not really sure what this means. There's not much documentation for the rl aspects of pybrain, and neither of us are experts on the subject. From what we understand, though, it's some sort of black-box optimization algorithm that takes in the current state of the environment, and learns proper actions based on received rewards.

Environment state (as seen by the leraning algorithms) is represented as a vector of floats. We fill this vector with the current joint positions, the distance vector from end effector to goal position, and all proximity sensor readings.

We give the robot rewards based on three factors. At each timestep, there's a reward that's directly proportional to how much closer / farther the robot got to the goal. If the robot collides with an object, there is a strong negative reward that is scaled based on how far the robot was from the goal when it collided. Finally, there's a reward for touching the goal that is scaled based on how little time it took.

## Results
The results of the experiment were mixed. On one hand, the robot learns to avoid obstacles detected by its proximity sensors remarkably quickly. This can be seen in the video `examples/avoidance.mp4`. On the other hand, the robot never really learns to reach its goal, though it does get into a habit of following a similar, very reasonable path that takes it near the area where the environment will generate goal positions. See the differences between `examples/early.mp4` and `examples/late.mp4`, where early was taken on the second iteration of an experiment and late was taken on the 849th iteration of an experiment.

In our opinion, one of the biggest problems with our method is that the robot has very poor sensor coverage of the environment. Because the proximity sensors are so thin and have such short range, the robot often does not detect the obstacles that it runs into. It struggled specifically with the laptop on the table in the environment, which was almost never detected by the sensors. One potential remedy for this would be to use low-resolution depth cameras to increase the FOV of the sensors, and subsequently coverage of the environment.

Additionally, we don't understand the properties of our chosen rl algorithm enough to know if it was a good fit for this application. Due to the lack of pybrain documentation, we struggled so much just getting any sort of learning working that we didn't have time to figure out what the "proper" methodes were. As such, we believe that further research into this topic could greatly improve our results.

## Conclusion
All in all, this was a fun learning experience. We got to work with controlling a robot in a simulated environment, and explored feature representation for robotic learning tasks. Even though the robot never reached the goal state, it was great to get to see the robot clearly "learning" to use information from things like its sensors. We're pretty proud of the outcome here.
