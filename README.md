# Temperature-Control-System

System adjusts the heating schedule individually to each room. The system consists of 5 rules that decide if the heating should be turned on or turned off. The system also checks it previous actions and remembers if the heating in the room was turned on or off. If in the next action it needs to stay turned off or on, the system makes action of remaining off/on.


System rules

Rule 1: If the current temperature is below the desired temperature, turn on the heating.

Condition: Current temperature < Desired temperature

Action: Turn on heating

Rule 2: If the current temperature is above the desired temperature, turn off the heating.

Condition: Current temperature > Desired temperature

Action: Turn off heating

Rule 3: If the outdoor temperature is above a certain threshold (set up to above 15 Celsius degrees), turn off the heating.

Condition: Outdoor temperature > Outdoor temperature threshold

Action: Turn off heating

Rule 4: If the outdoor temperature is below a certain threshold (Below 15 Celsius), check which rooms need the heating and turn on the heating. 

Condition: Outdoor temperature < Outdoor temperature threshold

Action: Check the rules 1 and 2 to control heating

Rule 5: If the heating system's energy consumption exceeds a predefined limit, turn off the heating to save energy.

Condition: Energy consumption > Energy consumption threshold

Action: Turn off the heating
