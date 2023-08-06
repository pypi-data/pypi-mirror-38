import numpy as np

from autolens import exc
from autolens.inversion import inversions
from autolens.lensing import lensing_image as li
from autolens.lensing import ray_tracing

minimum_value_profile = 0.1


def fit_lensing_image_with_tracer(lensing_image, tracer, padded_tracer=None, hyper_model_image=None,
                                  hyper_galaxy_images=None, hyper_minimum_values=None, plane_shape=(30, 30)):
    """Fit.

    Parameters
    -----------
    lensing_image : li.LensingImage
        Lensing _data
    tracer : ray_tracing.AbstractTracer
        tracer
    """

    if tracer.has_light_profile and not tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return ProfileFit(lensing_image=lensing_image, tracer=tracer, padded_tracer=padded_tracer,
                              plane_shape=plane_shape)
        elif tracer.has_hyper_galaxy:
            return HyperProfileFit(lensing_image=lensing_image, tracer=tracer, hyper_model_image=hyper_model_image,
                                   hyper_galaxy_images=hyper_galaxy_images, hyper_minimum_values=hyper_minimum_values,
                                   padded_tracer=padded_tracer, plane_shape=plane_shape)

    elif not tracer.has_light_profile and tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return InversionFit(lensing_image=lensing_image, tracer=tracer)
        elif tracer.has_hyper_galaxy:
            return HyperInversionFit(lensing_image=lensing_image, tracer=tracer, hyper_model_image=hyper_model_image,
                                     hyper_galaxy_images=hyper_galaxy_images, hyper_minimum_values=hyper_minimum_values)

    elif tracer.has_light_profile and tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return ProfileInversionFit(lensing_image=lensing_image, tracer=tracer, padded_tracer=padded_tracer)
        elif tracer.has_hyper_galaxy:
            return HyperProfileInversionFit(lensing_image=lensing_image, tracer=tracer,
                                            hyper_model_image=hyper_model_image,
                                            hyper_galaxy_images=hyper_galaxy_images,
                                            hyper_minimum_values=hyper_minimum_values, padded_tracer=padded_tracer)

    else:

        raise exc.FittingException('The incorrect_fit routine did not call a Fit class - check the '
                                   'properties of the tracer')


def fast_likelihood_from_lensing_image_and_tracer(lensing_image, tracer, hyper_model_image=None,
                                                  hyper_galaxy_images=None, hyper_minimum_values=None):
    if tracer.has_light_profile and not tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return ProfileFit.fast_likelihood(lensing_image=lensing_image, tracer=tracer)
        elif tracer.has_hyper_galaxy:
            return HyperProfileFit.fast_scaled_likelihood(lensing_image=lensing_image, tracer=tracer,
                                                          hyper_model_image=hyper_model_image,
                                                          hyper_galaxy_images=hyper_galaxy_images,
                                                          hyper_minimum_values=hyper_minimum_values)

    elif not tracer.has_light_profile and tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return InversionFit.fast_evidence(lensing_image=lensing_image, tracer=tracer)
        elif tracer.has_hyper_galaxy:
            return HyperInversionFit.fast_scaled_evidence(lensing_image=lensing_image, tracer=tracer,
                                                          hyper_model_image=hyper_model_image,
                                                          hyper_galaxy_images=hyper_galaxy_images,
                                                          hyper_minimum_values=hyper_minimum_values)

    elif tracer.has_light_profile and tracer.has_pixelization:

        if not tracer.has_hyper_galaxy:
            return ProfileInversionFit.fast_evidence(lensing_image=lensing_image, tracer=tracer)
        elif tracer.has_hyper_galaxy:
            return HyperProfileInversionFit.fast_scaled_evidence(lensing_image=lensing_image, tracer=tracer,
                                                                 hyper_model_image=hyper_model_image,
                                                                 hyper_galaxy_images=hyper_galaxy_images,
                                                                 hyper_minimum_values=hyper_minimum_values)

    else:

        raise exc.FittingException('The fast likelihood routine did not call a likelihood functions - check the '
                                   'properties of the tracer')


