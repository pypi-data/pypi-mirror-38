import numpy as np
import pytest

from autolens.fitting import fitting
from autolens.imaging import scaled_array as sca
from autolens.imaging import mask as msk
from autolens.galaxy import galaxy_data
from autolens.galaxy import galaxy as g
from autolens.galaxy import galaxy_fitting
from autolens.profiles import light_profiles as lp
from autolens.profiles import light_profiles as mp
from test.mock.mock_galaxy import MockGalaxy


@pytest.fixture(name="mock_galaxy", scope='function')
def make_mock_galaxy():
    return [g.Galaxy(light=MockLightProfile(value=1.0), mass=MockMassProfile(value=1.0))]

@pytest.fixture(name="galaxy_data", scope='function')
def make_galaxy_data():
    array = sca.ScaledSquarePixelArray(array=np.ones(1), pixel_scale=1.0)
    mask = msk.Mask(array=np.array([[True, True, True],
                                    [True, False, True],
                                    [True, True, True]]), pixel_scale=1.0)
    return galaxy_data.GalaxyData(data=array, mask=mask)


class TestGalaxyFit:

    class TestLikelihood:

        def test__1x1_image__light_profile_fits_data_perfectly__lh_is_noise_term(self):

            array = sca.ScaledSquarePixelArray(array=np.ones((3, 3)), pixel_scale=1.0)

            noise_map = sca.ScaledSquarePixelArray(array=np.ones((3, 3)), pixel_scale=1.0)

            mask = msk.Mask(array=np.array([[True, True, True],
                                           [True, False, True],
                                           [True, True, True]]), pixel_scale=1.0)

            data = galaxy_data.GalaxyData(array=array, noise_map=noise_map, mask=mask, sub_grid_size=1)

            g0 = MockGalaxy(value=1.0)

            fit = galaxy_fitting.GalaxyFit(galaxy_data=data, galaxy=g0)

            print(fit._data)
            print(fit._model_data)
            print(fit.data)
            print(fit.chi_squared_term)
            print(fit.noise_term)

            assert fit.likelihood == -0.5 * np.log(2 * np.pi * 1.0)