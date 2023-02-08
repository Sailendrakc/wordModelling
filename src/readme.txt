1. Any learned data is called  a "sample". A sample contains three piece of information,
    i.e. total words learned, total unique word learnt and set of those unique word.
    
2. The process of creating sample is called "sampling".

3. List of sample is called a "simulation".
    It contains daily sampling from day 1 to day N.

4. "Iteration" is a list of multiple cycles. So first item of list contains a simulation from day 1 to day N,
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

[dog, cat, deer]- > x amount (10) - 3 day1 
[dog, ball, water, stick] -> (10) - 3+4 day2