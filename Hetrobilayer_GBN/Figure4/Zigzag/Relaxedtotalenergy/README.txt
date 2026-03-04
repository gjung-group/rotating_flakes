Energy Data Description

The files energy100AA.dat, energy100AB.dat, energy500.dat, contain rigid and relaxed 
the total energy calculations for flakes of different radii (100, 500).

Each data file has the following column structure:

1. Twist angle (theta)

2. Energy (initial) #Rigid energy

3. Energy (next-to-last)

4. Energy (final relaxed total)

6.Total energy per atom (eV/atom)

8.Total energy per atom (eV/atom)

Interaction Energy

An additional quantity, E_inter_total, is computed to measure the interaction
between the flake and the substrate. It is obtained using:

E_inter_total = E_total - E_substrate -  E_flake / (2 * E_flake)

where:

E_total is the final relaxed total energy of the combined system,

E_substrate is the energy of the isolated substrate,

E_flake is the energy of a single isolated flake.

E_inter_total describes how the interaction varies with twist angle for
different flake sizes.

