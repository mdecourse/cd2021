-- The decimal point of number x is rounded to the nth place
function round(x, n)
    n = math.pow(10, n or 0)
    x = x * n
    if x >= 0 then x = math.floor(x + 0.5) else x = math.ceil(x - 0.5) end
    return x / n
end

-- radian to degree
deg = 180/math.pi
-- link 1 length
a1 = 10
-- link 2 length
a2 = 10
-- derivated based upon https://www.youtube.com/watch?v=IKOGwoJ2HLk&t=311s
function ik(x, y)
    -- (x, y) need to be located inside the circle with radius a1+a2
    if (x^2 + y^2) <= (a1+ a2)^2 then
        q2 = -math.acos((x^2+y^2-a1^2-a2^2)/(2*a1*a2))
        q1 = math.atan2(y, x) + math.atan2((a2*math.sin(q2)), (a1+a2*math.cos(q2)))
        return {round(q1*deg, 4), round(q2*deg, 4)}
    else
        print("Over range!")
        -- end the script execution
        os.exit()
    end
end

theta = ik(15, 1)

print(theta[1], theta[2])
  
