# Reinforcement Learning Robot
The goal of this project is to create a program which uses reinforcement learning to control a robot. The robot is tasked with reaching a randomized goal point in a static environment. The environment is cluttered with obstacles, and the robot is penalized for any collisions that it causes by moving through the environment.

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
// TODO describe methods
go into detail about how we represent state for RL, what we reward / punish, what pybrain classes we use (state that we don't really understand this), etc. @csun can talk about this

## Results
// TODO describe results
Say that robot learns how to avoid stuff using prox sensors pretty quickly, after couple hundred iterations gets pretty good about only going toward goal. Also that we need more sensors and when hits things it's because not in sensor

## Note
This project was built for Professor Robert Platt's Robotics Systems class at Northeastern University.