class AbstractFit(object):

    def __init__(self, lensing_image, tracer, _model_image):

        self.lensing_image = lensing_image
        self.tracer = tracer

        self.scaled_array_from_array_1d = lensing_image.grids.image.scaled_array_from_array_1d
        self.image = lensing_image.image
        self._image = lensing_image[:]
        self._noise_map = lensing_image.noise_map

        self._model_image = _model_image
        self._residuals = residuals_from_image_and_model(self._image, self._model_image)
        self._chi_squareds = chi_squareds_from_residuals_and_noise(self._residuals, lensing_image.noise_map)

    @property
    def chi_squared_term(self):
        return chi_squared_term_from_chi_squareds(self._chi_squareds)

    @property
    def reduced_chi_squared(self):
        return self.chi_squared_term / self.lensing_image.mask.pixels_in_mask

    @property
    def noise_term(self):
        return noise_term_from_noise_map(self._noise_map)

    @property
    def likelihood(self):
        return likelihood_from_chi_squared_and_noise_terms(self.chi_squared_term, self.noise_term)

    @property
    def noise_map(self):
        return self.scaled_array_from_array_1d(self._noise_map)

    @property
    def model_image(self):
        return self.scaled_array_from_array_1d(self._model_image)

    @property
    def residuals(self):
        return self.scaled_array_from_array_1d(self._residuals)

    @property
    def chi_squareds(self):
        return self.scaled_array_from_array_1d(self._chi_squareds)

    @property
    def total_inversions(self):
        return len(self.tracer.mappers_of_planes)


class AbstractProfileFit(AbstractFit):

    def __init__(self, lensing_image, tracer, padded_tracer, plane_shape):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        self.padded_tracer = padded_tracer

        self.convolve_image = lensing_image.convolver_image.convolve_image
        _model_image = self.convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)

        super(AbstractProfileFit, self).__init__(lensing_image, tracer, _model_image)

    @property
    def model_images_of_planes(self):

        _model_images_of_planes = list(map(lambda plane:
                                  self.convolve_image(plane._image_plane_image, plane._image_plane_blurring_image),
                                  self.tracer.all_planes))

        return list(map(lambda image : None if not image.any() else self.scaled_array_from_array_1d(image),
                         _model_images_of_planes))

    @property
    def unmasked_model_profile_image(self):
        return unmasked_model_image_from_lensing_image_and_tracer(self.lensing_image, self.padded_tracer)

    @property
    def unmasked_model_profile_images_of_galaxies(self):
        return unmasked_model_images_of_galaxies_from_lensing_image_and_tracer(self.lensing_image, self.padded_tracer)


class AbstractInversion(object):

    @property
    def likelihood_with_regularization(self):
        return likelihood_with_regularization_from_chi_squared_regularization_and_noise_terms(self.chi_squared_term,
                                                 self.inversion.regularization_term, self.noise_term)

    @property
    def evidence(self):
        return evidence_from_reconstruction_terms(self.chi_squared_term, self.inversion.regularization_term,
                                                  self.inversion.log_det_curvature_reg_matrix_term,
                                                  self.inversion.log_det_regularization_matrix_term,
                                                  self.noise_term)


class AbstractInversionFit(AbstractFit, AbstractInversion):

    def __init__(self, lensing_image, tracer):
        self.mapper = tracer.mappers_of_planes[0]
        self.regularization = tracer.regularizations_of_planes[0]
        self.inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(lensing_image,
                                                                                           lensing_image.noise_map,
                                                                                           lensing_image.convolver_mapping_matrix,
                                                                                           self.mapper, self.regularization)

        super(AbstractInversionFit, self).__init__(lensing_image, tracer, self.inversion.reconstructed_data_vector)

    @property
    def model_images_of_planes(self):
        return [None, self.scaled_array_from_array_1d(self._model_image)]


