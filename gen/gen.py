import numpy as np
import gen.dists as dists


class Generator:
    def __init__(self, n_DM, n_gas, n_star, M_halo, M_gas, M_star, R_NFW, c_NFW, R_gas, max_gas, Z_gas, R_star, max_star, Z_star, G=6.67e-8):
        self.n_DM = n_DM
        self.n_gas = n_gas
        self.n_star = n_star
        self.M_halo = M_halo
        self.M_gas = M_gas
        self.M_star = M_star
        self.R_NFW = R_NFW
        self.c_NFW = c_NFW
        self.R_gas = R_gas
        self.max_gas = max_gas
        self.Z_gas = Z_gas
        self.R_star = R_star
        self.max_star = max_star
        self.Z_star = Z_star
        self.G = G

        self._gen_dm()
        if n_gas:
            self._gen_gas()
        if n_star:
            self._gen_star()
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


    # This really should be a pass-through function for gen gas, etc. but oh well.
    def _gen_star(self):
        gen_star_r = dists.GasR(self.R_star, self.max_star)
        gen_star_z = dists.GasZ(self.Z_star)
        
        self.star_theta = 2*np.pi*np.random.rand(self.n_star)
        self.star_z = gen_star_z.gen(self.n_star)
        self.star_r = gen_star_r.gen(self.n_star)
        self.star_v_x, self.star_v_y, self.star_v_z = self._mod_v(self.star_r)*gen_star_r.vel(self.star_theta)

        return self.star_theta, self.star_z, self.star_r, self.star_v_x, self.star_v_y, self.star_v_z


    def _m_in_r_dm(self, r):
        prefactor = self.M_halo/(np.log(self.c_NFW + 1) - self.c_NFW/(self.c_NFW + 1))
        return prefactor*(np.log((self.R_NFW + r)/self.R_NFW) - r/(self.R_NFW + r))


    def _m_in_r_gas(self, r):
        div = r/self.R_gas
        return self.M_gas*(1 - (1 + div)*np.exp(-div))


    def _m_in_r_star(self, r):
        div = r/self.R_star
        return self.M_star*(1 - (1 + div)*np.exp(-div))


    def _m_in_r(self, r):
        # We need to consider all components separately
        return self._m_in_r_dm(r) + self._m_in_r_gas(r) + self._m_in_r_star(r)
        

    def _mod_v(self, r):
        return np.sqrt(self.G * self._m_in_r(r)/r)


    def _convert_coords(self):
        self.dm_x, self.dm_y, self.dm_z = dists.spherical_to_cartesian(self.dm_r, self.dm_theta, self.dm_phi)
        if n_gas:
            self.gas_x, self.gas_y, self.gas_z = dists.cylindrical_to_cartesian(self.gas_r, self.gas_theta, self.gas_z)
        if n_star:
            self.star_x, self.star_y, self.star_z = dists.cylindrical_to_cartesian(self.star_r, self.star_theta, self.star_z)

        return 


if __name__ == "__main__":
    # Generate some test distribution and display in 3d with mpl
    gen = Generator(int(100), int(100), int(100), 1e5, 1e4, 10, 40, 100, 10, 40, 100, 10, 2)
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(gen.gas_x, gen.gas_y, gen.gas_z, gen.gas_v_x, gen.gas_v_y, gen.gas_v_z, length=10)
    ax.quiver(gen.star_x, gen.star_y, gen.star_z, gen.star_v_x, gen.star_v_y, gen.star_v_z, length=10)
    ax.set_zlim(-400, 400)

    plt.show()
