# for acos, atan2 and sin
import math
import sys

# radian to degree
deg = 180/math.pi
# link 1 length
a1 = 10
# link 2 length
a2 = 10
# derivated based up https://www.youtube.com/watch?v=IKOGwoJ2HLk&t=311s

def ik(x, y):
    # (x, y)  need to be located inside the circle with radius a1+a2
    if (x**2 + y**2) <= (a1+ a2)**2:
        q2 = -math.acos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
        q1 = math.atan2(y, x) + math.atan2((a2*math.sin(q2)), (a1+a2*math.cos(q2)))
        # The decimal point of number is rounded to the 4th place
        return [round(q1*deg, 4), round(q2*deg, 4)]
    else:
        print("Over range!")
        # end the script execution
        sys.exit()

theta = ik(15, 1)

print(theta[0], theta[1])
  
