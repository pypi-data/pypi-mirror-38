from matplotlib import pyplot as plt

from autolens import conf
from autolens.plotting import tools_array

def plot_grid(grid, xmin=None, xmax=None, ymin=None, ymax=None,
              figsize=(12, 8), pointsize=3, xyticksize=16,
              title='Grid', titlesize=16, xlabelsize=16, ylabelsize=16,
              output_path=None, output_format='show', output_filename='grid'):

    plt.figure(figsize=figsize)
    plt.scatter(y=grid[:, 0], x=grid[:, 1], s=pointsize, marker='.')
    tools_array.set_title(title=title, titlesize=titlesize)
    plt.ylabel('y (arcsec)', fontsize=xlabelsize)
    plt.xlabel('x (arcsec)', fontsize=ylabelsize)
    plt.tick_params(labelsize=xyticksize)
    if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
        plt.axis([xmin, xmax, ymin, ymax])
    tools_array.output_figure(None, False, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot=False)

def plot_image(image, mask=None, positions=None, grid=None, as_subplot=False,
               units='arcsec', kpc_per_arcsec=None,
               xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
               figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
               title='Observed Image', titlesize=16, xlabelsize=16, ylabelsize=16,
               output_path=None, output_format='show', output_filename='observed_image'):

    if positions is not None:
        positions = list(map(lambda pos: image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos), positions))

    tools_array.plot_array(image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(image.shape, units, kpc_per_arcsec, image.xticks, image.yticks, xlabelsize,
                                           ylabelsize, xyticksize)

    # TODO : if you use set_colorbar and plt.scatter the scatter plot doesnt show...default to removing colorbar now

    if mask is None:
        tools_array.set_colorbar(cb_ticksize)
    tools_array.plot_mask(mask)
    tools_array.plot_points(positions)
    tools_array.plot_grid(grid)
    tools_array.output_figure(image, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_noise_map(noise_map, mask=None, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Noise-Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='noise_map'):


    tools_array.plot_array(noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(noise_map.shape, units, kpc_per_arcsec, noise_map.xticks, noise_map.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.plot_mask(mask)
    tools_array.output_figure(noise_map, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_psf(psf, as_subplot=False,
             units='arcsec', kpc_per_arcsec=None,
             xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
             figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
             title='PSF', titlesize=16, xlabelsize=16, ylabelsize=16,
             output_path=None, output_format='show', output_filename='psf'):

    tools_array.plot_array(psf, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(psf.shape, units, kpc_per_arcsec, psf.xticks, psf.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(psf, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_signal_to_noise_map(signal_to_noise_map, mask=None, as_subplot=False,
                             units='arcsec', kpc_per_arcsec=None,
                             xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                             figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                             title='Noise-Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                             output_path=None, output_format='show', output_filename='signal_to_noise_map'):


    tools_array.plot_array(signal_to_noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(signal_to_noise_map.shape, units, kpc_per_arcsec,
                                           signal_to_noise_map.xticks, signal_to_noise_map.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.plot_mask(mask)
    tools_array.output_figure(signal_to_noise_map, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_intensities(intensities, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Intensities', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='intensities'):

    tools_array.plot_array(intensities, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(intensities.shape, units, kpc_per_arcsec, intensities.xticks,
                                           intensities.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(intensities, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_surface_density(surface_density, as_subplot=False,
                         units='arcsec', kpc_per_arcsec=None,
                         xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                         figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                         title='Surface Density', titlesize=16, xlabelsize=16, ylabelsize=16,
                         output_path=None, output_format='show', output_filename='surface_density'):
    tools_array.plot_array(surface_density, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(surface_density.shape, units, kpc_per_arcsec, surface_density.xticks,
                                           surface_density.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(surface_density, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_potential(potential, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Potential', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='potential'):
    tools_array.plot_array(potential, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(potential.shape, units, kpc_per_arcsec, potential.xticks, potential.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(potential, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_deflections_y(deflections_y, as_subplot=False,
                       units='arcsec', kpc_per_arcsec=None,
                       xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                       figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                       title='Deflections (y)', titlesize=16, xlabelsize=16, ylabelsize=16,
                       output_path=None, output_format='show', output_filename='deflections_y'):
    tools_array.plot_array(deflections_y, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(deflections_y.shape, units, kpc_per_arcsec, deflections_y.xticks,
                                           deflections_y.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(deflections_y, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_deflections_x(deflections_x, as_subplot=False,
                       units='arcsec', kpc_per_arcsec=None,
                       xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                       figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                       title='Deflections (x)', titlesize=16, xlabelsize=16, ylabelsize=16,
                       output_path=None, output_format='show', output_filename='deflections_x'):

    tools_array.plot_array(deflections_x, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(deflections_x.shape, units, kpc_per_arcsec, deflections_x.xticks,
                                           deflections_x.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(deflections_x, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_image_plane_image(image_plane_image, mask=None, positions=None, grid=None, as_subplot=False,
                           units='arcsec', kpc_per_arcsec=None,
                           xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                           figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                           title='Image-Plane Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                           output_path=None, output_format='show', output_filename='plane_image_plane_image'):

    if positions is not None:
        positions = list(map(lambda pos: image_plane_image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos),
                             positions))

    tools_array.plot_array(image_plane_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min,
                           linthresh, linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(image_plane_image.shape, units, kpc_per_arcsec, image_plane_image.xticks,
                                           image_plane_image.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.plot_points(positions)
    tools_array.plot_mask(mask)
    tools_array.plot_grid(grid)
    tools_array.output_figure(image_plane_image, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_plane_image(plane_image, positions=None, plot_grid=False, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Plane Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='plane_image'):

    if positions is not None:
        positions = list(map(lambda pos: plane_image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos),
                             positions))

    tools_array.plot_array(plane_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min,
                           linthresh, linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(plane_image.shape, units, kpc_per_arcsec, plane_image.xticks, plane_image.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.plot_points(positions)
    if plot_grid:
        tools_array.plot_grid(plane_image.grid)
    tools_array.output_figure(plane_image, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_model_image(model_image, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='model_image'):

    tools_array.plot_array(model_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(model_image.shape, units, kpc_per_arcsec, model_image.xticks,
                                           model_image.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(model_image, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_residuals(residuals, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Residuals', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='residuals'):

    tools_array.plot_array(residuals, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(residuals.shape, units, kpc_per_arcsec, residuals.xticks, residuals.yticks,
                                           xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(residuals, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)
    
def plot_chi_squareds(chi_squareds, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Chi-Squareds', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='chi_squareds'):

    tools_array.plot_array(chi_squareds, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(chi_squareds.shape, units, kpc_per_arcsec, chi_squareds.xticks,
                                           chi_squareds.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(chi_squareds, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_contributions(contributions, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Scaled Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='contributions'):

    tools_array.plot_array(contributions, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(contributions.shape, units, kpc_per_arcsec, contributions.xticks,
                                           contributions.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(contributions, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)

def plot_scaled_model_image(scaled_model_image, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Scaled Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='scaled_model_image'):

    tools_array.plot_array(scaled_model_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(scaled_model_image.shape, units, kpc_per_arcsec, scaled_model_image.xticks,
                                           scaled_model_image.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(scaled_model_image, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_scaled_residuals(scaled_residuals, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Scaled Residuals', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='scaled_residuals'):

    tools_array.plot_array(scaled_residuals, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(scaled_residuals.shape, units, kpc_per_arcsec, scaled_residuals.xticks,
                                           scaled_residuals.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(scaled_residuals, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)


def plot_scaled_chi_squareds(scaled_chi_squareds, as_subplot=False,
                      units='arcsec', kpc_per_arcsec=None,
                      xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                      figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                      title='Scaled Chi-Squareds', titlesize=16, xlabelsize=16, ylabelsize=16,
                      output_path=None, output_format='show', output_filename='scaled_chi_squareds'):

    tools_array.plot_array(scaled_chi_squareds, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(scaled_chi_squareds.shape, units, kpc_per_arcsec, scaled_chi_squareds.xticks,
                                           scaled_chi_squareds.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(scaled_chi_squareds, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)
    
def plot_scaled_noise_map(scaled_noise_map, as_subplot=False,
                      units='arcsec', kpc_per_arcsec=None,
                      xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                      figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                      title='Scaled Noise Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                      output_path=None, output_format='show', output_filename='scaled_noise_map'):

    tools_array.plot_array(scaled_noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                           linscale)
    tools_array.set_title(title, titlesize)
    tools_array.set_xy_labels_and_ticksize(scaled_noise_map.shape, units, kpc_per_arcsec, scaled_noise_map.xticks,
                                           scaled_noise_map.yticks, xlabelsize, ylabelsize, xyticksize)
    tools_array.set_colorbar(cb_ticksize)
    tools_array.output_figure(scaled_noise_map, as_subplot, output_path, output_filename, output_format)
    tools_array.figure_close(as_subplot)