class AbstractProfileInversionFit(AbstractFit, AbstractInversion):

    def __init__(self, lensing_image, tracer, padded_tracer):
        self.convolve_image = lensing_image.convolver_image.convolve_image
        self._profile_model_image = self.convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)
        self._profile_subtracted_image = lensing_image[:] - self._profile_model_image

        self.mapper = tracer.mappers_of_planes[0]
        self.regularization = tracer.regularizations_of_planes[0]
        self.inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(self._profile_subtracted_image,
                                                                                           lensing_image.noise_map,
                                                                                           lensing_image.convolver_mapping_matrix,
                                                                                           self.mapper, self.regularization)

        self._inversion_model_image = self.inversion.reconstructed_data_vector

        _model_image = self._profile_model_image + self._inversion_model_image

        super(AbstractProfileInversionFit, self).__init__(lensing_image, tracer, _model_image)

    @property
    def profile_subtracted_image(self):
        return self.scaled_array_from_array_1d(self._profile_subtracted_image)

    @property
    def profile_model_image(self):
        return self.scaled_array_from_array_1d(self._profile_model_image)

    @property
    def inversion_model_image(self):
        return self.scaled_array_from_array_1d(self._inversion_model_image)

    @property
    def model_images_of_planes(self):
        return [self.profile_model_image, self.inversion_model_image]


