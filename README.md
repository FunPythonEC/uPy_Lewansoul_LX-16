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
| `set_vin_limit(ID,minvin,maxvin)`       | Defines a range of voltage in which the servo works. minvin must be less than maxvin.  The voltage limits must be between 4500 - 12000 mv. In case the supplied voltage or Vin isn't in the specified range, the servo stops working. |
| `set_max_temp_limit(ID,temp)`           | Defines the max temperature in which the servo will work. `temp` can take values from 50 to 100, specified in Celsius degrees. The default value is 85 degrees Celsius. The servo will flash the led if it reaches a higher value of temperature. |
| `set_load_status(ID,status)`            | Defines whether the servo exerts torque or not. `status` can take values of 0 or 1. 1 represents the servo is loaded, it has a torque output. 0 is the default value which means unloaded. |
| `set_led_ctrl(ID,mode)`                 | Defines if the led is on/off. This is saved even if the servo is shutdowned. 0 is for always off, and 1 for always on. |
| `set_led_error(ID,fault)`               | Sets the fault that will cause the LED flashing alarm. It can have value between 0~7. |
| `goal_speed(ID,speed)`                  | Puts the servo in a mode like a DC motor. Where `speed` takes values between 0~1000. 1000 being the maximum value. If it is defined as negative. It turns the other way. |
| `joint_mode(ID)`                        | Puts the servo in joint mode, meaning it is like a normal servo, that can be used with `goal_position(angle,time)` method. This is saved even if the servo is shutdowned. |


## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">uPy_Lewansoul_LX-16</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Steven Silva</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/FunPythonEC/uPy_Lewansoul_LX-16" rel="dct:source">https://github.com/FunPythonEC/uPy_Lewansoul_LX-16</a>.

