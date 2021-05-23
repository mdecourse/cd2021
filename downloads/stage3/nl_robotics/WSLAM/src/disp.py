import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import settings

import cv2
import numpy as np


class Display(object):
    """
    SLAM Display
    """
    def __init__(self, agent, wall):
        self.bytearray = bytearray(settings.image_size*settings.image_size)
        self.agent = agent
        self.im = None
        self.colormap = settings.colormap
        self.visited = np.ones([settings.image_size, settings.image_size, 3])

        self.wall_disp = False
        # Agent parameters
        self.agent_radius    = settings.agent_radius
        self.agent_color     = settings.agent_color

        # Speed display
        self.speed_location  = [(60,700), (90,700)]
        self.step = 0
        # Create cv2 window
        self.display_name = 'Simultaneous Localization and Mapping (SLAM)'
        cv2.namedWindow(self.display_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.display_name, settings.window_size,settings.window_size)

    def close(self):
        cv2.destroyWindow(self.display_name)

    def update(self):
        """
        Updates the current display based on current information of the agent
        """

        if self.step % settings.steps_slam == 0:
            self.agent.slam(self.bytearray)

        self.im = self.to_image()
         
        if settings.canny_filter: 
            self.im = cv2.cvtColor(cv2.Canny(self.im, 100,150), cv2.COLOR_GRAY2RGB)
        if settings.draw_closest:
            self.draw_closest(self.im)
        self.draw_trajectory(self.im)
        self.draw_agent(self.im)     
        self.im = cv2.flip(self.im, 0) 

        self.draw_elements(self.im)        
        self.draw_speed(self.im)
        # self.im = cv2.blur(self.im,(3,3))
        cv2.imshow(self.display_name, self.im)
        key = cv2.waitKey(1) & 0xFF
        self.step += 1


    def draw_closest(self, image):
        """
        Draws lines to the closest objects right and left
        """
        angles, distances = self.agent.find_closest()
        scale = 30
        for i in range(2):
            x = self.agent.pos[0] + int(np.cos((self.agent.theta+angles[i])*np.pi/180) * distances[i]*settings.closest_line_scale) 
            y = self.agent.pos[1] + int(np.sin((self.agent.theta+angles[i])*np.pi/180) * distances[i]*settings.closest_line_scale)
            cv2.line(image, (x, y), tuple(self.agent.pos), settings.closest_line_color, 1)

    def draw_trajectory(self, image):
        """
        Draw the position history
        """
        for i in range(1, len(self.agent.position_history)):
            size = round(100./(float(i) + 33)*3)
            color = (0+i*5,0+i*5,0+i*5)
            cv2.line(image, self.agent.position_history[i-1], self.agent.position_history[i], color, 1)

    def to_image(self):
        """
        Convert bytearray to opencv color image
        """
        array = np.frombuffer(self.bytearray, dtype=np.uint8)
        gray  = np.reshape(array, [settings.image_size, settings.image_size])
        color = cv2.applyColorMap(gray, self.colormap)
        return color

    def draw_agent(self, image):
        """
        Draws the agent in the map
        """
        cv2.circle(image, (self.agent.pos[0], self.agent.pos[1]), self.agent_radius, self.agent_color, cv2.FILLED)
        # Coordinates of the angle indicator
        x = self.agent.pos[0] + int(np.cos(self.agent.theta*np.pi/180) * settings.agent_center_scale) 
        y = self.agent.pos[1] + int(np.sin(self.agent.theta*np.pi/180) * settings.agent_center_scale)
        
        cv2.circle(self.visited, (self.agent.pos[0], self.agent.pos[1]), self.agent_radius, (2,2,2), cv2.FILLED)
        self.draw_line_at_angle(image, 15, 0, (150,150,150))
        self.draw_line_at_angle(image, 15, -135, (150,150,150))
        self.draw_line_at_angle(image, 15, 135, (150,150,150))

    
    def draw_line_at_angle(self, im, length, angle, color):
        """
        Generic method for line drawing
        """
        x = self.agent.pos[0] + int(np.cos((self.agent.theta+angle)*np.pi/180) * length) 
        y = self.agent.pos[1] + int(np.sin((self.agent.theta+angle)*np.pi/180) * length)
        cv2.line(im, (x, y), tuple(self.agent.pos), color, 1)
    
    def draw_speed(self, im=None):
        """
        Draws a small graph of the current speed
        REFACTORING NEEDED
        """
        origin = self.speed_location
        off = 500
        if im is None:
            im = self.to_image()
        sp = self.agent.current_speed_API()
        im=cv2.rectangle(im, origin[0], (origin[0][0]+20, origin[0][1]-int(sp[0]*settings.speed_limit*1.5)), (240, 150, 150), cv2.FILLED)
        im=cv2.rectangle(im, origin[1], (origin[1][0]+20, origin[1][1]-int(sp[1]*settings.speed_limit*1.5)), (240, 150, 150), cv2.FILLED)
        cv2.line(im, (50,off+200), (120,off+200), (150,150,150), 1)
        cv2.line(im, (50,off+240), (120,off+240), (150,150,150), 1)
        cv2.line(im, (50,off+160), (120,off+160), (150,150,150), 1)

    def draw_elements(self, img):
        """
        Draw the elements and text
        """
        off = 500
        cv2.rectangle(img, (0, off+120), (280,off+300), (150,150,150),cv2.FILLED)
        cv2.rectangle(img, (50,off+140), (120, off+260),(255,255,255), cv2.FILLED)
        cv2.rectangle(img, (50,off+140), (120, off+260),(0,0,0), 1)
        cv2.putText(img, " L  R", (60,off+155), cv2.FONT_HERSHEY_PLAIN,1, (0,0,0), 1)
        cv2.putText(img, "0", (30,off+205), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
        cv2.putText(img, str(-settings.speed_limit), (22,off+245), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
        cv2.putText(img, str(settings.speed_limit), (30,off+165), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
        cv2.putText(img, "Step: {}".format(self.step), (150,off+150), cv2.FONT_HERSHEY_PLAIN, (1), (0,0,0),1)
        

