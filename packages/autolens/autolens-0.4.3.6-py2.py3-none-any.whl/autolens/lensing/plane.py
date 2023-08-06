from functools import wraps

import numpy as np
from astropy import constants

from autolens import exc
from autolens.imaging import imaging_util
from autolens.imaging import mask as msk
from autolens.imaging import scaled_array


def cosmology_check(func):
    """
    Wrap the function in a function that, if the grid is a sub-grid (grids.SubGrid), rebins the computed values to  the
    _data-grid by taking the mean of each set of sub-gridded values.

    Parameters
    ----------
    func : (profiles, *args, **kwargs) -> Object
        A function that requires transformed coordinates
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """

        Parameters
        ----------
        self
        args
        kwargs

        Returns
        -------
            A value or coordinate in the same coordinate system as those passed in.
        """

        if self.cosmology is not None:
            return func(self, *args, *kwargs)
        else:
            return None

    return wrapper


class Plane(object):

    def __init__(self, galaxies, grids, borders=None, compute_deflections=True, cosmology=None):
        """A plane represents a set of galaxies at a given redshift in a ray-tracer and a the grid of _data-plane \
        or lensed coordinates.

        From a plane, the _data's of its galaxies can be computed (in both the _data-plane and source-plane). The \
        surface-density, potential and deflection angles of the galaxies can also be computed.

        Parameters
        -----------
        galaxies : [Galaxy]
            The list of lens galaxies in this plane.
        grids : mask.ImagingGrids
            The grids of (x,y) arc-second coordinates of this plane.
        compute_deflections : bool
            If true, the deflection-angles of this plane's coordinates are calculated use its galaxy's mass-profiles.
        """

        self.galaxies = galaxies

        if not galaxies:
            raise exc.RayTracingException('An empty list of galaxies was supplied to Plane')

        if cosmology is not None:
            if any([redshift is None for redshift in self.galaxy_redshifts]):
                raise exc.RayTracingException('A cosmology has been supplied to ray-tracing, but a galaxy does not'
                                              'have a redshift. Either do not supply a cosmology or give the galaxy'
                                              'a redshift.')

        if any([redshift is not None for redshift in self.galaxy_redshifts]):
            if not all([galaxies[0].redshift == galaxy.redshift for galaxy in galaxies]):
                raise exc.RayTracingException('The galaxies supplied to A Plane have different redshifts or one galaxy'
                                              'does not have a redshift.')

        self.grids = grids
        self.borders = borders

        if compute_deflections:

            def calculate_deflections(grid):
                return sum(map(lambda galaxy: galaxy.deflections_from_grid(grid), galaxies))

            self.deflections = self.grids.apply_function(calculate_deflections)
        else:
            self.deflections = None

        self.cosmology = cosmology

    # TODO : The map function isn't passing the class attributes correcty. We shouldbe able to refactor this
    # TODO : doing it messy for now!

    def trace_grids_to_next_plane(self):
        """Trace this plane's grids to the next plane, using its deflection angles."""

        if isinstance(self.grids.image, msk.PaddedImageGrid):
            image_grid = msk.PaddedImageGrid(arr=self.grids.image - self.deflections.image, mask=self.grids.image.mask,
                                             image_shape=self.grids.image.image_shape)
        elif isinstance(self.grids.image, msk.ImageGrid):
            image_grid = msk.ImageGrid(arr=self.grids.image - self.deflections.image, mask=self.grids.image.mask)

        if isinstance(self.grids.sub, msk.PaddedSubGrid):
            sub_grid = msk.PaddedSubGrid(self.grids.sub - self.deflections.sub, self.grids.sub.mask,
                                         self.grids.sub.image_shape, self.grids.sub.sub_grid_size)
        elif isinstance(self.grids.sub, msk.SubGrid):
            sub_grid = msk.SubGrid(self.grids.sub - self.deflections.sub, self.grids.sub.mask,
                                   self.grids.sub.sub_grid_size)

        blurring_grid = msk.ImageGrid(arr=self.grids.blurring - self.deflections.blurring, mask=None)
        return msk.ImagingGrids(image=image_grid, sub=sub_grid, blurring=blurring_grid)

    @property
    def galaxy_redshifts(self):
        return [galaxy.redshift for galaxy in self.galaxies]

    @property
    def redshift(self):
        return self.galaxies[0].redshift

    @property
    def constant_kpc(self):
        # noinspection PyUnresolvedReferences
        return constants.c.to('kpc / s').value ** 2.0 / (4 * math.pi * constants.G.to('kpc3 / M_sun s2').value)

    @property
    @cosmology_check
    def arcsec_per_kpc_proper(self):
        return self.cosmology.arcsec_per_kpc_proper(z=self.redshift).value

    @property
    @cosmology_check
    def kpc_per_arcsec_proper(self):
        return 1.0 / self.arcsec_per_kpc_proper

    @property
    @cosmology_check
    def angular_diameter_distance_to_earth(self):
        return self.cosmology.angular_diameter_distance(self.redshift).to('kpc').value

    @property
    def has_light_profile(self):
        return any(list(map(lambda galaxy: galaxy.has_light_profile, self.galaxies)))

    @property
    def has_pixelization(self):
        return any(list(map(lambda galaxy: galaxy.has_pixelization, self.galaxies)))

    @property
    def has_regularization(self):
        return any(list(map(lambda galaxy: galaxy.has_regularization, self.galaxies)))

    @property
    def has_hyper_galaxy(self):
        return any(list(map(lambda galaxy: galaxy.has_hyper_galaxy, self.galaxies)))

    @property
    def hyper_galaxies(self):
        return [galaxy.hyper_galaxy for galaxy in self.galaxies]

    @property
    def has_padded_grids(self):
        return isinstance(self.grids.image, msk.PaddedImageGrid)

    @property
    def mapper(self):

        galaxies_with_pixelization = list(filter(lambda galaxy: galaxy.has_pixelization, self.galaxies))

        if len(galaxies_with_pixelization) == 0:
            return None
        if len(galaxies_with_pixelization) == 1:
            pixelization = galaxies_with_pixelization[0].pixelization
            return pixelization.mapper_from_grids_and_borders(self.grids, self.borders)
        elif len(galaxies_with_pixelization) > 1:
            raise exc.PixelizationException('The number of galaxies with pixelizations in one plane is above 1')

    @property
    def regularization(self):

        galaxies_with_regularization = list(filter(lambda galaxy: galaxy.has_regularization, self.galaxies))

        if len(galaxies_with_regularization) == 0:
            return None
        if len(galaxies_with_regularization) == 1:
            return galaxies_with_regularization[0].regularization
        elif len(galaxies_with_regularization) > 1:
            raise exc.PixelizationException('The number of galaxies with regularizations in one plane is above 1')

    @property
    def image_plane_image(self):
        return self.grids.image.scaled_array_from_array_1d(self._image_plane_image)

    @property
    def image_plane_image_for_simulation(self):
        if not self.has_padded_grids:
            raise exc.RayTracingException(
                'To retrieve an _data plane _data for the simulation, the grids in the tracer'
                'must be padded grids')
        return self.grids.image.map_to_2d_keep_padded(self._image_plane_image)

    @property
    def _image_plane_image(self):
        return sum([intensities_from_grid(self.grids.sub, [galaxy]) for galaxy in self.galaxies])

    @property
    def _image_plane_image_of_galaxies(self):
        return list([intensities_from_grid(self.grids.sub, [galaxy]) for galaxy in self.galaxies])

    @property
    def _image_plane_blurring_image(self):
        return sum([intensities_from_grid(self.grids.blurring, [galaxy]) for galaxy in self.galaxies])

    @property
    def plane_image(self):
        return plane_image_from_grid_and_galaxies(shape=self.grids.image.mask.shape,
                                                  grid=self.grids.image.unlensed_grid, galaxies=self.galaxies)

    @property
    def surface_density(self):
        _surface_density = sum([surface_density_from_grid(self.grids.sub.unlensed_grid, [galaxy]) for galaxy in
                                self.galaxies])
        return self.grids.image.scaled_array_from_array_1d(_surface_density)

    @property
    def potential(self):
        _potential = sum([potential_from_grid(self.grids.sub.unlensed_grid, [galaxy]) for galaxy in self.galaxies])
        return self.grids.image.scaled_array_from_array_1d(_potential)

    @property
    def deflections_y(self):
        return self.grids.image.scaled_array_from_array_1d(self._deflections[:, 0])

    @property
    def deflections_x(self):
        return self.grids.image.scaled_array_from_array_1d(self._deflections[:, 1])

    @property
    def _deflections(self):
        return sum([deflections_from_grid(self.grids.sub.unlensed_grid, [galaxy]) for galaxy in self.galaxies])


