# uPy_Lewansoul_LX-16
This is a library specific to be used in MicroPython, especifically for the ESP32 and ESP8266. However, it should work in any other board with uPy that has uart ports.

This uPy script will be developed with the help of the following repository: https://github.com/maximkulkin/lewansoul-lx16a

I will only be adapting any function and constructors needed for a better use, similar to the Dynamixel library used by Robotis.



## Methods

Here every method or action that can be done with the servo will be stated. These are divided in writing and reading methods. Have in mind that most of writing methods begin with `set`, also that they have been defined in such a way that it is easy to use them. Most of them are really similar to the ones found for Dynamixel in arduino in order to keep something similar.



In most of the methods, `ID` needs to be identified, which corresponds to the ID of the servo that is going to be modified or worked with.

### Writing methods

| Method                                  | Description                                                  |
| --------------------------------------- | :----------------------------------------------------------- |
| `goal_position(ID, angle, time)`        | This method turn the servo to the specified angle in the specified time. The angle limits are between 0-240 degrees. And time goes from 0-30000 ms. |
| `start_goal_position(ID, angle,time)`   | This is a special method, which needs the same as the last method to be defined. Does the same as the last method, however, it doesn't turn as soon as the method is executed unless the method `start(ID)` is executed as well. (Explained below) |
| `start(ID)`                             | Works as a trigger for every WAIT command that is used. Triggers the last saved action in the servo. |
| `stop(ID)`                              | Stops the servo immediately.                                 |
| `set_id(ID,NID)`                        | Changes the ID of the servo, where NID corresponds to the new ID that want to be specified. |
| `set_temp_offset_angle(ID,angle)`       | Adjusts the offset angle, isn't saved, meaning it is temporary, just while the servo is on. The angle range is -30~30 degrees. Also after it is executed, the servo will rotate the defined degrees as angle. |
| `set_offset_angle(ID,angle)`            | This is the same as the last method, however, this one saves the angle specifed, even if the servo is shut downed. |
| `set_angle_limit(ID,minangle,maxangle)` | Sets the limit angle in which the servo can turn. Have in mind that `minangle` must be less than `maxangle`. Also that the angles mus be between 0~240 degrees. |
| `set_vin_limit(ID,minvin,maxvin)`       |                                                              |
| `set_max_temp_limit(ID,temp)`           |                                                              |
| `set_load_status(ID,status)`            |                                                              |
| `set_led_ctrl(ID,mode)`                 |                                                              |
| `set_led_error(ID,fault)`               |                                                              |
| `goal_speed(ID,speed)`                  |                                                              |
| `servo_mode(ID)`                        |                                                              |