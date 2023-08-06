import sys
import numpy as np
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pickle

sys.path.append("../pyBSE/")
import pybse
import dart_board
from dart_board import sf_history


# Values for Swift J0513.4-6547 from Coe et al. 2015, MNRAS, 447, 1630
kwargs = {"P_orb" : 27.405, "P_orb_err" : 0.5, "ecc_max" : 0.17, "m_f" : 9.9,
          "m_f_err" : 2.0, "ra" : 78.36775, "dec" : -65.7885278}
pub = dart_board.DartBoard("NSHMXB", evolve_binary=pybse.evolv_wrapper,
                           ln_prior_pos=sf_history.flat.prior_lmc, nwalkers=320,
                           kwargs=kwargs)


dart = 2.456, 2.0126, 6.0637, 0.6139, 214.710, 0.9193, 2.4561, 78.5648, -65.7610, 3.4504

pub.aim_darts(dart=dart)

start_time = time.time()
pub.throw_darts(nburn=2, nsteps=2000)
print("Simulation took",time.time()-start_time,"seconds.")




import corner


corner.corner(pub.sampler.flatchain)

# plt.show()
plt.savefig("test1.pdf")



from dart_board.plotting import plot_chains

plot_chains(pub.sampler.chain, tracers=5)
plt.savefig("test1_chains.pdf")



pickle.dump(pub.sampler.chain, open("test1_chains.obj", "wb"))
