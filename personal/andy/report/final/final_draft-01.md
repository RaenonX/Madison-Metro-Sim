# Final Report

# Metro Bus Simulator
Andy Lin <lin383@wisc.edu>
Jeremy Michael <jmsusanto@wisc.edu>
Ray Hsieh <yhsieh36@wisc.edu>
Chang Xu 
## Introduction

<center><img src="https://i.imgur.com/Jm0241p.png" width=550></center>

[The City of Madison, categorized into 145 wards]

Each number is the ward number of that area. A ward is basically a subdivision of an area, mainly used for electoral purposes. With this, we estimated the population distribution in the city of Madison. This estimation achieves a 98.03% of accuracy. 

<center><img src="https://i.imgur.com/nbeAsJB.png" width=550></center>

[Population distribution in Madison.]

In our simulation, we simulated random bus riders from each ward, according to the population in that ward.

### Inputs data from user:
- `times`: a list of times in the form `HH:MM:SS`
- `servs`: service types (e.g. `weekday`, `weekend`, `holiday`, `modified_week`)
- `num_points` or `perc_pop`:
  - Either one of `num_points` and `perc_pop` should be given, or both of them are not given.
  - 1. When both of them are not given: 253,030 riders will be generated.
  - 2. `num_points` specified:       generate riders `>= 144 * num_points`.
  - 3. `perc_pop`   specified:       generate points `>= 253,030 * (perc_pop / 100)`
- `threshold`: threshold distance (in meters, default to `400m`, or `1/4 miles`). It is used for calculating *the number of stops* and *available routes* within the threshold distance; riders will then decide to go to the bus stop with *the minimum waiting time* for the next bus to come.
- `bar_plot`: a user can decide if he/she wants a visualization of the simulated result.
- `geo_plot`: a user can decide if he/she wants a visualization of the generated riders connected to the nearest bus stop, shown by a map of Madison.

Using these data, we are able to compare **the level of service** among for each *ward*, determine **removal of one bus route/stop** that has the highest/lowest impact.

<center><img src="https://i.imgur.com/e6qIm3H.jpg" width=550></center>

Example of a simulation with **input** (as following): 
 - `times` = 7:30:00
 - `servs` = weekday
 - `perc_pop` = 1 (meaning 1% of population)
 - `threshold` = 400 (default)
 - `geo_plot` = True

**Result**:
Will show with plots after integrating area coverage method.



#### Comparing the level of service among wards. 
Identifying wards that have more accessibility to the Madison Metro Transit service (e.g. shorter waiting time overall, accessible to more routes and stops within the given threshold, able to reach more places/higher area coverage).

#### Identifying removal of a route that cause more/less impacts on each ward
a comparison of before/after of average of all points.

#### Identifying removal of a stop that cause more/less impacts on each ward
a comparison of before/after of average of all points.

[impacts could be: longer waiting time, fewer accessibility to routes, faster commuting time/higher area coverage]

### Simplifying Assumptions:
- riders can walk diagonal to bus stops.
- we do not take the time required by walking to the bus stop into account.

## Introduction to Madison Metro Simulation

<center><h4>How Are Riders Generated?</center>

<center><img src="https://i.imgur.com/fWAK2tH.png" width=1000></center>

<center>[Areas Categorized into 145 <em>Wards</em> and Population Distribution Based on <em>Wards</em>.]</center>


<br>

Each number is a ward number of that area. A *ward* is basically a subdivision of an area, mainly used for electoral purposes. With this, we estimated the population distribution in the city of Madison, then generate riders using the population distribution with respect to the density of that *ward*.

#### Simplifying Assumptions:
- Riders can walk diagonal to bus stops.
- Do not take the time required for walking to the bus stop into account.
- Data are based on the year 2020, thus some suspended routes not shown (due to COVID-19).










## Area Coverage for Different Times of Day

<img src="https://i.imgur.com/1AGA6O8.jpg" width="5000" align="center"/>
</p>
<center><strong>Figure 1: Area Coverage in 30 Minutes at Different Start Times <br/></strong></center>
<br/><br/>
<div align="left"><strong> Figure 1 </strong> shows the the trend of total possible area covered in 30 minutes depending on the starting time of day. The starting stop is within the UW Campus, which is approximately at the center of Madison. As can be seen in the figure, there is a noticable peak in the morning between 6:30 and 8:30 AM as well as at around 5:30 PM. Similar to the trend of route frequency over a typical weekday, this is likely due to the City of Madison increasing their level of bus service around these times to accomodate for people going to work and going back from work. There is also an unexpected drop at exactly 6:00 AM and 5:00 PM. This is possibly due to the fact they may have just missed a bus by a few minutes, therefore wasting some of the 30 minutes on simply waiting at the bus stop. Below shows some visual representation of what the simulator is doing. 

<br/><br/><br/><br/><br/>


<img src="https://i.imgur.com/rmpFtUZ.jpg" width="5000" align="center"/>
</p>
<center><strong>Figure 2: Area Coverage at 6:00 Starting at X  <br/></strong></center>
<br/><br/>
<div align="left"><strong> Figure 2 </strong> shows the simulated area coverage starting at X at 6:00 for 30 minutes. As can be seen in <strong>Figure 1</strong>, this is one of the dips in terms of area coverage. Considering that the starting stop is within the UW Campus, we would expect it to have a better area coverage. The relatively low area coverage becomes more apparent in the next figure. <br/><br/><br/><br/><br/>






