# Belgium's Energy Consumption Visualization (Group B)

## Team Members

- Chad: "An intelligent and witty person that works on the betterment of oneself and those around him." -Jacob
- Harpreet: Passionate mathematician on the path of becoming a statistician.
- Nelson: Definitely a data engineer on my right track in the near future.
- Nyanda: one sentence about you!

## Describe your topic/interest in about 150-200 words

It is really important for the electricity grid operators to determine the amount of electricity fed into the electricity grid otherwise it might lead to a power blackout. The served purpose for this visualization would be to help the energy management system of Belgium to determine the adequate size of photovoltaic and energy storage to diminish the power flow into the grid during the various seasons of the year. Moreover, since the data is collected from a low-energy house it would help the management to address the challenge and decide upon a minimum threshold per household for load control if required in any unforeseen emergency situation. For instance, in case the management is willing to perform certain changes in the services or is willing to keep the power grid under maintenance then they would require a backup system that has the capacity to handle the least amount of energy load per household which is dependent on that power grid which is under maintenance. Our main focus would be to help the team to find out only the necessary amount of energy required by a Belgium resident. Our app will allow the user/the operator's supervising team to flexibly filter their search and view different aspects of the data by filtering and re-ordering on different variables.

## About this Dashboard

The dashboard offers an interactive floorplan where the user can select which room they would like to display data for. The plot next to the floorplan updates with temperature and humidity plots for the selected room. Expanded plots are displayed below showing outdoor temperature and humidity data alongside energy usage for the house. Using a selection of sliders, users can set the time range for the data.

<img src ="docs/milestone_sketch.png" width="500px">


## Describe your dataset in about 150-200 words

The data set was donated in the year 2017 by Luis Candanedo, University of Mons (UMONS). It was collected to create regression models of appliances energy use in a low energy building in Belgium. Our dataset includes approximately, 20000 temperature and humidity sensors measurements from a ZigBee wireless network, outside weather conditions (`To` and `RH_out`, `Wind speed`, `Visibility`, `Tdewpoint`) from a nearby airport station (Chievres Airport, Belgium), and recordings of the energy consumed by the lighting fixtures and other appliances operated by the people residing in that house. The recordings have been recorded at 10 min for about 4.5 months (i.e. from January 11, 2016 to May 27, 2016) in a low-energy building. The node transmitted the temperature recording (`T1` to `T9`) in Celsius and humidity (`RH_1` to `RH_9`) in % for every individual room in the house around every 3.3 minutes which were then averaged for 10 minutes periods. The energy data for both appliances (`Appliances`) and lights (`lights`) separately was logged every 10 minutes with m-bus energy meters in the Wh unit. 

## Acknowledgements and references 

- http://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction
- https://www.sciencedirect.com/science/article/abs/pii/S0378778816308970?via%3Dihub