class PlanePositions(object):

    def __init__(self, galaxies, positions, compute_deflections=True, cosmology=None):
        """A plane represents a set of galaxies at a given redshift in a ray-tracer and the positions of _data-plane \
        coordinates which mappers close to one another in the source-plane.

        Parameters
        -----------
        galaxies : [Galaxy]
            The list of lens galaxies in this plane.
        positions : [[[]]]
            The (x,y) arc-second coordinates of _data-plane pixels which (are expected to) mappers to the same
            location(s) in the final source-plane.
        compute_deflections : bool
            If true, the deflection-angles of this plane's coordinates are calculated use its galaxy's mass-profiles.
        """

        self.galaxies = galaxies
        self.positions = positions

        if compute_deflections:
            def calculate_deflections(positions):
                return sum(map(lambda galaxy: galaxy.deflections_from_grid(positions), galaxies))

            self.deflections = list(map(lambda positions: calculate_deflections(positions), self.positions))

        self.cosmology = cosmology

    def trace_to_next_plane(self):
        """Trace the positions to the next plane."""
        return list(map(lambda positions, deflections: np.subtract(positions, deflections),
                        self.positions, self.deflections))


class PlaneImage(scaled_array.ScaledRectangularPixelArray):

    def __init__(self, array, pixel_scales, grid):
        self.grid = grid
        self.pixel_scales = pixel_scales
        super(PlaneImage, self).__init__(array=array, pixel_scales=pixel_scales)


