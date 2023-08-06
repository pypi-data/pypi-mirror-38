from autolens.galaxy import galaxy as g
from autolens.lensing import ray_tracing
from autolens.imaging import image as im
from autolens.imaging import mask
from autolens.profiles import light_profiles as lp
from autolens.profiles import mass_profiles as mp
from autolens.plotting import imaging_plotters
import os


# This is the simulated image we incorrect_fit in tutorial '1_phase'.

psf = im.PSF.simulate_as_gaussian(shape=(11, 11), sigma=0.1, pixel_scale=0.1)

image_plane_grids = mask.ImagingGrids.grids_for_simulation(shape=(130, 130), pixel_scale=0.1, psf_shape=(11, 11))

lens_galaxy = g.Galaxy(mass=mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=1.6))
source_galaxy = g.Galaxy(light=lp.SphericalExponential(centre=(0.0, 0.0), intensity=0.2, effective_radius=0.2))
tracer = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[lens_galaxy], source_galaxies=[source_galaxy],
                                             image_plane_grids=image_plane_grids)

image_simulated = im.PreparatoryImage.simulate(array=tracer.image_plane_image_for_simulation, pixel_scale=0.1,
                                               exposure_time=300.0, psf=psf, background_sky_level=0.1, add_noise=True)

path = "{}".format(os.path.dirname(os.path.realpath(__file__))) # Setup path so we can output the simulated data.
im.output_imaging_to_fits(image=image_simulated, image_path=path+'/data/1_non_linear_search_image.fits',
                                                 noise_map_path=path+'/data/1_non_linear_search_noise_map.fits',
                                                 psf_path=path+'/data/1_non_linear_search_psf.fits',
                          overwrite=True)

imaging_plotters.plot_image_subplot(image=image_simulated)

# This is the simulated image we incorrect_fit in the exercise '3_realism_and_complexity'

psf = im.PSF.simulate_as_gaussian(shape=(11, 11), sigma=0.05, pixel_scale=0.05)
image_plane_grids = mask.ImagingGrids.grids_for_simulation(shape=(130, 130), pixel_scale=0.1, psf_shape=(11, 11))

lens_galaxy = g.Galaxy(light=lp.EllipticalSersic(centre=(0.0, 0.0), axis_ratio=0.9, phi=45.0, intensity=0.04,
                                                         effective_radius=0.5, sersic_index=3.5),
                       mass=mp.EllipticalIsothermal(centre=(0.0, 0.0), axis_ratio=0.8, phi=45.0, einstein_radius=0.8))

source_galaxy = g.Galaxy(light=lp.EllipticalSersic(centre=(0.0, 0.0), axis_ratio=0.5, phi=90.0, intensity=0.03,
                                                   effective_radius=0.3, sersic_index=3.0))
tracer = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[lens_galaxy], source_galaxies=[source_galaxy],
                                             image_plane_grids=image_plane_grids)

image_simulated = im.PreparatoryImage.simulate(array=tracer.image_plane_image_for_simulation, pixel_scale=0.1,
                                               exposure_time=300.0, psf=psf, background_sky_level=0.1, add_noise=True)

path = "{}".format(os.path.dirname(os.path.realpath(__file__))) # Setup path so we can output the simulated data.
im.output_imaging_to_fits(image=image_simulated, image_path=path+'/data/3_realism_and_complexity_image.fits',
                                                 noise_map_path=path+'/data/3_realism_and_complexity_noise_map.fits',
                                                 psf_path=path+'/data/3_realism_and_complexity_psf.fits',
                          overwrite=True)

imaging_plotters.plot_image_subplot(image=image_simulated)