<img src="https://i.imgur.com/lyjDmNY.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 3: Area Coverage at 17:30 Starting at X <br/></strong></center>
<br/><br/>
<div align="left"><strong> Figure 3 </strong> once again shows the simulated area coverage starting at X for 30 minutes, but the starting time is now 17:30. Visually, we can already see that the area coverage at 17:30 is significantly more than at 6:00. Starting at 17:30 rather than 6:00 allows for around 240% more area coverage. One thing to note is that on the figure, there exists some area covered that is isolated from the main brach of area. This is due to the fact that the bus is able to take people from stop to stop but is unable to drop them off before arriving at the next stop. The possibility of walking is also taken into account for by the simulator in the form of a circular area coverage around stops that they drop off at. 


## Evaluation of Starting Stops With Low Farthest Distance Travelled with Zero Transfers (According to Megan Tabutt)

In the prior analysis, Megan Tabutt concluded that stops in certain areas have a low possible farthest distance travelled assuming no transfers. While this metric may be able to indicate whether a stop is efficient or inefficient, we want to observe how these stops behave in regards to their area coverage. In other words, we compare the area coverage when starting at a centralized stop and starting at at a possible inefficient stop (As indicated by Megan). The next 3 figures show the area coverage at different starting points.

<img src="https://i.imgur.com/mgewtMe.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 4: Area Coverage at 12:00 Starting at Centralized X <br/></strong></center>
<br/><br/>



<img src="https://i.imgur.com/mloDo3n.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 5: Area Coverage at 12:00 Starting at Outskirt X (1) <br/></strong></center>
<br/><br/>




<img src="https://i.imgur.com/Qt04MrZ.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 6: Area Coverage at 12:00 Starting at Outskirt X (2) <br/></strong></center>
<br/><br/>

<strong> Figure 3 </strong> acts as a visual reference since it starts at a centralized stop, which we expect to have a relatively higher area coverage. As can be seen in both <strong> Figure 4 </strong> and <strong> Figure 5 </strong>, the area covered in 30 minutes is astonishingly low. In <strong> Figure 5 </strong>, the area coverage is low enough to where people may decide to just walk from one place to another within the area, other than perhaps some exceptions such as travelling from the starting stop to the outer border of the area depicted. However, in the case of <strong> Figure 5 </strong>, the area covered is so low that we would imagine people would not even consider using the bus. Once again note that this is the possible area coverage within 30 whole minutes. For people living near these stops, the bus system may not be an efficient way of travelling, especially not for long distance travelling. 


## Which Stops have the Best or Worst Area Coverage?



Here, we simulated over every possible starting stop starting at 12:00 noon with 30 minutes of elapsed time. For each simulation, we calculated the total area covered using the sim and the results can be seen below.

<img src="https://i.imgur.com/o85Jw4c.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 7: Best and Worst Starting Stops for Area Coverage <br/></strong></center>
<br/><br/>

<strong> Figure 7</strong> shows the best and worst starting stops for area coverage. The Green pointers show the 50 best starting stops for area coverage and the Red pointers for the worst. Other stops are also depicted in the figure as a small grey pointer. We can see that most of the best starting stops are located around the campus area of Madison. There are some exceptions to this, such as the stop near the Dane County Airport and the stop near East Towne Mall. However, notice that some of the worst stops are also located at the UW Campus. This is once again due to the nature of the bus timings. All the stops were simulated starting at 12:00 noon for 30 minutes, but some of these stops may be randomly better than others at this time. For example, one stop may have a bus coming at 12:01 while another may have just missed a bus at 11:58. This has a drastic impact on the area coverage as we are only simulating 30 minutes of time. On that note, this figure shows only roughly where the best and worst stops are located around.

To improve on this, we repeat this process for 5 other starting times each at a longer time period of 45 minutes. We assign a rank in the order of area coverage for each process and take the average to get a more accurate indication of which stops have the best and worst area coverage (UNFINISHED: TODO IN THE FUTURE)

## Which Bus Route is the Most Important to Students on Campus ?

The UW-Madison campus is located at the center of Madison and is key feature of the city. Students travel both off and on campus quite often. Here, to determine the most important route for students, we simulated 30 minutes starting at several stops in the campus area. We found that removing the 80 bus route had a drastic impact on the potential area coverage starting at a campus stop. The effect of removing the 80 bus route can be seen in the figures below:

<img src="https://i.imgur.com/RlTATwR.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 8: Before 80 Removal Starting At A Central Stop <br/></strong></center>
<br/><br/>




<img src="https://i.imgur.com/iZicQt4.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure 9: After 80 Removal Starting At A Central Stop <br/></strong></center>
<br/><br/>

As can be seen in the <strong>Figure 8</strong> and <strong>Figure 9</strong>, removing the 80 bus route had a massive impact on the potential area coverage starting at a campus stop. To further emphasize this, removing the 80 bus route has a similar effect to campus students as the combined effect removing every other bus route.



## NOV 30 START - Remember to remove this

## Which Areas are Under and Overprovided in Regards to the Bus Transit Service Level?

We want to determine bus stops and routes that need to changed,  especially in regards to location. Here, we divided Madison to its individual wards and analyzed the level of bus service in each ward. Every ward has unique features such as average income levels, population density, racial composition, and average age.

<img src="https://i.imgur.com/QqsUeCX.jpg" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure: Average Area Covered for Each Ward <br/></strong></center>
<br/><br/><br/><br/>

The above figure shows the level of bus service in each Ward. We used the average possible area coverage as an indicator of the level of service for each ward. To arrive at the value, we simulated over every stop in each ward to obtain the possible area coverage for each stop and taking the average across all stops in a ward. 
<br/><br/><br/><br/>



<img src="https://i.imgur.com/hsgQ3RT.png" width="10000" height = "" align="center"/>
</p>
<center><strong>Figure: Population Density against Average Area Coverage <br/></strong></center>
<br/><br/>

Here, we observe a positive correlation between Population Density And Possible Area Coverage. TODO HERE



![](https://i.imgur.com/LkVdlXP.jpeg)
