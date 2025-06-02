---
permalink: /hardware/topological/
title: "Topological Quantum Computing"
---

Topological quantum computing is a unique approach that protects quantum information using the **topology** of special quantum states. Unlike other systems that require complex error correction, topological systems are naturally resistant to noise and imperfections.

This is made possible by using exotic particles called **non-Abelian anyons**. When these particles are moved (or “braided”) around each other in specific ways, they perform quantum operations that are protected from small errors. Although still experimental, this method holds promise for building very stable quantum computers.

---

## Topological Qubit Platforms

### 1. Majorana Zero Modes in Nanowires

This is the most explored path for topological qubits today. In this system, **Majorana zero modes** are expected to appear at the ends of a semiconductor nanowire covered with a thin superconducting layer, under very cold conditions.

- **Main materials**: Indium arsenide (InAs) or indium antimonide (InSb) nanowires with aluminium (Al)
- **How the qubit works**: Uses the combined state (parity) of two or more Majorana modes
- **Quantum operations**: Done by moving (braiding) these Majorana modes
- **Who's working on it**: Microsoft, TU Delft, University of Copenhagen

![Majorana Nanowires](https://www.researchgate.net/profile/Anastasia-Shkop/publication/300947584/figure/fig2/AS:614401019813888@1523477066560/A-schematic-picture-of-Majorana-nanowire-with-controllable-coupling-to-the-leads-Tip-of.png)  
*Schematic of a nanowire device where Majorana zero modes can emerge at the ends under specific conditions.*  
Source: [ResearchGate](https://www.researchgate.net/figure/A-schematic-picture-of-Majorana-nanowire-with-controllable-coupling-to-the-leads-Tip-of_fig2_300947584)

---

### 2. Topological Insulator–Superconductor Systems

**Topological insulators** are materials that conduct electricity only on their surfaces. When these are placed in contact with a superconductor, they may also host Majorana modes. This setup is still mostly in the research phase.

- **Main materials**: Bismuth selenide (Bi₂Se₃), Bismuth telluride (Bi₂Te₃) with aluminium or niobium
- **Goal**: Create Majorana modes on the surface
- **Progress**: Early-stage experiments and theoretical proposals
- **Research groups**: Weizmann Institute, Princeton, MIT

![TI-SC Interface](https://www.nature.com/articles/s41467-019-10658-3/figures/1)  
*Illustration of a topological insulator (Bi₂Te₃) interfaced with a superconductor (FeTe), showing the emergence of superconductivity at the interface.*  
Source: [Nature Communications](https://www.nature.com/articles/s41467-019-10658-3)

---

### 3. Quantum Hall Edge States

In very strong magnetic fields and ultra-low temperatures, 2D electron systems can enter special phases where particles behave like **anyons**—including non-Abelian anyons. These systems are topologically ordered and could be used for quantum computation through braiding.

- **Conditions needed**: High magnetic fields and millikelvin temperatures
- **Current use**: Mostly for basic research and simulations
- **Research groups**: Microsoft StationQ, Harvard, UIUC

![Quantum Hall Edge States](https://topocondmat.org/w3_pump_QHE/QHEedgestates.html)  
*Diagram depicting chiral edge states in a quantum Hall system, illustrating the unidirectional flow of electrons along the edges.*  
Source: [Topology in Condensed Matter](https://topocondmat.org/w3_pump_QHE/QHEedgestates.html)

---

## Braiding and Topological Gates

Topological quantum gates are performed by **braiding** non-Abelian particles around one another. The result of a braid depends only on the path the particles take — not on the exact timing — which gives this system its natural protection from errors.

- **Single-qubit gates**: Done by exchanging (braiding) Majorana modes
- **Two-qubit gates**: Require measurements or helper systems
- **Challenge**: On their own, braiding can’t perform all types of quantum operations, so other techniques may be added

Source: [Braiding and quantum computation](https://topocondmat.org/w2_majorana/braiding.html)

---

## Companies and Research Groups Working on Topological Quantum Computing

- **[Microsoft StationQ](https://www.microsoft.com/en-us/research/group/stationq/)** – Leading the development of Majorana-based qubits and topological computing.

- **[TU Delft – QuTech](https://qutech.nl/research/quantum-computing/topological-qubits/)** – Research on nanowires and 2D materials for topological qubits.

- **[University of Copenhagen – Niels Bohr Institute](https://www.nbi.ku.dk/english/research/condensed-matter-physics/)** – Exploring new materials and nanostructures.

- **[Weizmann Institute of Science](https://www.weizmann.ac.il/condmat/heiblum/)** – Experiments in fractional quantum Hall systems and interferometry.

- **[Princeton University – Yazdani Lab](https://yazdanilab.princeton.edu/)** – Research using scanning tunneling microscopy to study Majorana modes.

- **[MIT – Quantum Nanostructures Group](https://qns.mit.edu/)** – Building and testing TI–superconductor devices.

---

## Further Reading

We recommend these resources to learn more:

- [A Collection of Resources for Learning Topological Quantum Computation](https://github.com/fatimahmadi/Blogposts/blob/master/TQC.md) by Fatimah Ahmadi  
  > A curated list of tutorials, papers, and explanations to help you get started.

- [Topological Quantum Computation](https://arxiv.org/abs/quant-ph/9707021) by Chetan Nayak et al.  
  > A theoretical overview of anyons, braiding, and how this approach works.

- [Majorana Fermions in Semiconductor Nanowires](https://arxiv.org/abs/1204.2792) by Roman Lutchyn et al.  
  > Explains how to create and detect Majorana modes in nanowire setups.

---

## See Also

- [Trapped Ion Quantum Computing](/hardware/ions/)
- [Silicon Spin Qubits](/hardware/silicon-spin/)

---

*This page is part of the hardware directory exploring physical implementations of quantum computers.*
