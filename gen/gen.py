import numpy as np
import gen.dists as dists


class Generator:
    def __init__(self, n_DM, n_gas, M_halo, M_disk, R_NFW, c_NFW, R_gas, max_gas, Z_gas, G=6.67e-8):
        self.n_DM = n_DM
        self.n_gas = n_gas
        self.M_halo = M_halo
        self.M_disk = M_disk
        self.R_NFW = R_NFW
        self.c_NFW = c_NFW
        self.R_gas = R_gas
        self.max_gas = max_gas
        self.Z_gas = Z_gas
        self.G = G

        self._gen_dm()
        self._gen_gas()
        self._convert_coords()
        
        return

    
    def _gen_dm(self):
        self.nfw_gen = dists.NFW(self.R_NFW, self.c_NFW)
        
        self.dm_theta = 2*np.pi*np.random.rand(self.n_DM)
        self.dm_phi = np.arccos(2*np.random.rand(self.n_DM) - 1)
        self.dm_r = self.nfw_gen.gen(self.n_DM)
        self.dm_v_x, self.dm_v_y, self.dm_v_z = self._mod_v(self.dm_r)*self.nfw_gen.vel(self.dm_r)

        return self.dm_theta, self.dm_phi, self.dm_r, self.dm_v_x, self.dm_v_y, self.dm_v_z


    def _gen_gas(self):
        gen_gas_r = dists.GasR(self.R_gas, self.max_gas)
        gen_gas_z = dists.GasZ(self.Z_gas)
        
        self.gas_theta = 2*np.pi*np.random.rand(self.n_gas)
        self.gas_z = gen_gas_z.gen(self.n_gas)
        self.gas_r = gen_gas_r.gen(self.n_gas)
        self.gas_v_x, self.gas_v_y, self.gas_v_z = self._mod_v(self.gas_r)*gen_gas_r.vel(self.gas_theta)

        return self.gas_theta, self.gas_z, self.gas_r, self.gas_v_x, self.gas_v_y, self.gas_v_z

    
    def _m_in_r(self, r):
        prefactor = self.M_halo/(np.log(self.c_NFW + 1) - self.c_NFW/(self.c_NFW + 1))
        return prefactor*(np.log((self.R_NFW + r)/self.R_NFW) - r/(self.R_NFW + r))


    def _mod_v(self, r):
        return np.sqrt(self.G * self._m_in_r(r)/r)


    def _convert_coords(self):
        self.dm_x, self.dm_y, self.dm_z = dists.spherical_to_cartesian(self.dm_r, self.dm_theta, self.dm_phi)
        self.gas_x, self.gas_y, self.gas_z = dists.cylindrical_to_cartesian(self.gas_r, self.gas_theta, self.gas_z)

        return self.dm_x, self.dm_y, self.dm_z, self.gas_x, self.gas_y, self.gas_z
    


if __name__ == "__main__":
    # Generate some test distribution and display in 3d with mpl
    gen = Generator(int(100), int(100), 1e5, 1e4, 10, 40, 100, 10, 2)
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(gen.gas_x, gen.gas_y, gen.gas_z, gen.gas_v_x, gen.gas_v_y, gen.gas_v_z, length=10)
    ax.set_zlim(-400, 400)

    plt.show()
