# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:43:39 2022

@author: michael
"""

import numpy as np 
import pygame 
import math 
import random as r
from scipy.stats import norm
import matplotlib.pyplot as plt


green = (0 , 255 , 0)
red = (255 , 0 , 0)
blue = (0 ,0 , 255)
estimcol = (100 , 100 , 255)
white = (255 ,255 , 255)
col  = (252, 3, 219)
black = (0 ,0 ,0)

pygame.init()
dimx , dimy = 800 , 600
surface = pygame.display.set_mode((dimx , dimy))
manholes= [(100 , 200) , (300 , 400) , (400 , 200) , (500 , 505) , (200 , 500) , (206 , 200) , (300 , 80), (100 , 100) , (200  , 150) , (150 , 200) , (200  , 150) , (300 , 350) ]
              
        
def plot_manholes(manholes) :
    for point in manholes :
        draw = pygame.draw.circle(surface, green, (point[0] , point[1]) , 5)
    for i in range(1 , len( manholes)) :
        lines = pygame.draw.line(surface , black , (manholes[i-1][0],manholes[i-1][1]) ,  (manholes[i][0],manholes[i][1]) )                         
    pygame.display.flip() 
 
starting_point =  manholes[3]
location = starting_point
n = manholes.index(location)


def move(location,  n):
    if event.key == pygame.K_RIGHT :       
        step = np.random.normal(5, 1) 
        x = manholes[n+1][0] - manholes[n][0]
        y = manholes[n+1][1] - manholes[n][1]  
        grad = y/x 
        angle = np.arctan(y/x)
        if grad != 0 and x > 0 :                                                          
            locationx = location[0] + np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (round(locationx , 2), round(locationy , 2))   
        if grad == 0 and location[0] > manholes[n+1][0]:
            locationx = location[0] - np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (np.round(locationx ,2) , np.round(locationy ,2))             
        if grad == 0 and location[0] < manholes[n+1][0]:
            locationx = location[0] + np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (np.round(locationx , 2) , np.round(locationy ,2 ))                             
        if grad != 0 and x < 0 :
            locationx = location[0] - np.cos(angle)*step
            locationy = location[1] - np.sin(angle)*step
            location = (np.round(locationx , 2), np.round(locationy , 2))    
        return location 
        
 
def sense(location , n ):      
    distance = np.sqrt((manholes[n+1][0] - location[0])**2 + (manholes[n+1][1] - location[1])**2) + np.random.normal(0, 1) 
    if distance < 5: 
        location = manholes[n+1]
        n +=1 
        return n , location  , distance

    else:
        n = n
    return n  , location , distance 

length = len(manholes)-1 

number_particles = 400

particle_location = location
particle_angle = []
particle_listi = []


def move_particles(particle_location):        
    if event.key == pygame.K_RIGHT :
        x = manholes[n+1][0] - manholes[n][0]
        y = manholes[n+1][1] - manholes[n][1]  
        grad = y/x 
        print(np.arctan(grad))
       # angle_particle = np.arctan(y/x) + np.random.normal(0, 1) 
        angle_particle = np.random.normal(np.arctan(grad), 0.5 , number_particles) 
       # particle_angle.append(angle_particle)
        step_particle = np.random.normal(5, 1, number_particles)    

        
        if grad != 0 and x > 0 :                                                          
            locationx = particle_location[0] + np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            
            particle_location = (np.round(locationx , 2), np.round(locationy , 2))   

        if grad == 0 and np.mean(particle_location[0]) > manholes[n+1][0]:
            locationx = particle_location[0] - np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            particle_location = (np.round(locationx) , np.round(locationy))    

        if grad == 0 and np.mean(particle_location[0]) < manholes[n+1][0]:
            locationx = particle_location[0] + np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            particle_location = (np.round(locationx ,2 ) , np.round(locationy ,2 ))   
                      
        if  grad != 0 and x < 0 :
             locationx = particle_location[0] - np.cos(angle_particle)*step_particle
             locationy = particle_location[1] - np.sin(angle_particle)*step_particle
             particle_location = (np.round(locationx , 2), np.round(locationy , 2))
        
        particle_listi.append(particle_location)  
        return particle_location 
     

def particle_sense(particle_location , n ):
    x1 = particle_location[0]
    y1 = particle_location[1]
    particle_distance = np.sqrt((manholes[n+1][0] - particle_location[0])**2 + (manholes[n+1][1] - particle_location[1])**2) + np.random.normal(0, 2) 
    return particle_distance 


def weight(distance , particle_distance):
    weight_particle  = norm.pdf(particle_distance, distance, 1 )
    
    return weight_particle


def resample(weight_particle , particle_location ):
    particle_list = list(zip(particle_location[0] , particle_location[1]))  
    resample = r.choices(particle_list , weight_particle , k = number_particles)
  #  particle_location = resample
    particle_location = list(zip(*resample))
    return particle_location
         
def estimated_location(particle_location , weight_particle):
    
    #estimatex = np.mean(particle_location[0])
    #estimatey = np.mean(particle_location[1])
    estim  = np.where(weight_particle ==  np.max(weight_particle))[0][0]
    estimatex = particle_location[0][estim]
    estimatey = particle_location[1][estim]
    pygame.draw.circle(surface, estimcol , (estimatex, estimatey) , 3)  
    #rmse = np.sqrt(estimatex^2 - estimatey^2)
    return estimatex , estimatey #, rmse


xplt = []
yplt = []   
rmse = []
def data(estimatex , estimatey , location):
    xval = location[0] - estimatex
    yval = location[1] - estimatey
    yplt.append(yval) 
    xplt.append(xval)
    error = np.sqrt(yval**2 + xval**2)
    rmse.append(error)
    return xplt , yplt , rmse
           
 
estimated_trajectoryx = []
estimated_trajectoryy = []
while True : 
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT :               
            pygame.quit()
            quit()    
            
    if event.type == pygame.KEYDOWN:        
        n , location , distance  = sense(location , n  )          
        if distance > 40:
            distance =  0 
            
        if n == length:    
            print('fine') 
            manholes.reverse() 
            n = 0 
            location = (manholes[0][0] , manholes[0][1])       
        else :            
            location  = move( location, n)   
            pygame.draw.circle(surface, red, (location[0]  , location[1]) , 6)
            particle_location  = move_particles(particle_location) 
            for i in range(number_particles):
                xp = particle_location[0][i]
                yp = particle_location[1][i]
                pygame.draw.circle(surface, col, (xp , yp)  , 2) 
            particle_distance = particle_sense(particle_location , n )
            
           
            weight_particle = weight(distance , particle_distance)

            if any(weight_particle) == True:
                    particle_location =  resample(weight_particle , particle_location )
            
            estimatex , estimatey = estimated_location(particle_location , weight_particle)
            estimated_trajectoryx.append(estimatex )
            estimated_trajectoryy.append(estimatey )           
            xplt , yplt , rmse  = data(estimatex , estimatey , location)
            # plt.plot(xplt) 
            # plt.plot(yplt)
            plt.plot(rmse) 
            # 
    else :
        pygame.draw.circle(surface, red, (location[0]  , location[1]) , 6)  
    
    if location in manholes:
        pygame.display.update()         
        surface.fill(white)                               
        pygame.time.delay(100)                  
        plot_manholes(manholes)  
    else :
        for i in range(number_particles):
            xp = particle_location[0][i]
            yp = particle_location[1][i]
            pygame.draw.circle(surface, col, (xp , yp)  , 2) 
            estimated_location(particle_location , weight_particle)

    pygame.display.update()         
    surface.fill(white)      
    for p in range(len(estimated_trajectoryx)):
        pygame.draw.circle(surface, estimcol , (estimated_trajectoryx[p], estimated_trajectoryy[p]) , 3)
                        
    pygame.time.delay(100)                  
    plot_manholes(manholes)        

