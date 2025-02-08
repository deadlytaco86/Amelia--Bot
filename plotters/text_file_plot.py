import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def just_y(c_dir, y, params, log, *args):
    matplotlib.use('Agg')

    if not log:
        plot_id = ''
    else:
        plot_id = 'semilog'
    filename = f"{c_dir}/bot_data/graph_data/{plot_id}graph.png"

    if params == 3:
        plt.plot(y if not log else np.log(y),'b-')
    else:
        plt.plot(y if not log else np.log(y), 'b.')
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
    plt.minorticks_on()
    plt.title(f'{plot_id} {args[0]}')
    plt.xlabel(args[1])
    plt.ylabel(args[2])
    plt.savefig(filename)
    plt.close()
    return filename

def x_and_y(c_dir, x, y, params, logx, logy, *args):
    matplotlib.use('Agg')

    if not logx and not logy:
        plot_id = ''
    elif logy and not logx:
        plot_id = 'semilog'
    else:
        plot_id = 'loglog'
    filename = f"{c_dir}/bot_data/graph_data/{plot_id}graph.png"

    if params == 3:
        plt.plot(x if not logx else np.log(x),y if not logy else np.log(y),'b-')
    else:
        plt.plot(x if not logx else np.log(x),y if not logy else np.log(y),'b.')
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
    plt.minorticks_on()
    plt.title(f'{plot_id} {args[0]}')
    plt.xlabel(args[1])
    plt.ylabel(args[2])
    plt.savefig(filename)
    plt.close()
    return filename

def x_y_err(c_dir, x, y, err, params, logx, logy, *args):
    matplotlib.use('Agg')

    if logy:
        err = (np.log(y + err) - np.log(y - err))/2

    if not logx and not logy:
        plot_id = ''
    elif logy and not logx:
        plot_id = 'semilog'
    else:
        plot_id = 'loglog'
    filename = f"{c_dir}/bot_data/graph_data/{plot_id}graph.png"

    if params == 3:
        plt.errorbar(x if not logx else np.log(x),y if not logy else np.log(y), yerr=err, fmt='o', ecolor='black', elinewidth=0.6, color='blue', capsize=3.5)
        plt.plot(x if not logx else np.log(x),y if not logy else np.log(y),'b-')
    else:
        plt.errorbar(x if not logx else np.log(x),y if not logy else np.log(y), yerr=err, fmt='o', ecolor='black', elinewidth=0.6, color='blue', capsize=3.5)
    plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
    plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
    plt.minorticks_on()
    plt.title(f'{plot_id} {args[0]}')
    plt.xlabel(args[1])
    plt.ylabel(args[2])
    plt.savefig(filename)
    plt.close()
    return filename

def create_txt_plots(c_dir, params, *args):
    data = np.loadtxt(f'{c_dir}/bot_data/graph_data/txt_data.txt')
    filenames = []

    if len(data.shape) == 1:
        y = data
        if np.min(y) > 0:
            filename = just_y(c_dir, y, params, False, *args)
            log_filename = just_y(c_dir, y, params, True, *args)
            filenames.append(filename)
            filenames.append(log_filename)
        else:
            filename = just_y(c_dir, y, params, False, *args)
            filenames.append(filename)
        return filenames
    
    elif data.shape[1] == 2:
        x = data[:,0]
        y = data[:,1]
        if np.min(x) > 0 and np.min(y) > 0:
            filename = x_and_y(c_dir, x, y, params, False, False, *args)
            semilog_filename = x_and_y(c_dir, x, y, params, False, True, *args)
            loglog_filename = x_and_y(c_dir, x, y, params, True, True, *args)
            filenames.append(filename)
            filenames.append(semilog_filename)
            filenames.append(loglog_filename)
        elif np.min(y) > 0:
            filename = x_and_y(c_dir, x, y, params, False, False, *args)
            semilog_filename = x_and_y(c_dir, x, y, params, False, True, *args)
            filenames.append(filename)
            filenames.append(semilog_filename)
        else:
            filename = x_and_y(c_dir, x, y, params, False, False, *args)
            filenames.append(filename)
        return filenames
    
    elif data.shape[1] == 3:
        x = data[:,0]
        y = data[:,1]
        err = data[:,2]
        if np.min(x) > 0 and np.min(y) > 0:
            filename = x_y_err(c_dir, x, y, err, params, False, False, *args)
            semilog_filename = x_y_err(c_dir, x, y, err, params, False, True, *args)
            loglog_filename = x_y_err(c_dir, x, y, err, params, True, True, *args)
            filenames.append(filename)
            filenames.append(semilog_filename)
            filenames.append(loglog_filename)
        elif np.min(y) > 0:
            filename = x_y_err(c_dir, x, y, err, params, False, False, *args)
            semilog_filename = x_y_err(c_dir, x, y, err, params, False, True, *args)
            filenames.append(filename)
            filenames.append(semilog_filename)
        else:
            filename = x_y_err(c_dir, x, y, err, params, False, False, *args)
            filenames.append(filename)
        return filenames