import configparser
import sys
from gen import *
import h5py

config = configparser.RawConfigParser()
config.optionxform = str  # To preserve case

config.read(sys.argv[1])

# Make the gadget file
gfile = ""
gfname = config['ParameterFile']['ParameterFile']

for section in config.sections():
    for item in config[section]:
        if not section in ['Gas', 'Stars', 'ParameterFile']:
            gfile += "{} {}\n".format(item, config[section][item])

print("Writing Gadget Paramterfile... {}".format(gfname))
with open(gfname, 'w') as f:
    f.write(gfile)

# Generate initial conditions

# Set up variables

gas = config['Gas']
nfw = config['NFW']
star = config['Stars']

n_gas = int(float(gas['GasParticles']))
n_star = int(float(star['StarParticles']))

M_halo = float(nfw['HaloMass'])
M_gas = float(gas['GassMass'])
M_star = float(star['StarMass'])

R_nfw = float(nfw['NFWScaleRadius'])
R_gas = float(gas['GasScaleRadius'])
R_star = float(star['StarScaleRadius'])

Z_gas = float(gas['GasScaleHeight'])
Z_star = float(star['StarScaleHeight'])
c_nfw = float(nfw['NFWc'])
max_gas = float(gas['MaxGas'])
max_star = float(star['MaxStar'])

ic_filename = config['GadgetFiles']['InitCondFile'] + ".hdf5"
ul_cm = float(config['Units']['UnitLength_in_cm'])
um_g = float(config['Units']['UnitMass_in_g'])
uv_cms = float(config['Units']['UnitVelocity_in_cm_per_s'])

G = 6.674e-8 * (1/(ul_cm*(uv_cms**2)/um_g))

# Actually generate particles

print("Generating Particles...")
gen = Generator(0, n_gas, n_star, M_halo, M_gas, M_star, R_nfw, c_nfw, R_gas, max_gas, Z_gas, R_star, max_star, Z_star, G)
print("Writing IC File... {}".format(ic_filename))

op = h5py.File(ic_filename, 'w')

masses = [0]*6
if n_gas:
    masses[0] = M_gas/n_gas
if n_star:
    masses[4] = M_star/n_star

write_head(op, [n_gas, 0, 0, 0, n_star, 0], masses, z=1)

if n_gas:
    write_block(op, 0, np.array([gen.gas_x, gen.gas_y, gen.gas_z]).T, np.array([gen.gas_v_x, gen.gas_v_y, gen.gas_v_z]).T, np.arange(0, n_gas))
if n_star:
    write_block(op, 4, np.array([gen.star_x, gen.star_y, gen.star_z]).T, np.array([gen.star_v_x, gen.star_v_y, gen.star_v_z]).T, np.arange(0, n_star))
