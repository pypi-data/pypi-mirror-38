#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Simulate Target
---------------
Generate a forward model of a telescope detector with sensitivity variation,
and simulate stellar targets with motion relative to the CCD.

'''

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.widgets import Button
import everest
from everest.mathutils import SavGol
from .scopemath import PSF, PLD
import random
from random import randint
from astropy.io import fits
from everest import Transit
import k2plr
from k2plr.config import KPLR_ROOT
from everest.config import KEPPRF_DIR
from everest.missions.k2 import CDPP
import os
from tqdm import tqdm
from scipy.ndimage import zoom


class Target(object):
    """A simulated stellar object with a forward model of a telescope detector's sensitivity variation"""

    def __init__(self, fpix, flux, ferr, target, t, mag=12., roll=1., neighbor_magdiff=1.,
                 ncadences=1000, apsize=7, transit=False, variable=False, neighbor=False,
                 ccd_args=[]):

        # initialize self variables
        self.transit = transit
        self.variable = variable
        self.neighbor = neighbor
        self.targets = 1
        self.apsize = apsize
        self.ncadences = ncadences
        self.neighbor_magdiff = neighbor_magdiff
        self.mag = mag
        self.ccd_args = ccd_args

        self.t = t
        self.fpix = fpix
        self.flux = flux
        self.ferr = ferr
        self.target = target

        # add transit and variability
        if transit:
            self.add_transit()
        if variable:
            self.add_variability()
        if neighbor:
            self.add_neighbor()

    @property
    def targetpixelfile(self):
        return self.fpix

    @property
    def lightcurve(self):
        return self.flux

    @property
    def time(self):
        return self.t

    @property
    def error(self):
        return self.ferr

    @property
    def target_flux(self):
        return self.target

    def detrend(self, fpix=[]):
        """
        Runs 2nd order PLD with a Gaussian Proccess on a given light curve.

        Parameters
        ----------
        `fpix` :
            Pixel-level light curve of dimemsions (apsize, apsize, ncadences). Automatically set to fpix
            generated in GenerateLightCurve() unless a different light curve is passed.
        """

        # check if fpix light curve was passed in
        if len(fpix) == 0:
            fpix = self.fpix

        # Set empty transit mask if no transit provided
        if not self.transit:
            self.trninds = np.array([])

        # define aperture
        self.aperture = self.create_aperture(fpix)

        # Run 2nd order PLD with a Gaussian Process
        self.flux, self.rawflux = PLD(fpix, self.ferr, self.trninds, self.t, self.aperture)

        self.detrended_cdpp = self.find_CDPP(self.flux)
        self.raw_cdpp = self.find_CDPP(self.rawflux)

        return self

    def add_transit(self, fpix=[], depth=.001, per=15, dur=.5, t0=5.):
        """
        Injects a transit into light curve.

        Parameters
        ----------
        `fpix` :
            Pixel-level light curve of dimemsions (apsize, apsize, ncadences). Automatically set to
            fpix generated in GenerateLightCurve() unless a different light curve is passed.
        `depth` :
            Drop in flux due to transit relative to mean flux value.
        `per` :
            Period of transit in days.
        `dur` :
            Duration of transit in days.
        't0' :
            Initial transit time in days.
        """

        # check if fpix light curve was passed in
        if len(fpix) == 0:
            fpix = self.fpix

        self.transit = True

        # Transit information
        self.depth = depth
        self.per = per # period (days)
        self.dur = dur # duration (days)
        self.t0 = t0 # initial transit time (days)

        # Create transit light curve
        if self.depth == 0:
            self.trn = np.ones((self.ncadences))
        else:
            self.trn = Transit(self.t, t0=self.t0, per=self.per, dur=self.dur, depth=self.depth)

        # Define transit mask
        self.trninds = np.where(self.trn>1.0)
        self.M=lambda x: np.delete(x, self.trninds, axis=0)

        # Add transit to light curve
        self.fpix_trn = np.zeros((self.ncadences, self.apsize, self.apsize))
        for i,c in enumerate(fpix):
            self.fpix_trn[i] = c * self.trn[i]

        # Create flux light curve
        self.flux_trn = np.sum(self.fpix_trn.reshape((self.ncadences), -1), axis=1)

        self.fpix = self.fpix_trn
        self.flux = self.flux_trn

        return self

    def add_variability(self, fpix=[], var_amp=0.0005, freq=0.25, custom_variability=[]):
        """
        Add a sinusoidal variability model to the given light curve.

        Parameters
        ----------
        `fpix` :
            Pixel-level light curve of dimemsions (apsize, apsize, ncadences). Automatically
            set to fpix generated in GenerateLightCurve() unless a different light curve is passed.
        `var_amp` :
            Amplitude of sin wave, which is multiplied by the light curve.
        `freq` :
            Frequency of sin wave in days.
        `custom_variability` :
            A custom 1-dimensional array of length ncadences can be passed into the AddVariability()
            function, which will be multiplied by the light curve.
        """

        # check if fpix light curve was passed in
        if len(fpix) == 0:
            fpix = self.fpix

        self.variable = True

        # Check for custom variability
        if len(custom_variability) != 0:
            V = custom_variability
        else:
            V = 1 + var_amp * np.sin(freq*self.t)

        # Add variability to light curve
        V_fpix = [f * V[i] for i,f in enumerate(fpix)]

        # Create flux light curve
        V_flux = np.sum(np.array(V_fpix).reshape((self.ncadences), -1), axis=1)

        self.fpix = V_fpix
        self.flux = V_flux

        return self

    def add_neighbor(self, fpix=[], magdiff=1., dist=1.7):
        """
        Add a neighbor star with given difference in magnitude and distance at a
        randomized location.

        Parameters
        ----------
        `fpix` :
            Pixel-level light curve of dimemsions (apsize, apsize, ncadences). Automatically
            set to fpix generated in GenerateLightCurve() unless a different light curve is passed.
        `magdiff` :
            Difference in stellar magnitude between target and neighbor. Positive magdiff
            corresponds to higher values for the neighbor star's magnitude.
        `dist` :
            Distance (in pixels) between cetroid position of target and neighbor. The (x, y)
            coordinates of the neighbor are chosen arbitrarily to result in the given distance.
        """

        if len(fpix) == 0:
            fpix = self.fpix

        # initialize arrays
        n_fpix = np.zeros((self.ncadences, self.apsize, self.apsize))
        neighbor = np.zeros((self.ncadences, self.apsize, self.apsize))
        n_ferr = np.zeros((self.ncadences, self.apsize, self.apsize))

        # set neighbor params
        x_offset = dist * np.random.randn()
        y_offset = np.sqrt(np.abs(dist**2 - x_offset**2)) * random.choice((-1, 1))
        nx0 = (self.apsize / 2.0) + x_offset
        ny0 = (self.apsize / 2.0) + y_offset
        sx = [0.5 + 0.05 * np.random.randn()]
        sy = [0.5 + 0.05 * np.random.randn()]
        rho = [0.05 + 0.02 * np.random.randn()]

        # calculate comparison factor for neighbor, based on provided difference in magnitude
        self.r = 10 ** (magdiff / 2.5)

        neighbor_args = np.concatenate([[self.A / self.r], np.array([nx0]),
                                       np.array([ny0]), sx, sy, rho])

        # create neighbor pixel-level light curve
        for c in tqdm(range(self.ncadences)):

            # iterate through cadences, calculate pixel flux values
            n_fpix[c], neighbor[c], n_ferr[c] = PSF(neighbor_args, self.ccd_args,
                                                    self.xpos[c], self.ypos[c])

        # add neighbor to light curve
        fpix += n_fpix
        self.n_fpix = n_fpix

        # calculate flux light curve
        flux = np.sum(np.array(fpix).reshape((self.ncadences), -1), axis=1)

        self.neighbor = True
        self.targets += 1

        self.fpix = fpix
        self.flux = flux

        return self

    def create_aperture(self, fpix=[]):
        """
        Create an aperture including all pixels containing target flux.

        Parameters
        ----------
        `fpix` :
            Pixel-level light curve of dimemsions (apsize, apsize, ncadences). Automatically set to
            fpix generated in GenerateLightCurve() unless a different light curve is passed.
        """

        # check if fpix light curve was passed in
        if len(fpix) == 0:
            fpix = self.fpix

        aperture = np.zeros((self.ncadences, self.apsize, self.apsize))

        # Identify pixels with target flux for each cadence
        for c,f in enumerate(self.target):
            for i in range(self.apsize):
                for j in range(self.apsize):
                    if f[i][j] < 100.:
                        aperture[c][i][j] = 0
                    else:
                        aperture[c][i][j] = 1

        # Identify pixels with target flux for each cadence
        if self.neighbor:
            for c,f in enumerate(self.n_fpix):
                for i in range(self.apsize):
                    for j in range(self.apsize):
                        if f[i][j] > (.5 * np.max(f)):
                            aperture[c][i][j] = 0

        # Create single aperture
        finalap = np.zeros((self.apsize, self.apsize))

        # Sum apertures to weight pixels
        for i in range(self.apsize):
            for ap in aperture:
                finalap[i] += ap[i]

        max_counts = np.max(finalap)

        # Normalize to 1
        self.weighted_aperture = finalap / max_counts

        # Set excluded pixels to NaN
        for i in range(self.apsize):
            for j in range(self.apsize):
                if finalap[i][j] == 0:
                    finalap[i][j] = np.nan
                else:
                    finalap[i][j] = 1.

        self.aperture = finalap

        return finalap

    def display_aperture(self):
        """Displays aperture overlaid over the first cadence target pixel file."""

        self.create_aperture()
        pl.imshow(self.fpix[0] * self.aperture, origin='lower',
                  cmap='viridis', interpolation='nearest')
        pl.show()

    def display_detector(self):
        """Returns matrix of dimensions (apsize, apsize) for CCD pixel sensitivity."""

        # read in ccd parameters
        cx, cy, apsize, background_level, inter, photnoise_conversion = self.ccd_args

        # Define detector dimensions
        xdim = np.linspace(0, self.apsize, 100)
        ydim = np.linspace(0, self.apsize, 100)

        # Pixel resolution
        res = int(1000 / self.apsize)

        pixel_sens = np.zeros((res,res))

        # Calculate sensitivity function with detector parameters for individual pixel
        for i in range(res):
            for j in range(res):
                pixel_sens[i][j] = np.sum([c * (i-res/2) ** m for m, c in enumerate(cx)], axis = 0) + \
                np.sum([c * (j-res/2) ** m for m, c in enumerate(cy)], axis = 0)

        # Tile to create detector
        intra = np.tile(pixel_sens, (self.apsize, self.apsize))
        self.detector = np.zeros((res*self.apsize,res*self.apsize))

        # Multiply by inter-pixel sensitivity variables
        for i in range(self.apsize):
            for j in range(self.apsize):
                self.detector[i*res:(i+1)*res][j*res:(j+1)*res] = intra[i*res:(i+1)*res][j*res:(j+1)*res] * inter[i][j]

        # Display detector
        pl.imshow(self.detector, origin='lower', cmap='gray')

    def find_CDPP(self, flux=[]):
        """
        Quick function to calculate and return Combined Differential Photometric Precision (CDPP) of a given light curve.
         If no light curve is passed, this funtion returns the CDPP of the light curve generated in GenerateLightCurve().

        Parameters
        ----------
        `flux` :
            1-dimensional flux light curve for which CDPP is calculated. If nothing is passed into FindCDPP(), it returns
            the CDPP of the light curve generated in GenerateLightCurve()

        Returns
        -------
        `cdpp` : float
            Combined Differential Photometric Precision (CDPP) of given `flux` light curve
        """

        # check if flux light curve was passed in
        if len(flux) == 0:
            flux = self.flux

        cdpp = CDPP(flux)

        return cdpp

    def plot(self):
        """Simple plotting function to view first cadence tpf, and both raw and de-trended flux light curves."""

        # initialize subplots with 1:3 width ratio
        fig, ax = pl.subplots(1, 2, figsize=(12,3), gridspec_kw = {'width_ratios':[1, 3]})

        # Get aperture contour
        aperture = self.create_aperture()

        def PadWithZeros(vector, pad_width, iaxis, kwargs):
            vector[:pad_width[0]] = 0
            vector[-pad_width[1]:] = 0
            return vector
        ny, nx = self.fpix[0].shape
        contour = np.zeros((ny, nx))
        contour[np.where(aperture==1)] = 1
        contour = np.lib.pad(contour, 1, PadWithZeros)
        highres = zoom(contour, 100, order=0, mode='nearest')
        extent = np.array([-1, nx, -1, ny])


        # display first cadence tpf
        ax[0].imshow(self.fpix[0], origin='lower', cmap='viridis', interpolation='nearest')
        ax[0].contour(highres, levels=[0.5], extent=extent, origin='lower', colors='r', linewidths=2)

        ax[0].set_title('First Cadence tpf')
        ax[0].set_xlabel('x (pixels)')
        ax[0].set_ylabel('y (pixels)')

        # plot raw and de-trend light curves
        self.detrend()

        # make sure CDPP is a number before printing it
        if np.isnan(self.find_CDPP(self.flux)):
            ax[1].plot(self.t, self.rawflux, 'r.', alpha=0.3, label='raw flux')
            ax[1].plot(self.t, self.flux, 'k.', label='de-trended')
        else:
            ax[1].plot(self.t, self.rawflux, 'r.', alpha=0.3, label='raw flux (CDPP = %.i)'
                       % self.find_CDPP(self.rawflux))
            ax[1].plot(self.t, self.flux, 'k.', label='de-trended (CDPP = %.i)'
                       % self.find_CDPP(self.flux))
        ax[1].set_xlim([self.t[0], self.t[-1]])
        ax[1].legend(loc=0)
        ax[1].set_xlabel('Time (days)')
        ax[1].set_ylabel('Flux (counts)')
        ax[1].set_title('Flux Light Curve')

        fig.tight_layout()
        pl.show()

def generate_target(mag=12., roll=1., background_level=0., ccd_args=[], neighbor_magdiff=1.,
                    photnoise_conversion=.000625, ncadences=1000, apsize=7, ID=205998445,
                    custom_ccd=False, transit=False, variable=False, neighbor=False, ftpf=None):
    """

    Parameters
    ----------
     `mag` :
         Magnitude of primary target PSF.
     `roll` :
         Coefficient on K2 motion vectors of target. roll=1 corresponds to current K2 motion.
     `background_level` :
         Constant background signal in each pixel. Defaults to 0.
     `ccd_args` :
         Autogenerated if nothing passed, otherwise takes the following arguments:
         `cx` : sensitivity variation coefficients in `x`
         `cy` : sensitivity variation coefficients in `y`
         `apsize` : see below
         `background_level` : see above
         `inter` : matrix (apsize x apsize) of stochastic inter-pixel sensitivity variation
         `photnoise_conversion`: see below
     `neighbor_magdiff` :
         Difference between magnitude of target and neighbor. Only accessed if neighbor initialized as
         `True` or if AddNeighbor() function is called.
     `photnoise_conversion` :
         Conversion factor for photon noise, defaults to 0.000625 for consistency with benchmark.
     `ncadences` :
         Number of cadences in simulated light curve.
     `apsize` :
         Dimension of aperture on each side.

     Returns
     -------
     `Target`: :class:`Target` object
        A simulated CCD observation
    """
    t = np.linspace(0, 90, ncadences) # simulation lasts 90 days, with n cadences
    aperture = np.ones((ncadences, apsize, apsize))

    # calculate PSF amplitude for given Kp Mag
    A = calculate_PSF_amplitude(mag)

    # read in K2 motion vectors for provided K2 target (EPIC ID #)
    if ftpf is None:

        # access target information
        client = k2plr.API()
        star = client.k2_star(ID)
        tpf = star.get_target_pixel_files(fetch = True)[0]
        ftpf = os.path.join(KPLR_ROOT, 'data', 'k2', 'target_pixel_files', '%d'
                            % ID, tpf._filename)

    with fits.open(ftpf) as f:

        # read motion vectors in x and y
        xpos = f[1].data['pos_corr1']
        ypos = f[1].data['pos_corr2']

    # throw out outliers
    for i in range(len(xpos)):
        if abs(xpos[i]) >= 50 or abs(ypos[i]) >= 50:
            xpos[i] = 0
            ypos[i] = 0
        if np.isnan(xpos[i]):
            xpos[i] = 0
        if np.isnan(ypos[i]):
            ypos[i] = 0

    # crop to desired length and multiply by roll coefficient
    xpos = xpos[0:ncadences] * roll
    ypos = ypos[0:ncadences] * roll

    # create self.inter-pixel sensitivity variation matrix
    # random normal distribution centered at 0.975
    inter = np.zeros((apsize, apsize))
    for i in range(apsize):
        for j in range(apsize):
            inter[i][j] = (0.975 + 0.001 * np.random.randn())

    # assign PSF model parameters to be passed into PixelFlux function
    if not custom_ccd:

        # cx,cy: intra-pixel variation polynomial coefficients in x,y
        cx = [1.0, 0.0, -0.05]
        cy = [1.0, 0.0, -0.05]

        # x0,y0: center of PSF, half of aperture size plus random deviation
        x0 = (apsize / 2.0) + 0.2 * np.random.randn()
        y0 = (apsize / 2.0) + 0.2 * np.random.randn()

        # sx,sy: standard deviation of Gaussian in x,y
        # rho: rotation angle between x and y dimensions of Gaussian
        sx = [0.5 + 0.05 * np.random.randn()]
        sy = [0.5 + 0.05 * np.random.randn()]
        rho = [0.05 + 0.02 * np.random.randn()]
        psf_args = np.concatenate([[A], np.array([x0]), np.array([y0]), sx, sy, rho])

    ccd_args = [cx, cy, apsize, background_level, inter, photnoise_conversion]
    ccd_args = ccd_args

    # initialize pixel flux light curve, target light curve, and isolated noise in each pixel
    fpix = np.zeros((ncadences, apsize, apsize))
    target = np.zeros((ncadences, apsize, apsize))
    ferr = np.zeros((ncadences, apsize, apsize))

    '''
    Here is where the light curves are created
    PSF function calculates flux in each pixel
    Iterate through cadences (c), and x and y dimensions on the detector (i,j)
    '''

    for c in tqdm(range(ncadences)):

        fpix[c], target[c], ferr[c] = PSF(psf_args, ccd_args, xpos[c], ypos[c])


    flux = np.sum(fpix.reshape((ncadences), -1), axis=1)

    return Target(fpix, flux, ferr, target, t, mag=mag, roll=roll, neighbor_magdiff=neighbor_magdiff,
                 ncadences=ncadences, apsize=apsize, transit=transit, variable=variable, neighbor=neighbor,
                 ccd_args=ccd_args)

def calculate_PSF_amplitude(mag):
    """
    Returns the amplitude of the PSF for a star of a given magnitude.

    Parameters
    ----------
    `mag`: float
        Input magnitude.

    Returns
    -------
    amp : float
        Corresponding PSF applitude.
    """

    # mag/flux relation constants
    a,b,c = 1.65e+07, 0.93, -7.35
    return a * np.exp(-b * (mag+c))
