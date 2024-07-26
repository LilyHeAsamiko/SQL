# From the Deep

In this problem, you'll write freeform responses to the questions provided in the specification.

## Random Partitioning

Advantage: 
The observations will be evenly distributed. (High robust: Even any specific processor process one  specific boat won't mislead by past experience or bias.)
Disadvantage: 
The researcher will need to run the query on all of the boats.(Researcher cannot know which boat get one specific observation.)

## Partitioning by Hour

Advantage: 
The researcher will need to run the query on only one specific boat for searching one specific observation with time stamp.(High efficiency.)

Disadvantage:
The observations will not be evenly distributed. (One process one specific boat might be misled by past experiences.)


## Partitioning by Hash Value

Advantage: 
The observations will be evenly distributed and encoded. (High robust and safe: Even any specific 
processor process one  specific boat won't mislead by past experience or bias.)
Disadvantage: 
The researcher will need to run the query on all of the boats.(Researcher cannot 
know which boat get one specific observation.)

