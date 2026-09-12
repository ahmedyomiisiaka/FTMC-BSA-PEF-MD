# BSA Control MD Simulation Log

## System

- Protein: Bovine serum albumin (BSA)
- UniProt: P02769
- Structure: PDB 4F5S, Chain A
- Mature-chain length: 583 residues
- Canonical sequence identity after correction: 100%
- Force field: AMBER99SB-ILDN
- Water model: TIP3P
- Box: Dodecahedral
- Protein-to-box distance: 1.0 nm
- Initial protein charge: -16 e
- NaCl concentration: 0.15 M
- Na+ ions: 109
- Cl- ions: 93
- Final water molecules: 29,748
- Final net charge: 0

## Energy Minimization

- Integrator: steep
- Maximum steps: 50,000
- emtol: 1000 kJ mol^-1 nm^-1
- emstep: 0.01 nm
- Electrostatics: PME
- Periodic boundary conditions: xyz
- Converged after: 1,206 steps
- Potential energy: -1.5524191e+06 kJ/mol
- Maximum force: 9.9985583e+02 kJ mol^-1 nm^-1
- Force norm: 1.6501566e+01 kJ mol^-1 nm^-1
- Status: PASS

## NVT Equilibration

- Duration: 100 ps
- Time step: 2 fs
- Steps: 50,000
- Temperature target: 300 K
- Thermostat: V-rescale
- Coupling groups: Protein / non-Protein
- Position restraints: Yes
- Pressure coupling: No

### Result

- Average temperature: 299.827 K
- RMSD: 2.927 K
- Total drift: 1.210 K
- Performance: 1.143 ns/day
- Status: PASS

## NPT Equilibration

- Duration: 100 ps
- Time step: 2 fs
- Steps: 50,000
- Temperature target: 300 K
- Pressure target: 1 bar
- Thermostat: V-rescale
- Barostat: C-rescale
- Pressure coupling: isotropic
- tau_p: 5.0 ps
- Compressibility: 4.5e-5 bar^-1
- Position restraints: Yes
- refcoord_scaling: com

### Full 0–100 ps results

- Average temperature: 300.024 K
- Temperature RMSD: 1.013 K
- Temperature drift: -0.424 K
- Average pressure: -21.33 bar
- Pressure RMSD: 133.67 bar
- Pressure error estimate: 32 bar
- Average density: 1011.58 kg/m^3
- Density RMSD: 5.56 kg/m^3
- Density drift: 7.57 kg/m^3

### Final 50–100 ps results

- Average pressure: 3.60 bar
- Pressure error estimate: 6.1 bar
- Pressure RMSD: 99.96 bar
- Pressure drift: -10.86 bar
- Average density: 1012.71 kg/m^3
- Density error estimate: 0.43 kg/m^3
- Density RMSD: 1.41 kg/m^3
- Density drift: -1.28 kg/m^3

### Interpretation

The temperature remained close to 300 K throughout the NPT stage.

Pressure showed the large fluctuations expected for a finite
biomolecular MD system. During the final 50 ps, the mean pressure
approached the 1 bar target within the estimated uncertainty.

Density was substantially more stable during the final 50 ps than
over the full 100 ps interval.

The 100 ps NPT stage was therefore accepted as the initial
equilibrated starting point for preparation of the control
production simulation.

- Performance: 1.077 ns/day
- Status: PASS

## Current Project Status

Energy minimization, NVT equilibration, and NPT equilibration are
complete.

Production control MD has NOT yet been started.

Electric-field simulations have NOT yet been started.