def sub_to_image_grid(func):
    """
    Wrap the function in a function that, if the grid is a sub-grid (grids.SubGrid), rebins the computed values to
    the _data-grid by taking the mean of each set of sub-gridded values.

    Parameters
    ----------
    func : (profiles, *args, **kwargs) -> Object
        A function that requires transformed coordinates
    """

    @wraps(func)
    def wrapper(grid, galaxies, *args, **kwargs):
        """

        Parameters
        ----------
        grid : ndarray
            PlaneCoordinates in either cartesian or profiles coordinate system
        args
        kwargs

        Returns
        -------
            A value or coordinate in the same coordinate system as those passed in.
        """

        result = func(grid, galaxies, *args, *kwargs)

        if isinstance(grid, msk.SubGrid):
            return grid.sub_data_to_image(result)
        else:
            return result

    return wrapper


@sub_to_image_grid
def intensities_from_grid(grid, galaxies):
    return sum(map(lambda g: g.intensities_from_grid(grid), galaxies))


@sub_to_image_grid
def surface_density_from_grid(grid, galaxies):
    return sum(map(lambda g: g.surface_density_from_grid(grid), galaxies))


@sub_to_image_grid
def potential_from_grid(grid, galaxies):
    return sum(map(lambda g: g.potential_from_grid(grid), galaxies))


# TODO : There will be a much cleaner way to apply sub data to surface_density to the array wihtout the need for a
# transpose

def deflections_from_grid(grid, galaxies):
    deflections = sum(map(lambda galaxy: galaxy.deflections_from_grid(grid), galaxies))
    if isinstance(grid, msk.SubGrid):
        return np.asarray([grid.sub_data_to_image(deflections[:, 0]), grid.sub_data_to_image(deflections[:, 1])]).T
    return sum(map(lambda galaxy: galaxy.deflections_from_grid(grid), galaxies))


def deflections_from_sub_grid(sub_grid, galaxies):
    return sum(map(lambda galaxy: galaxy.deflections_from_grid(sub_grid), galaxies))


def deflections_from_grid_collection(grid_collection, galaxies):
    return grid_collection.apply_function(lambda grid: deflections_from_sub_grid(grid, galaxies))


def plane_image_from_grid_and_galaxies(shape, grid, galaxies):
    y_min = np.amin(grid[:, 0])
    y_max = np.amax(grid[:, 0])
    x_min = np.amin(grid[:, 1])
    x_max = np.amax(grid[:, 1])

    y_pixel_scale = ((y_max - y_min) / shape[0])
    x_pixel_scale = ((x_max - x_min) / shape[1])

    uniform_grid = imaging_util.image_grid_1d_masked_from_mask_and_pixel_scales(mask=np.full(shape=shape,
                                                                                             fill_value=False),
                                                                                pixel_scales=(
                                                                                    y_pixel_scale, x_pixel_scale))

    image_1d = sum([intensities_from_grid(uniform_grid, [galaxy]) for galaxy in galaxies])

    image_2d = imaging_util.map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(array_1d=image_1d, shape=shape)

    return PlaneImage(array=image_2d, pixel_scales=(y_pixel_scale, x_pixel_scale), grid=grid)


def traced_collection_for_deflections(grids, deflections):
    def subtract_scaled_deflections(grid, scaled_deflection):
        return np.subtract(grid, scaled_deflection)

    result = grids.map_function(subtract_scaled_deflections, deflections)

    return result
