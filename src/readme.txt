1. Any learned data is called  a "sample". A sample contains three piece of information,
    i.e. total words learned, total unique word learnt and set of those unique word.
    
2. The process of creating sample is called "sampling".

3. List of sample is called a "simulation".
    It contains daily sampling from day 1 to day N.

4. "Iteration" is a list of multiple simulation. So first item of list contains a simulation from day 1 to day N,
    second item also contains another simulation from day 1 to day N and so on. Iteration is generally created to smooth out the curve.

5. Iteration data can be averaged to create an averaged simulation.
6. "Defecit" is used to describe the percentage of unique word to be removed from a sample's unique word count and unique word set.
7. Defecit can be done to individual sample, to get a new sample with random percentage of word removed from orginal sample.
8. Iteration data can be looped to make a defecit in each individual sample to create a 
new iteration data with all defecit samples.

Suggestions:
// total words = token count
// total uniquew words = type count
// replace cycle with simulation.


[[day1, day2, day3, day4, day4], [day1, day2, day3, day4], [day1, day2, day3, day4]]

[[_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4]]

        day1    day2    day3    ..dayN
dog     4       30      3           6
cat     0       1       0           0
..  
..
..


base 1 -    one two three four five [types = 5]
defecit 1 - one two three [types = 3]
enrich 1 -  one two three four six [types = 5]

t.base 2 -    one five six seven eight [ types = 5]
t.defecit 2 - one six seven eight [types = 4, -1]
t.enrich 2 -  one six seven eight nine ten [ types = 6, +2]

cumulative 
base2 =  base1 + t.base2 = one two three four five + one five six seven eight
      =  one two three four five six seven eight [ types = 8]

defecit 2 = defecit 1 + t.defecit 2 = one two three + one six seven eight
	  = one two three six seven eight [ types = 6, -2]

enrich 2 = enrich 1 + t.enrich2 = one two three four six + one six seven eight nine ten
	=  one two three four six seven eight nine ten [ types = 9, +3]

