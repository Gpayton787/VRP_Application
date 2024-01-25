### Purpose
This application was built to schedule a given list of patient pick-ups and drop-offs. Manual scheduling takes not only a great deal of time and effort that could be used for something more productive, it's also not optimal more often than not. By taking in a few parameters the scheduler, which makes use of Google OR tools, models the problem and outputs the optimal schedule along with other useful information about said scheduling. 

### More information
This repository holds the source code for a route optimzation application. 
The application models a certain type of vehicle routing problem and uses Google OR tools to solve them.

It's a generalization of the classic VRP problem to a specific case
- There are patients that need to picked up and dropped off
- It also includes the common Capacitated, Pick-up and Delivery, Time window constraints.

Thanks to the Google OR team for creating and maintaining such a useful tool.
