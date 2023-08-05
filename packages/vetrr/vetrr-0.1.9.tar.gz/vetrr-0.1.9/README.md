# vetrr
vet the redshifts for the CGM^2 galaxy catalogue (PI J. Werk)

# Requirements


* python
* numpy
* scipy
* matplotlib
* astropy
* h5py
* future
* PyYAML
* linetools

# How to run vetrr

### Example:
vetrr_vet_rr J1059_1441_m08_rr.fits test_vetted_rr.json --coadd_file=J1059+1441-08_coadd.yaml

vetrr_vet_rr is a script that will start the gui. It takes 3 arguments:
* output from RedRock (fits file with rr in it)
* vetted redshifts json folder. Lets use the convention JXXXX+XXXX_vetrr_your initials.json
* coadd_file: JXXXXXXX-<mask_number>_coadd.yaml created by the redux software


# Commands to use in the GUI:

# vet red rock using the gui
vetrr_vet_rr J0914_2823_m01_rr.fits J0914_2823_m01_vetrr_MW.json --coadd_file=J0914+2823-01_coadd.yaml


#### list of in GUI commands:
* & Toggle through ZQ
* '#' Toggle through RedRock Guesses
* % Set z=0 (for stars)
* 9 Skip to next spectrum with ZQ=-99
* x Next spectrum
* S = smooth
* Y = decrease
* W = unzoom
* pressing 'b' = bottom where cursor
* pressing "_" goes to Halpha
* pressing "*" goes to [OII] doublet
* pressing "(" goes to CaII absorption
* pressing ")" goes to [OIII] 5007 lines
* press "[" and "]" to pan left or right

#### Redshift quality of fit ZQ
* 4=awesome
* 3=single line but confident in the redshift
* 2= Not an option
* 1= I've identified a spectral feature but am not confident in the redshift
* 0 = ok spectrum but nothing to key on
* -1 = junk
* -99 = un-vetted
