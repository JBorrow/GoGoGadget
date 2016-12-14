import h5py
import numpy as np

def write_block(f, type, pos, vel, id, m=False, U=False, rho=False, hsml=False, pot=False, acc=False, dAdt=False, dt=False):
    type = f.create_group("PartType{}".format(type))
    n_particles = len(id)

    # Create datasets
    positions = type.create_dataset("Coordinates", (n_particles, 3), data=pos)
    velocities = type.create_dataset("Velocities", (n_particles, 3))
    ids = type.create_dataset("ParticleIDs", (n_particles,))

    if m: #.any()
        masses = type.create_dataset("Masses", (n_particles, ))
    if U: #.any()
        internal_energies = type.create_dataset("InternalEnergy", (n_particles, ))
    if rho: #.any()
        density = type.create_dataset("Density", (n_particles, ))
    if hsml: #.any()
        smoothing_length = type.create_dataset("SmoothingLength", (n_particles, ))
    if pot: #.any()
        potential = type.create_dataset("Potential", (n_particles, ))
    if acc: #.any()
        accelerations = type.create_dataset("Acceleration", (n_particles, 3))
    if dAdt: #.any()
        rate_of_change_of_entropy = type.create_dataset("RateOfChangeOfEntropy", (n_particles, ))
    if dt: #.any()
        timestep = type.create_dataset("TimeStep", (n_particles, ))

    # Now fill

    velocities[...] =  vel
    ids[...] = id

    if m: #.any()
        masses[...] = m
    if U: #.any()
        internal_energies[...] = U
    if rho: #.any()
        density[...] = rho
    if hsml: #.any()
        smoothing_length[...] = hsml
    if pot: #.any()
        potential[...] = pot
    if acc: #.any()
        accelerations[...] = acc
    if dAdt: #.any()
        rate_of_change_of_entropy[...] = dAdt
    if dt: #.any()
        timestep[...] = dt

    return f


def write_head(f, npart, massarr, time, z=False, flagsfr=False, flagfeedback=False, nall=False, flagcooling=False, numfiles=1, omega0=0.3, omegalambda=0.7, hubbleparam=0.7, flagage=False, flagmetals=False, nallhw=0, flagentrics=False):
    header = f.create_group('Header')

    header.attrs['NumPart_ThisFile'] = npart
    header.attrs['MassTable'] = massarr
    header.attrs['Time'] = time
    header.attrs['NumFilesPerSnapshot'] = numfiles
    header.attrs['Omega0'] = omega0
    header.attrs['OmegaLambda'] = omegalambda
    header.attrs['HubbleParam'] = hubbleparam
    header.attrs['NumPart_Total_HW'] = nallhw

    if z: #.any()
        header.attrs['Redshift'] = z
    if flagsfr: #.any()
        header.attrs['Flag_Sfr'] = flagsfr
    if flagfeedback: #.any()
        header.attrs['Flag_Feedback'] = flagfeedback
    if nall: #.any()
        header.attrs['NumPart_Total'] = nall
    else:
        header.attrs['NumPart_Total'] = npart
    if flagcooling: #.any()
        header.attrs['Flag_Cooling'] = flagcooling
    if flagage: #.any()
        header.attrs['Flag_StellarAge'] = flagage
    if flagmetals: #.any()
        header.attrs['Flag_Metals'] = flagmetals
    if flagentrics: #.any()
        header.attrs['Flag_Entropy_ICs'] = flagentrics

    return f


if __name__ == "__main__":
    # Run a test
    n_particles = 100000
    pos = 100+100*np.random.rand(n_particles, 3)
    vel = np.random.rand(n_particles, 3)
    ids = np.arange(n_particles)
    
    f = h5py.File("TestICs.hdf5", "w")

    write_head(f, [0, n_particles, 0, 0, 0, 0], [0, 1e5, 0, 0, 0, 0], 0, z=1)
    write_block(f, 1, pos, vel, ids)

    f.close()