class ProfileFit(AbstractProfileFit):

    def __init__(self, lensing_image, tracer, padded_tracer=None, plane_shape=(30, 30)):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """
        super(ProfileFit, self).__init__(lensing_image, tracer, padded_tracer, plane_shape)

    @classmethod
    def fast_likelihood(cls, lensing_image, tracer):
        convolve_image = lensing_image.convolver_image.convolve_image
        _model_image = convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)
        _residuals = residuals_from_image_and_model(lensing_image[:], _model_image)
        _chi_squareds = chi_squareds_from_residuals_and_noise(_residuals, lensing_image.noise_map)
        chi_squared_term = chi_squared_term_from_chi_squareds(_chi_squareds)
        noise_term = noise_term_from_noise_map(lensing_image.image.noise_map)
        return likelihood_from_chi_squared_and_noise_terms(chi_squared_term, noise_term)


class InversionFit(AbstractInversionFit):

    def __init__(self, lensing_image, tracer):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        super(InversionFit, self).__init__(lensing_image, tracer)

    @classmethod
    def fast_evidence(cls, lensing_image, tracer):
        mapper = tracer.mappers_of_planes[0]
        regularization = tracer.regularizations_of_planes[0]
        inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(lensing_image[:], lensing_image.noise_map,
                                                                                      lensing_image.convolver_mapping_matrix,
                                                                                      mapper, regularization)
        _model_image = inversion.reconstructed_data_vector
        _residuals = residuals_from_image_and_model(lensing_image[:], _model_image)
        _chi_squareds = chi_squareds_from_residuals_and_noise(_residuals, lensing_image.noise_map)
        chi_squared_term = chi_squared_term_from_chi_squareds(_chi_squareds)
        noise_term = noise_term_from_noise_map(lensing_image.noise_map)
        return evidence_from_reconstruction_terms(chi_squared_term, inversion.regularization_term,
                                                  inversion.log_det_curvature_reg_matrix_term,
                                                  inversion.log_det_regularization_matrix_term, noise_term)


class ProfileInversionFit(AbstractProfileInversionFit):

    def __init__(self, lensing_image, tracer, padded_tracer=None):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        super(ProfileInversionFit, self).__init__(lensing_image, tracer, padded_tracer)

    @classmethod
    def fast_evidence(cls, lensing_image, tracer):
        convolve_image = lensing_image.convolver_image.convolve_image
        _profile_model_image = convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)
        _profile_subtracted_image = lensing_image[:] - _profile_model_image
        mapper = tracer.mappers_of_planes[0]
        regularization = tracer.regularizations_of_planes[0]
        inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(_profile_subtracted_image,
                                                                                      lensing_image.noise_map,
                                                                                      lensing_image.convolver_mapping_matrix,
                                                                                      mapper, regularization)
        _model_image = _profile_model_image + inversion.reconstructed_data_vector
        _residuals = residuals_from_image_and_model(lensing_image[:], _model_image)
        _chi_squareds = chi_squareds_from_residuals_and_noise(_residuals, lensing_image.noise_map)
        chi_squared_term = chi_squared_term_from_chi_squareds(_chi_squareds)
        noise_term = noise_term_from_noise_map(lensing_image.noise_map)
        return evidence_from_reconstruction_terms(chi_squared_term, inversion.regularization_term,
                                                  inversion.log_det_curvature_reg_matrix_term,
                                                  inversion.log_det_regularization_matrix_term, noise_term)


class AbstractHyper(AbstractFit):

    def contributions_and_scaled_noise_map_from_hyper_images(self, tracer, hyper_model_image, hyper_galaxy_images,
                                                             hyper_minimum_values):
        self.is_hyper_fit = True

        self._contributions = contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images,
                                                                           tracer.hyper_galaxies, hyper_minimum_values)

        self._scaled_noise_map = scaled_noise_from_hyper_galaxies_and_contributions(self._contributions,
                                                                                    tracer.hyper_galaxies,
                                                                                    self._noise_map)

    @property
    def scaled_chi_squared_term(self):
        return chi_squared_term_from_chi_squareds(self._scaled_chi_squareds)

    @property
    def scaled_noise_term(self):
        return noise_term_from_noise_map(self._scaled_noise_map)

    @property
    def scaled_noise_map(self):
        return self.scaled_array_from_array_1d(self._scaled_noise_map)

    @property
    def scaled_chi_squareds(self):
        return self.scaled_array_from_array_1d(self._scaled_chi_squareds)

    @property
    def contributions(self):
        return list(map(lambda contributions: self.scaled_array_from_array_1d(contributions), self._contributions))


class AbstractHyperInversion(AbstractHyper):

    @property
    def scaled_model_image(self):
        return self.scaled_array_from_array_1d(self._scaled_model_image)

    @property
    def scaled_residuals(self):
        return self.scaled_array_from_array_1d(self._scaled_residuals)

    @property
    def scaled_evidence(self):
        return evidence_from_reconstruction_terms(self.scaled_chi_squared_term,
                                                  self.scaled_inversion.regularization_term,
                                                  self.scaled_inversion.log_det_curvature_reg_matrix_term,
                                                  self.scaled_inversion.log_det_regularization_matrix_term,
                                                  self.scaled_noise_term)


class HyperProfileFit(AbstractProfileFit, AbstractHyper):

    def __init__(self, lensing_image, tracer, hyper_model_image, hyper_galaxy_images, hyper_minimum_values,
                 padded_tracer=None, plane_shape=(30, 30)):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        super(HyperProfileFit, self).__init__(lensing_image, tracer, padded_tracer, plane_shape)
        self.contributions_and_scaled_noise_map_from_hyper_images(tracer, hyper_model_image,
                                                                  hyper_galaxy_images, hyper_minimum_values)

        self._scaled_chi_squareds = chi_squareds_from_residuals_and_noise(self._residuals, self._scaled_noise_map)

    @classmethod
    def fast_scaled_likelihood(cls, lensing_image, tracer, hyper_model_image, hyper_galaxy_images,
                               hyper_minimum_values):
        _contributions = contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images,
                                                                      tracer.hyper_galaxies, hyper_minimum_values)
        _scaled_noise_map = scaled_noise_from_hyper_galaxies_and_contributions(_contributions, tracer.hyper_galaxies,
                                                                               lensing_image.noise_map)

        convolve_image = lensing_image.convolver_image.convolve_image
        _model_image = convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)
        _residuals = residuals_from_image_and_model(lensing_image[:], _model_image)
        _scaled_chi_squareds = chi_squareds_from_residuals_and_noise(_residuals, _scaled_noise_map)

        scaled_chi_squared_term = chi_squared_term_from_chi_squareds(_scaled_chi_squareds)
        scaled_noise_term = noise_term_from_noise_map(_scaled_noise_map)
        return likelihood_from_chi_squared_and_noise_terms(scaled_chi_squared_term, scaled_noise_term)

    @property
    def scaled_likelihood(self):
        return likelihood_from_chi_squared_and_noise_terms(self.scaled_chi_squared_term, self.scaled_noise_term)


class HyperInversionFit(AbstractInversionFit, AbstractHyperInversion):

    def __init__(self, lensing_image, tracer, hyper_model_image, hyper_galaxy_images, hyper_minimum_values):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        super(HyperInversionFit, self).__init__(lensing_image, tracer)

        self.contributions_and_scaled_noise_map_from_hyper_images(tracer, hyper_model_image,
                                                                  hyper_galaxy_images, hyper_minimum_values)

        self.scaled_inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(
            lensing_image[:], self._scaled_noise_map, lensing_image.convolver_mapping_matrix, self.mapper,
            self.regularization)

        self._scaled_model_image = self.scaled_inversion.reconstructed_data_vector
        self._scaled_residuals = residuals_from_image_and_model(self._image, self._scaled_model_image)
        self._scaled_chi_squareds = chi_squareds_from_residuals_and_noise(self._scaled_residuals,
                                                                          self._scaled_noise_map)

    @classmethod
    def fast_scaled_evidence(cls, lensing_image, tracer, hyper_model_image, hyper_galaxy_images,
                             hyper_minimum_values):
        _contributions = contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images,
                                                                      tracer.hyper_galaxies, hyper_minimum_values)
        _scaled_noise_map = scaled_noise_from_hyper_galaxies_and_contributions(_contributions, tracer.hyper_galaxies,
                                                                               lensing_image.noise_map)

        mapper = tracer.mappers_of_planes[0]
        regularization = tracer.regularizations_of_planes[0]

        scaled_inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(
            lensing_image[:], _scaled_noise_map, lensing_image.convolver_mapping_matrix, mapper, regularization)

        _scaled_residuals = residuals_from_image_and_model(lensing_image[:], scaled_inversion.reconstructed_data_vector)
        _scaled_chi_squareds = chi_squareds_from_residuals_and_noise(_scaled_residuals, _scaled_noise_map)
        scaled_chi_squared_term = chi_squared_term_from_chi_squareds(_scaled_chi_squareds)
        scaled_noise_term = noise_term_from_noise_map(_scaled_noise_map)
        return evidence_from_reconstruction_terms(scaled_chi_squared_term, scaled_inversion.regularization_term,
                                                  scaled_inversion.log_det_curvature_reg_matrix_term,
                                                  scaled_inversion.log_det_regularization_matrix_term,
                                                  scaled_noise_term)


class HyperProfileInversionFit(AbstractProfileInversionFit, AbstractHyperInversion):

    def __init__(self, lensing_image, tracer, hyper_model_image, hyper_galaxy_images, hyper_minimum_values,
                 padded_tracer=None):
        """
        Class to evaluate the incorrect_fit between a model described by a tracer and an actual lensing_image.

        Parameters
        ----------
        lensing_image: li.LensingImage
            An lensing_image that has been masked for efficiency
        tracer: ray_tracing.AbstractTracer
            An object describing the model
        """

        super(HyperProfileInversionFit, self).__init__(lensing_image, tracer, padded_tracer)

        self.contributions_and_scaled_noise_map_from_hyper_images(tracer, hyper_model_image,
                                                                  hyper_galaxy_images, hyper_minimum_values)

        self.scaled_inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(
            self._profile_subtracted_image, self._scaled_noise_map, lensing_image.convolver_mapping_matrix,
            self.mapper, self.regularization)

        self._scaled_model_image = self._profile_model_image + self.scaled_inversion.reconstructed_data_vector
        self._scaled_residuals = residuals_from_image_and_model(self._image, self._scaled_model_image)
        self._scaled_chi_squareds = chi_squareds_from_residuals_and_noise(self._scaled_residuals,
                                                                          self._scaled_noise_map)

    @classmethod
    def fast_scaled_evidence(cls, lensing_image, tracer, hyper_model_image, hyper_galaxy_images,
                             hyper_minimum_values):
        _contributions = contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images,
                                                                      tracer.hyper_galaxies, hyper_minimum_values)
        _scaled_noise_map = scaled_noise_from_hyper_galaxies_and_contributions(_contributions, tracer.hyper_galaxies,
                                                                               lensing_image.noise_map)

        convolve_image = lensing_image.convolver_image.convolve_image
        _profile_model_image = convolve_image(tracer._image_plane_image, tracer._image_plane_blurring_image)
        _profile_subtracted_image = lensing_image[:] - _profile_model_image

        mapper = tracer.mappers_of_planes[0]
        regularization = tracer.regularizations_of_planes[0]

        scaled_inversion = inversions.inversion_from_lensing_image_mapper_and_regularization(
            _profile_subtracted_image, _scaled_noise_map, lensing_image.convolver_mapping_matrix, mapper,
            regularization)

        _scaled_model_image = _profile_model_image + scaled_inversion.reconstructed_data_vector
        _scaled_residuals = residuals_from_image_and_model(lensing_image[:], _scaled_model_image)
        _scaled_chi_squareds = chi_squareds_from_residuals_and_noise(_scaled_residuals, _scaled_noise_map)
        scaled_chi_squared_term = chi_squared_term_from_chi_squareds(_scaled_chi_squareds)
        scaled_noise_term = noise_term_from_noise_map(_scaled_noise_map)
        return evidence_from_reconstruction_terms(scaled_chi_squared_term, scaled_inversion.regularization_term,
                                                  scaled_inversion.log_det_curvature_reg_matrix_term,
                                                  scaled_inversion.log_det_regularization_matrix_term,
                                                  scaled_noise_term)


class PositionFit:

    def __init__(self, positions, noise):

        self.positions = positions
        self.noise = noise

    @property
    def chi_squareds(self):
        return np.square(np.divide(self.maximum_separations, self.noise))

    @property
    def likelihood(self):
        return -0.5 * sum(self.chi_squareds)

    def maximum_separation_within_threshold(self, threshold):
        if max(self.maximum_separations) > threshold:
            return False
        else:
            return True

    @property
    def maximum_separations(self):
        return list(map(lambda positions: self.max_separation_of_grid(positions), self.positions))

    def max_separation_of_grid(self, grid):
        rdist_max = np.zeros((grid.shape[0]))
        for i in range(grid.shape[0]):
            xdists = np.square(np.subtract(grid[i, 0], grid[:, 0]))
            ydists = np.square(np.subtract(grid[i, 1], grid[:, 1]))
            rdist_max[i] = np.max(np.add(xdists, ydists))
        return np.max(np.sqrt(rdist_max))


def blur_image_including_blurring_region(image, blurring_image, convolver):
    """For a given lensing_image and blurring region, convert them to 2D and blur with the PSF, then return as
    the 1D DataGrid.

    Parameters
    ----------
    image : ndarray
        The lensing_image data_vector using the GridData 1D representation.
    blurring_image : ndarray
        The blurring region data_vector, using the GridData 1D representation.
    convolver : auto_lens.inversion.frame_convolution.KernelConvolver
        The 2D Point Spread Function (PSF).
    """
    return convolver.convolve_image(image, blurring_image)


def residuals_from_image_and_model(image, model):
    """Compute the residuals between an observed charge injection lensing_image and post-cti model lensing_image.

    Residuals = (Data - Model).

    Parameters
    -----------
    image : ChInj.CIImage
        The observed charge injection lensing_image data.
    model : np.ndarray
        The model lensing_image.
    """
    return np.subtract(image, model)


def chi_squareds_from_residuals_and_noise(residuals, noise):
    """Computes a chi-squared lensing_image, by calculating the squared residuals between an observed charge injection \
    images and post-cti hyper_model_image lensing_image and dividing by the variance (noises**2.0) in each pixel.

    Chi_Sq = ((Residuals) / (Noise)) ** 2.0 = ((Data - Model)**2.0)/(Variances)

    This gives the residuals, which are divided by the variance of each pixel and squared to give their chi sq.

    Parameters
    -----------
    residuals
    noise : np.ndarray
        The noises in the lensing_image.
    """
    return np.square((np.divide(residuals, noise)))


def chi_squared_term_from_chi_squareds(chi_squareds):
    """Compute the chi-squared of a model lensing_image's incorrect_fit to the data_vector, by taking the difference between the
    observed lensing_image and model ray-tracing lensing_image, dividing by the noise_map in each pixel and squaring:

    [Chi_Squared] = sum(([Data - Model] / [Noise]) ** 2.0)

    Parameters
    ----------
    chi_squareds
    """
    return np.sum(chi_squareds)


def noise_term_from_noise_map(noise_map):
    """Compute the noise_map normalization term of an lensing_image, which is computed by summing the noise_map in every pixel:

    [Noise_Term] = sum(log(2*pi*[Noise]**2.0))

    Parameters
    ----------
    noise_map : grids.GridData
        The noise_map in each pixel.
    """
    return np.sum(np.log(2 * np.pi * noise_map ** 2.0))


def likelihood_from_chi_squared_and_noise_terms(chi_squared_term, noise_term):
    """Compute the likelihood of a model lensing_image's incorrect_fit to the data_vector, by taking the difference between the
    observed lensing_image and model ray-tracing lensing_image. The likelihood consists of two terms:

    Chi-squared term - The residuals (model - data_vector) of every pixel divided by the noise_map in each pixel, all
    squared.
    [Chi_Squared_Term] = sum(([Residuals] / [Noise]) ** 2.0)

    The overall normalization of the noise_map is also included, by summing the log noise_map value in each pixel:
    [Noise_Term] = sum(log(2*pi*[Noise]**2.0))

    These are summed and multiplied by -0.5 to give the likelihood:

    Likelihood = -0.5*[Chi_Squared_Term + Noise_Term]

    Parameters
    ----------
    """
    return -0.5 * (chi_squared_term + noise_term)


def contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images, hyper_galaxies,
                                                 minimum_values):
    """Use the model lensing_image and galaxy lensing_image (computed in the previous phase of the pipeline) to determine the
    contributions of each hyper galaxy.

    Parameters
    -----------
    minimum_values
    hyper_model_image : ndarray
        The best-incorrect_fit model lensing_image to the data_vector, from a previous phase of the pipeline
    hyper_galaxy_images : [ndarray]
        The best-incorrect_fit model lensing_image of each hyper-galaxy, which can tell us how much flux each pixel contributes to.
    hyper_galaxies : [galaxy.HyperGalaxy]
        Each hyper-galaxy which is used to determine its contributions.
    """
    # noinspection PyArgumentList
    return list(map(lambda hyper, galaxy_image, minimum_value:
                    hyper.contributions_from_hyper_images(hyper_model_image, galaxy_image, minimum_value),
                    hyper_galaxies, hyper_galaxy_images, minimum_values))


def scaled_noise_from_hyper_galaxies_and_contributions(contributions, hyper_galaxies, noise):
    """Use the contributions of each hyper galaxy to compute the scaled noise_map.
    Parameters
    -----------
    noise
    hyper_galaxies
    contributions : [ndarray]
        The contribution of flux of each galaxy in each pixel (computed from galaxy.HyperGalaxy)
    """
    scaled_noises = list(map(lambda hyper, contribution: hyper.scaled_noise_from_contributions(noise, contribution),
                             hyper_galaxies, contributions))
    return noise + sum(scaled_noises)


def likelihood_with_regularization_from_chi_squared_regularization_and_noise_terms(chi_squared_term,
                                                                                   regularization_term, noise_term):
    return -0.5 * (chi_squared_term + regularization_term + noise_term)


def evidence_from_reconstruction_terms(chi_squared_term, regularization_term, log_covariance_regularization_term,
                                       log_regularization_term, noise_term):
    return -0.5 * (chi_squared_term + regularization_term + log_covariance_regularization_term -
                   log_regularization_term + noise_term)


def unmasked_model_image_from_lensing_image_and_tracer(lensing_image, tracer):
    if tracer is None:
        return None
    elif tracer is not None:
        model_image_1d = lensing_image.padded_grids.image.convolve_array_1d_with_psf(tracer._image_plane_image,
                                                                                       lensing_image.psf)
        return lensing_image.padded_grids.image.scaled_array_from_array_1d(model_image_1d)


# TODO : The [plane_index][galaxy_index] data structure is going to be key to tracking galaxies / hyper galaxies in
# TODO : Multi-plane ray tracing. I never felt it was easy to follow using list comprehensions from ray_tracing.
# TODO : Can we make this neater?


def unmasked_model_images_of_galaxies_from_lensing_image_and_tracer(lensing_image, tracer):

    if tracer is None:
        return None
    elif tracer is not None:

        padded_model_images_of_galaxies = [[] for _ in range(len(tracer.all_planes))]

        for plane_index, plane in enumerate(tracer.all_planes):
            for galaxy_index in range(len(plane.galaxies)):
                _galaxy_image_plane_image = plane._image_plane_image_of_galaxies[galaxy_index]
                _blurred_galaxy_image_plane_image = \
                    lensing_image.padded_grids.image.convolve_array_1d_with_psf(_galaxy_image_plane_image,
                                                                                lensing_image.psf)
                galaxy_model_image = \
                    lensing_image.padded_grids.image.scaled_array_from_array_1d(_blurred_galaxy_image_plane_image)

                padded_model_images_of_galaxies[plane_index].append(galaxy_model_image)

        return padded_model_images_of_galaxies