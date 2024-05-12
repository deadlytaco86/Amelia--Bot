import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
import os


def animate(e, a, mass):
    plt.rcParams['savefig.dpi']=70
    import matplotlib
    matplotlib.use('cairo')
    matplotlib.rc('figure', max_open_warning = 0) 
    #t_start_loading = time.time() ########################################

    ##### constants

    timesteps = 60
    gif_fps = 4
    plt_dist_past_orbit = 0.4
    sun_size_of_plot = 0.01
    planet_size_of_sun = 0.333
    save_path = 'C://Desktop//Discord Bot//bot_data//orbit_plots//'
    plot_size = (6,6)
    orbit_points = 400
    G = 6.6743e-11
    AU = 149597870700
    MS = 1.989e30

    ##### create the orbit path and params

    theta = np.linspace(0, 2*np.pi, orbit_points)
    r = a*(1 - e*e) / (1 + e*np.cos(theta))
    x_s = r*np.cos(theta)
    y_s = r*np.sin(theta)

    periheleon = a*(1 - e*e) / (1 + e*np.cos(0))
    aphelion = a*(1 - e*e) / (1 + e*np.cos(np.pi))

    P = np.sqrt(4 * np.pi**2 / (G * mass * MS) * (a * AU)**3)

    if P > 30000000.0:
        time_mode = 'years'
        period = P/60/60/24/365.24219
    elif P > 300000.0:
        time_mode = 'days'
        period = P/60/60/24
    else:
        time_mode = 'hours'
        period = P/60/60

    ##### plot limits, offsets and dot sizes

    xmin = - np.max(r) - plt_dist_past_orbit
    xmax = np.min(r) + plt_dist_past_orbit
    xlims = (xmin, xmax)
    ymin = -a - plt_dist_past_orbit
    ymax =  a + plt_dist_past_orbit
    ylims = (ymin, ymax)
    window_size = xmax - xmin

    x_off = window_size/40
    t_off = window_size/43
    v_off = window_size/25

    if e > 0.9:
        sun_size_of_plot = sun_size_of_plot*(10*(1-e))**2
    rel_planet_size = planet_size_of_sun**2
    sun_size = 30000*sun_size_of_plot
    planet_size = 30000*rel_planet_size*sun_size_of_plot

    #print(f'loading time was {time.time() - t_start_loading}') ########################################

    ##### create plots

    filenames = []
    for i in range(timesteps):
        #start_pass = time.time() ########################################
        big_e = 2*np.pi * i/timesteps
        t = period/(2*np.pi) * (big_e - e*np.sin(big_e))

        radius = a*(1 - e*np.cos(big_e))
        right = np.sqrt((1+e)/(1-e)) * np.tan(big_e/2)
        theta_p = 2*np.arctan(right)
        px = radius*np.cos(theta_p)
        py = radius*np.sin(theta_p)

        v = np.sqrt(G * MS * (2/(radius*AU) - 1/(a*AU)))

        plt.figure(figsize=(plot_size))
        plt.title(f'a = {a} AU, e = {e}, star mass = {mass} solar masses')
        plt.xlim(xlims)
        plt.ylim(ylims)
        plt.plot(x_s, y_s, 'gray')
        plt.scatter(0, 0, sun_size, color='orange')
        plt.scatter(px, py, planet_size, color='#2dc23b')
        plt.text(px + x_off, py + t_off, f'{np.round(t,2)} {time_mode}')
        plt.text(px + x_off, py - x_off/2.5, f'{np.round(radius,3)} AU')
        plt.text(px + x_off, py - v_off, f'{np.round(v/1000,2)} km/s')
        plt.text(xmin + x_off, ymin + x_off*2.4, f'per: {np.round(periheleon,3)} AU')
        plt.text(xmin + x_off, ymin + x_off*1.2, f'aph: {np.round(aphelion,3)} AU')
        plt.text(xmin + x_off, ymin, f'P: {np.round(period,3)} {time_mode}')
        plt.axis('off')
        graph_name = f'at angle {i}.png'
        #graph_done_time = time.time() ########################################
        plt.savefig(save_path + graph_name)
        #save_done_time = time.time() ########################################
        #print(f'graph finished in {graph_done_time - start_pass}') ########################################
        #print(f'save time is {save_done_time - graph_done_time}') ########################################
        plt.clf()
        filenames.append(graph_name)

    plt.close()
    #gif_start = time.time() ########################################
    frames = [Image.open(save_path + filename) for filename in filenames[1:]]
    frame_one = Image.open(save_path + filenames[0])
    frame_one.save("C://Desktop//Discord Bot//bot_data//graph_data//Orbit Animation.gif", format="GIF", append_images=frames, save_all=True, duration=1000/gif_fps, loop=0)
    #print(f'gif finished in {time.time() - gif_start}') ########################################
    #print(f'total time is {time.time() - t_start_loading}') ########################################
    for i in range(timesteps):
        os.remove(f'C://Desktop//Discord Bot//bot_data//orbit_plots//at angle {i}.png')


#animate(0.9, 10, 1)

