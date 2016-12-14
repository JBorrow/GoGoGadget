GoGoGadget
============

A Generator for Isolated Disk Galaxies in Gadget
------------------------------------------------

This script generates the initial conditions and parameterfile for a gadget run with an isolated galaxy. It is inteded for use with the fixed potential [InterStellarGadget](https://github.com/JBorrow/InterStellarGadget).

To set up a run, simply run the parser script followed by the .ini file, for example from the 'example' directory:
```
python3 ../parser.py test.ini
```
This will generate the initial conditions (sans dark matter halo, of course). These follow exponential radial profiles and sech^2 profiles for the gas and stars.

The custom (i.e. non base-gadget) paramters are:
```
[ParameterFile]

# Name and location of gadget file
ParameterFile: test.param


[NFW]

# Scale lengths and masses are given in simulation units
NFWc: 40
NFWScaleRadius: 20
HaloMass: 1e12


[Gas]

GasScaleRadius: 10
# Particles are generated out to radius GasScaleRadius*MaxGas
MaxGas: 30
GasScaleHeight: 1
GassMass: 1e10
GasParticles: 1e3
GasDispersion: 0


[Stars]

StarScaleRadius: 10
MaxStar: 30
StarScaleHeight: 2
StarMass: 5e10
StarParticles: 1e3
StarDispersion: 0
```
