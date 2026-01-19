### Temporary Components V2 handler
Since OwObot is moving towards using components v2 and discord.py-self has yet to add proper support to components we will be temporarily using this approach to handle components.

~~We won't be fully unwrapping the message object by discord, instead we will recursively search the function and return required fields. This approach isn't safe but certainly easier than properly handling it!~~

Actually nwm we are going, to the best of our ability flatten up the components to a list!


I'll add proper documentation here later, lazy! :>