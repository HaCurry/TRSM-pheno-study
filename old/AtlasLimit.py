#!/usr/bin/env python

import json
import argparse
import glob
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import atlas_mpl_style as ampl
import matplotlib.patheffects as path_effects
import pathlib
import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot the limit on 2d space.')
    parser.add_argument('inputs', nargs="+", help='The input json files')
    parser.add_argument('-c', '--coeff', default=1, type=float, help='Coefficient to be applied to the limit. Useful for unit conversion.')
    parser.add_argument('--log', action='store_true', help='Log scale')
    parser.add_argument('--observed', action=argparse.BooleanOptionalAction, default=False, help='Print the limit value on the point.')
    parser.add_argument('--x-lim', nargs='+', type=float, help='Range of the x axis.')
    parser.add_argument('--y-lim', nargs='+', type=float, help='Range of the y axis.')
    parser.add_argument('--z-lim', nargs='+', type=float, help='Range of the z axis.')
    parser.add_argument('--cmap', default='viridis', type=str, help='Cmap color palette.')
    parser.add_argument('--label', type=str, nargs="+", default=["Expected upper limit"], help='Text to be printed below the ATLAS label.')
    parser.add_argument('--text', action=argparse.BooleanOptionalAction, default=True, help='Print the limit value on the point.')
    parser.add_argument('-o', '--output-dir', help='Output directory.')
    parser.add_argument('-n', '--output-name', help='Output name')
    args = parser.parse_args()

    ## Open the json inputs
    inputs = args.inputs
    #inputs = glob.glob(args.input_path+"/*")
    
    
    limits = []
    for json_in in inputs:
        with open(json_in) as json_file:
            data = json.load(json_file)
            limits.append(data)
    ## convert it to dataframe
    limits = pd.DataFrame(limits)

    ## extract expected limits and save them as columns
    limit_exp_min2 = []
    limit_exp_min1 = []
    limit_exp_0 = []
    limit_exp_plus1 = []
    limit_exp_plus2 = []
    for index, row in limits.iterrows():
        limit_exp_min2.append(row["limit_exp"][0])
        limit_exp_min1.append(row["limit_exp"][1])
        limit_exp_0.append(row["limit_exp"][2])
        limit_exp_plus1.append(row["limit_exp"][3])
        limit_exp_plus2.append(row["limit_exp"][4])
    limits['limit_exp_min2'] = limit_exp_min2
    limits['limit_exp_min1'] = limit_exp_min1
    limits['limit_exp_0'] = limit_exp_0
    limits['limit_exp_plus1'] = limit_exp_plus1
    limits['limit_exp_plus2'] = limit_exp_plus2
    
    # coeff is just a single value
    try:
        coeff = limits['signal_XS']
    except:
        coeff = args.coeff

    ## apply coefficient to the limit
    limits['limit_obs'] = limits['limit_obs'] * coeff
    limits['limit_exp_min2'] = limits['limit_exp_min2'] * coeff
    limits['limit_exp_min1'] = limits['limit_exp_min1'] * coeff
    limits['limit_exp_0'] = limits['limit_exp_0'] * coeff
    limits['limit_exp_plus1'] = limits['limit_exp_plus1'] * coeff
    limits['limit_exp_plus2'] = limits['limit_exp_plus2'] * coeff 

    ## Remove duplicates and pick one with best expected limit
    c_mins = limits.groupby(['x', 'y']).limit_exp_0.transform(min)
    limits = limits.loc[limits.limit_exp_0 == c_mins]


    ## Create the grid
    x_min, x_max = limits['x'].min(), limits['x'].max()
    y_min, y_max = limits['y'].min(), limits['y'].max()
    grid_x, grid_y = np.mgrid[x_min:x_max:100j, y_min:y_max:200j]
    ## Interpolate the limits on the grid
    if args.observed:
        grid_limit = griddata(limits[['x', 'y']], limits['limit_obs'], (grid_x, grid_y), method='cubic')
    else:
        grid_limit = griddata(limits[['x', 'y']], limits['limit_exp_0'], (grid_x, grid_y), method='cubic')


    ampl.use_atlas_style() # activate ATLAS style    
    fig, ax = plt.subplots()
    im = ax.imshow(grid_limit.T, extent=(x_min,x_max,y_min,y_max), origin='lower', aspect='auto', cmap=args.cmap, 
                   norm=LogNorm() if args.log else None, 
                   vmin=args.z_lim[0] if args.z_lim else None, 
                   vmax=args.z_lim[1] if args.z_lim else None)
    cbar = fig.colorbar(im, ax=ax)

    ## Remove values outside the grid                                                                                                         
    if args.x_lim:
        limits = limits[limits['x'] > args.x_lim[0]]
        limits = limits[limits['x'] < args.x_lim[1]]

    if args.y_lim:
        limits = limits[limits['y'] > args.y_lim[0]]
        limits = limits[limits['y'] < args.y_lim[1]]


    print(limits)

    ## print the limit on the plot
    if args.text:
        for index, row in limits.iterrows():

            if args.observed:
                text = ax.text(row['x'], row['y'], f"{row['limit_obs']:0.2f}",
                           color="black", ha="left", va="bottom")
            else:
                text = ax.text(row['x'], row['y'], f"{row['limit_exp_0']:0.2f}", 
                           color="black", ha="left", va="bottom")
            text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                                   path_effects.Normal()])

    ## draw atlas label
    ampl.draw_atlas_label(0.05, 0.92, ax=ax, status='int', fontsize=20)
    if args.label:
        for i, t in enumerate(args.label):
            ax.text(0.05, 0.89-((i+1)*0.05), t, transform=ax.transAxes)
    ampl.set_ylabel("$m_S$ [GeV]", ax=ax)
    ampl.set_xlabel("$m_X$ [GeV]", ax=ax)
    ampl.set_zlabel(r'$\sigma( pp \rightarrow X)\times$ BR$ (X \rightarrow SH  \rightarrow bb \gamma \gamma)$ [fb]', ax=ax, cbar=cbar)

    if args.x_lim: ax.set_xlim(args.x_lim[0], args.x_lim[1])
    if args.y_lim: ax.set_ylim(args.y_lim[0], args.y_lim[1])

    plt.tight_layout()


    ## create the dir if it does not exist
    pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    ## save the png
    fig.savefig(f'{args.output_dir}/{args.output_name}.png', format='png')
    
    
    
    
    
    
