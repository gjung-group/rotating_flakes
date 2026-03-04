
Data Description

The files energy100.dat, energy300.dat, energy500.dat, and energy1000.dat contain
the total energy calculations for flakes of different radii (100, 300, 500, and 1000).

Each data file has the following column structure:

Twist angle (theta)

Rigid total energy 


Interaction Energy
In this work, the total energy is computed for the Armchair, Zigzag, and circular geometries.
For each case, the quantity E_inter_energy***.dat is obtained using the relation:

E_inter_energy, is computed to measure the interaction between the flake and the substrate. It is obtained using:

E_inter_total = (E_total - E_flake - E_substrate) / (2 * E_flake)

where:

E_total is the final rigid/relaxed total energy of the combined system,

E_substrate is the energy of the isolated substrate,

E_flake is the energy of a single isolated flake.

E_inter_total describes how the interaction varies with twist angle for
different flake sizes.
