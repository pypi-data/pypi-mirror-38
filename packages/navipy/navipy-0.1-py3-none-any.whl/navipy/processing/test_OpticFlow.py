import unittest
import navipy.processing.mcode as mcode
import pandas as pd
import numpy as np


def Scale(data, oldmin, oldmax, mini, maxi, ran):
    """Scales all values in data into the range mini, maxi
    Input:
        - data: values to be scaled
        - mini: minimum of new range
        - maxi: maximum of new range
        - ran: range of new values (ran=maxi-mini)

    Output:
        - data: the scaled data"""
    data = (data-oldmin)/oldmax
    dmax = np.max(data)
    dmin = np.min(data)
    scaling = ran/(dmax-dmin)
    data = (data-dmin)*scaling
    data = data+mini
    return data


class TestCase(unittest.TestCase):
    def setUp(self):
        """sets up a distance array that is used in some tests,
           as well as the velocity and viewing direction frames
        """
        distance = np.array([[2.60009956,  2.60009956,  2.60009956],
                             [2.60009956,  2.60009956,  2.60009956],
                             [2.60009956,  2.60009956,  2.60009956]])

        self.scene = np.zeros((3, 3, 4, 1))
        self.scene[:, :, 0, 0] = np.array(distance).copy()
        self.scene[:, :, 1, 0] = np.array(distance).copy()
        self.scene[:, :, 2, 0] = np.array(distance).copy()
        self.scene[:, :, 3, 0] = np.array(distance).copy()
        self.convention = 'xyz'
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), ('location', 'dx'),
                  ('location', 'dy'), ('location', 'dz'),
                  (self.convention, 'alpha_0'), (self.convention, 'alpha_1'),
                  (self.convention, 'alpha_2'), (self.convention, 'dalpha_0'),
                  (self.convention, 'dalpha_1'), (self.convention, 'dalpha_2')]
        self.index = pd.MultiIndex.from_tuples(tuples,
                                               names=['position',
                                                      'orientation'])
        self.velocity = pd.Series(index=self.index)

        self.elevation = np.arange(-np.pi/2, 4*(np.pi/360)-np.pi/2,
                                   2*(np.pi/360))
        self.azimuth = np.arange(0, 4*(np.pi/360)+2*(np.pi/360), 2*(np.pi/360))

        self.viewing_directions = np.zeros((3, 2))
        self.viewing_directions[:, 0] = self.elevation
        self.viewing_directions[:, 1] = self.azimuth

    def test_wrong_convention(self):
        """ this test checks if an error is raised
        when none or a convention other than 'xyz'
        is used
        """
        velocity = pd.Series(index=['x', 'y', 'z',
                                    'alpha_0', 'alpha_1', 'alpha_2',
                                    'dx', 'dy', 'dz',
                                    'dalpha_0', 'dalpha_1', 'dalpha_2'])

        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-19.8, -20, 2.6, 1.57079633, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        velocity.x = x
        velocity.y = y
        velocity.z = z
        velocity.alpha_0 = yaw
        velocity.alpha_1 = pitch
        velocity.alpha_2 = roll
        velocity.dx = dx
        velocity.dy = dy
        velocity.dz = dz
        velocity.dalpha_0 = dyaw
        velocity.dalpha_1 = dpitch
        velocity.dalpha_2 = droll

        with self.assertRaises(Exception):
            rof, hof, vof = mcode.optic_flow(self.scene,
                                             self.viewing_directions,
                                             velocity)
        for convention in ['alsjf', '233', 9, -1]:
            tuples = [('location', 'x'), ('location', 'y'),
                      ('location', 'z'), ('location', 'dx'),
                      ('location', 'dy'), ('location', 'dz'),
                      (convention, 'alpha_0'),
                      (convention, 'alpha_1'),
                      (convention, 'alpha_2'),
                      (convention, 'dalpha_0'),
                      (convention, 'dalpha_1'),
                      (convention, 'dalpha_2')]
            index = pd.MultiIndex.from_tuples(tuples,
                                              names=['position',
                                                     'orientation'])
            velocity = pd.Series(index=index)
            velocity['location']['x'] = x
            velocity['location']['y'] = y
            velocity['location']['z'] = z
            velocity[convention]['alpha_0'] = yaw
            velocity[convention]['alpha_1'] = pitch
            velocity[convention]['alpha_2'] = roll
            velocity['location']['dx'] = dx
            velocity['location']['dy'] = dy
            velocity['location']['dz'] = dz
            velocity[convention]['dalpha_0'] = dyaw
            velocity[convention]['dalpha_1'] = dpitch
            velocity[convention]['dalpha_2'] = droll
            with self.assertRaises(ValueError):
                rof, hof, vof = mcode.optic_flow(self.scene,
                                                 self.viewing_directions,
                                                 velocity)

    def test_rotation_not_too_strong(self):
        """
        this test checks that a Value Error is throught,
        if the change in rotation is more than pi/2.
        Thoughs, if the velocity of yaw, pitch and roll is
        is smaller than pi/2
        """
        # dyaw is too big
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-19.8, -20, 2.6,
                               1.57079633 + np.pi/2 + 0.00001, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        with self.assertRaises(ValueError):
            rof, hof, vof = mcode.optic_flow(self.scene,
                                             self.viewing_directions,
                                             self.velocity)

        # dpitch is too big
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-19.8, -20, 2.6,
                               1.57079633, 0 + np.pi/2 + 0.0001, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        with self.assertRaises(ValueError):
            rof, hof, vof = mcode.optic_flow(self.scene,
                                             self.viewing_directions,
                                             self.velocity)

        # droll is too big
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-19.8, -20, 2.6, 1.57079633, 0,
                               0 + np.pi/2 + 0.0001]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        with self.assertRaises(ValueError):
            rof, hof, vof = mcode.optic_flow(self.scene,
                                             self.viewing_directions,
                                             self.velocity)

    def test_only_x(self):
        """
        this test checks for the correct response if for example
        the bee moves only in x-direction keeping the other
        parameters (y,z,yaw,pitch,roll) constant
        """
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-19.8, -20, 2.6, 1.57079633, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(self.scene,
                                         self.viewing_directions,
                                         self.velocity)

        testrof = [[2.88404299e-34, 8.22008280e-20, 1.64376617e-19],
                   [2.34252646e-05, 4.64310635e-05, 6.94159777e-05],
                   [9.36297157e-05, 1.38760866e-04, 1.83822856e-04]]
        testhof = [[0.07692013, 0.07690842, 0.07687327],
                   [0.0768967, 0.07686158, 0.07680307],
                   [0.07682644, 0.07676796, 0.07668619]]
        testvof = [[2.46536984e-10, 1.34244164e-03, 2.68447412e-03],
                   [1.34203275e-03, 2.68345936e-03, 4.02366094e-03],
                   [2.68120450e-03, 4.02043495e-03, 5.35762781e-03]]

        assert np.all(np.isclose(rof, testrof))
        assert np.all(np.isclose(hof, testhof))
        assert np.all(np.isclose(vof, testvof))

    def test_only_yaw_new_vs_old(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the yaw axis keeping the other
        parameters (x,y,z,pitch,roll) constant
        """
        # yaw only everything zero
        # only vertical should change, horizontal stays same
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.90079633, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0]-positions[0, 0]
        dy = positions[1, 1]-positions[0, 1]
        dz = positions[1, 2]-positions[0, 2]
        dyaw = positions[1, 3]-positions[0, 3]
        dpitch = positions[1, 4]-positions[0, 4]
        droll = positions[1, 5]-positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(self.scene, self.viewing_directions,
                                         self.velocity)

        testrof = [[-6.47644748e-26, -3.52655120e-19, -7.05202754e-19],
                   [-1.84591335e-11, -1.00513560e-04, -2.00996485e-04],
                   [-3.69126442e-11, -2.00996503e-04, -4.01931744e-04]]
        testhof = [[-0.33, -0.32994974, -0.32979897],
                   [-0.33, -0.32994974, -0.32979897],
                   [-0.33, -0.32994974, -0.32979897]]
        testvof = [[-1.05768414e-09, -5.75929518e-03, -1.15168350e-02],
                   [-1.05752305e-09, -5.75841801e-03, -1.15150809e-02],
                   [-1.05703983e-09, -5.75578677e-03, -1.15098192e-02]]

        assert np.all(np.isclose(rof, testrof))
        assert np.all(np.isclose(hof, testhof))
        assert np.all(np.isclose(vof, testvof))

    def test_only_yaw(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the yaw axis keeping the other
        parameters (x,y,z,pitch,roll) constant
        """
        # yaw only everything zero
        # only vertical should change, horizontal stays same
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.90079633, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0]-positions[0, 0]
        dy = positions[1, 1]-positions[0, 1]
        dz = positions[1, 2]-positions[0, 2]
        dyaw = positions[1, 3]-positions[0, 3]
        dpitch = positions[1, 4]-positions[0, 4]
        droll = positions[1, 5]-positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(self.scene, self.viewing_directions,
                                         self.velocity)

        testrof = [[-6.47644748e-26, -3.52655120e-19, -7.05202754e-19],
                   [-1.84591335e-11, -1.00513560e-04, -2.00996485e-04],
                   [-3.69126442e-11, -2.00996503e-04, -4.01931744e-04]]
        testhof = [[-0.33, -0.32994974, -0.32979897],
                   [-0.33, -0.32994974, -0.32979897],
                   [-0.33, -0.32994974, -0.32979897]]
        testvof = [[-1.05768414e-09, -5.75929518e-03, -1.15168350e-02],
                   [-1.05752305e-09, -5.75841801e-03, -1.15150809e-02],
                   [-1.05703983e-09, -5.75578677e-03, -1.15098192e-02]]

        assert np.all(np.isclose(rof, testrof))
        assert np.all(np.isclose(hof, testhof))
        assert np.all(np.isclose(vof, testvof))

    def test_only_yaw_big(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the yaw axis keeping the other
        parameters (x,y,z,pitch,roll) constant.
        here the azimuthal optic flow should be zero and the
        elevational optic flow should be proportional with a
        constant factor to the cos of the elevation
        """
        # generate scene aka distance channel
        scene = np.random.random((180, 360, 4, 1))

        elevation = np.arange(-np.pi/2, np.pi/2, 2*(np.pi/360))
        azimuth = np.arange(0, 2*np.pi, 2*(np.pi/360))

        viewing_directions = np.zeros((180, 2))
        viewing_directions[:, 0] = elevation
        viewing_directions[:, 1] = azimuth[0:180]

        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.90079633, 0, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0]-positions[0, 0]
        dy = positions[1, 1]-positions[0, 1]
        dz = positions[1, 2]-positions[0, 2]
        dyaw = positions[1, 3]-positions[0, 3]
        dpitch = positions[1, 4]-positions[0, 4]
        droll = positions[1, 5]-positions[0, 5]

        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), ('location', 'dx'),
                  ('location', 'dy'), ('location', 'dz'),
                  (self.convention, 'alpha_0'), (self.convention, 'alpha_1'),
                  (self.convention, 'alpha_2'), (self.convention, 'dalpha_0'),
                  (self.convention, 'dalpha_1'), (self.convention, 'dalpha_2')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position', 'orientation'])
        velocity = pd.Series(index=index)

        velocity['location']['x'] = x
        velocity['location']['y'] = y
        velocity['location']['z'] = z
        velocity['xyz']['alpha_0'] = yaw
        velocity['xyz']['alpha_1'] = pitch
        velocity['xyz']['alpha_2'] = roll
        velocity['location']['dx'] = dx
        velocity['location']['dy'] = dy
        velocity['location']['dz'] = dz
        velocity['xyz']['dalpha_0'] = dyaw
        velocity['xyz']['dalpha_1'] = dpitch
        velocity['xyz']['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(scene, viewing_directions,
                                         velocity)
        cosel = np.cos(elevation)
        has_zeros = len(np.where(cosel == 0)) > 0
        factor = np.array([0])
        if not has_zeros:
            factor = np.array(hof[:, 0]/cosel)

        assert np.all(factor == factor[0])

    def test_only_pitch(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the pitch axis keeping the other
        parameters (x,y,z,yaw,roll) constant
        """
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.57079633, 0.1, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll
        rof, hof, vof = mcode.optic_flow(self.scene, self.viewing_directions,
                                         self.velocity)

        testrof = [[0.1, 0.1, 0.1],
                   [0.09998477, 0.09998477, 0.09998477],
                   [0.09993908, 0.09993908, 0.09993908]]
        testhof = [[1.02726882e-18, 5.59367784e-12, 1.11856508e-11],
                   [1.02726882e-18, 5.59367784e-12, 1.11856508e-11],
                   [1.02726882e-18, 5.59367784e-12, 1.11856508e-11]]
        testvof = [[-3.20510352e-10, -3.20461536e-10, -3.20315105e-10],
                   [-1.74524096e-03, -1.74524096e-03, -1.74524096e-03],
                   [-3.48994999e-03, -3.48994999e-03, -3.48994999e-03]]

        assert np.all(np.isclose(rof, testrof))
        assert np.all(np.isclose(hof, testhof))
        assert np.all(np.isclose(vof, testvof))

    def test_only_pitch_big(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the pitch axis keeping the other
        parameters (x,y,z,yaw,roll) constant.
        here the azimuthal optic flow should be zero and the
        elevational optic flow should be proportional with a
        constant factor to the cos of the elevation
        """
        scene = np.random.random((180, 360, 4, 1))

        elevation = np.arange(-np.pi/2, np.pi/2, 2*(np.pi/360))

        azimuth = np.arange(0, 2*np.pi, 2*(np.pi/360))
        viewing_directions = np.zeros((180, 2))
        viewing_directions[:, 0] = elevation
        viewing_directions[:, 1] = azimuth[0:180]

        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.57079633, 0.1, 0]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(scene, viewing_directions,
                                         self.velocity)

        cosel = np.cos(elevation)
        has_zeros = len(np.where(cosel == 0)) > 0
        factor = np.array([0])
        if not has_zeros:
            factor = np.array(vof[0, :]/cosel)

        assert np.all(factor == factor[0])

    def test_only_roll_big(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the roll axis keeping the other
        parameters (x,y,z,yaw,pitch) constant
        here the azimuthal optic flow should be zero and the
        elevational optic flow should be proportional with a
        constant factor to the cos of the elevation
        """
        scene = np.random.random((180, 360, 4, 1))

        elevation = np.arange(-np.pi/2, np.pi/2, 2*(np.pi/360))

        azimuth = np.arange(0, 2*np.pi, 2*(np.pi/360))
        viewing_directions = np.zeros((180, 2))
        viewing_directions[:, 0] = elevation
        viewing_directions[:, 1] = azimuth[0:180]

        positions = np.array([[-20, -20, 2.6, 1.57079633, 0, 0],
                              [-20, -20, 2.6, 1.57079633, 0, 0.1]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll

        rof, hof, vof = mcode.optic_flow(scene, viewing_directions,
                                         self.velocity)
        cosel = np.cos(elevation)
        sinel = np.sin(elevation)
        has_zeros = cosel[np.where(cosel == 0)] = 1
        factor = np.array(hof[0, :]/cosel)
        factor[has_zeros] = factor[1]
        has_zerossin = sinel[np.where(sinel == 0)] = 1
        factorsin = np.array(vof[0, :]/sinel)
        factorsin[has_zerossin] = factorsin[0]

        for i in range(1, len(factor)):
            assert np.isclose(factor[1], factor[i])
            if i == 90:
                continue
            assert np.isclose(factorsin[0], factorsin[i])
            # print(i)
        # assert np.all(np.isclose(hof, testhof))
        # assert np.all(np.isclose(vof, testvof))

    def test_only_roll(self):
        """
        this test checks for the correct response if for example
        the bee rotates only around the pitch axis keeping the other
        parameters (x,y,z,yaw,roll) constant
        """
        positions = np.array([[-20, -20, 2.6, 1.57079633, 0.1, 0.1],
                              [-20, -20, 2.6, 1.57079633, 0.1, 0.2]])

        x = positions[0, 0]
        y = positions[0, 1]
        z = positions[0, 2]
        yaw = positions[0, 3]
        pitch = positions[0, 4]
        roll = positions[0, 5]

        dx = positions[1, 0] - positions[0, 0]
        dy = positions[1, 1] - positions[0, 1]
        dz = positions[1, 2] - positions[0, 2]
        dyaw = positions[1, 3] - positions[0, 3]
        dpitch = positions[1, 4] - positions[0, 4]
        droll = positions[1, 5] - positions[0, 5]

        self.velocity['location']['x'] = x
        self.velocity['location']['y'] = y
        self.velocity['location']['z'] = z
        self.velocity[self.convention]['alpha_0'] = yaw
        self.velocity[self.convention]['alpha_1'] = pitch
        self.velocity[self.convention]['alpha_2'] = roll
        self.velocity['location']['dx'] = dx
        self.velocity['location']['dy'] = dy
        self.velocity['location']['dz'] = dz
        self.velocity[self.convention]['dalpha_0'] = dyaw
        self.velocity[self.convention]['dalpha_1'] = dpitch
        self.velocity[self.convention]['dalpha_2'] = droll
        rof, hof, vof = mcode.optic_flow(self.scene, self.viewing_directions,
                                         self.velocity)
        testrof = [[0.01088051, 0.01088051, 0.01088051],
                   [0.0126067, 0.01260916, 0.01261109],
                   [0.01432905, 0.01433397, 0.01433784]]
        testhof = [[0.00894177, 0.00721257, 0.00548116],
                   [0.00894177, 0.00721257, 0.00548116],
                   [0.00894177, 0.00721257, 0.00548116]]
        testvof = [[0.09900333, 0.09914431, 0.09925508],
                   [0.09879836, 0.09893931, 0.09905007],
                   [0.09856329, 0.09870419, 0.09881489]]

        assert np.all(np.isclose(rof, testrof))
        assert np.all(np.isclose(hof, testhof))
        assert np.all(np.isclose(vof, testvof))
    """
    def test_findconv(self):
        ypr=[1.57079633,0.1,0.1]
        vec=[0,        -0.09900333,  0.00993347]
        tmpvec = vec


        M1 = rotation_matrix(-ypr[2], [1, 0, 0])[:3, :3]
        vec = np.transpose(np.dot(M1, np.transpose(vec)))
        roty = np.transpose(np.dot(M1, np.transpose([0, 1, 0])))
        M2 = rotation_matrix(-ypr[1], roty)[:3, :3]
        vec = np.transpose(np.dot(M2, np.transpose(vec)))
        rotz = np.transpose(np.dot(M1, np.transpose([0, 0, 1])))
        #rotz = np.transpose(np.dot(M2, np.transpose(rotz)))
        M4 = rotation_matrix(-ypr[1], [0, 1, 0])[:3, :3]
        rotatedax = np.transpose(np.dot(M4, np.transpose(rotz)))

        M3 = rotation_matrix(-ypr[0], rotatedax)
        scale, shear, angles, translate, perspective =
        decompose_matrix(M3,'xyz')
        print("angels", angles)
        vec = np.transpose(np.dot(M3[:3,:3], np.transpose(vec)))
        print("old vec", vec)
        oldvec=vec

        angles=[ypr[0], ypr[1],ypr[2], -ypr[0], -ypr[1], -ypr[2]]

        #for c in ['xyz','xyx','xzy','xzx','yzx','yzy','yxz','yxy',
        #          'zxy','zxz','zyx','zyz','zyx','xyx','yzx','xzx',
        #          'xzy','yzy','zxy','yxy','yxz','zxz','xyz','zyz']:
        for al in angles:
                for bl in angles:
                    for cl in angles:
                        M = compose_matrix(scale=None, shear=None,
                                           angles=[al, bl,cl],
                                           translate=None,
                                           perspective=None,
                                           axes='zyx')[:3,:3]
                        #M= np.transpose(M)
                        vec = np.dot(np.transpose(M), vec)
                        if (np.isclose(vec[0], oldvec[0]) or
                            np.isclose(vec[0], oldvec[1]) or
                            np.isclose(vec[0], oldvec[2]) or\
                            np.isclose(vec[0], -oldvec[0]) or
                            np.isclose(vec[0], -oldvec[1]) or
                            np.isclose(vec[0], -oldvec[2])) and\
                           (np.isclose(vec[1], oldvec[0]) or
                            np.isclose(vec[1], oldvec[1]) or
                            np.isclose(vec[1], oldvec[2]) or\
                            np.isclose(vec[1], -oldvec[0]) or
                            np.isclose(vec[1], -oldvec[1]) or
                            np.isclose(vec[1], -oldvec[2])) and\
                           (np.isclose(vec[2], oldvec[0]) or
                            np.isclose(vec[2], oldvec[1]) or
                            np.isclose(vec[2], oldvec[2]) or\
                            np.isclose(vec[2], -oldvec[0]) or
                            np.isclose(vec[2], -oldvec[1]) or
                            np.isclose(vec[2], -oldvec[2])):
                            print("found")
                            print("conve", al, bl, cl)
                            print("new vec", vec)
                        #scale, shear, angles, translate,
                        perspective =decompose_matrix(M3,c)
                        #print("angels", angles)
                        #print("old vec", oldvec)
                        print("new vec", vec)
                        vec=tmpvec
    """


if __name__ == '__main__':
    unittest.main()
