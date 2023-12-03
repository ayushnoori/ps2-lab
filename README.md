# Investigating molecular blood-brain-barrier permeability

## Project Summary

The blood-brain-barrier (BBB) is a selective semipermeable membrane that separates circulating blood from the brain and extracellular fluid in the central nervous system. It is composed of capillary endothelial cells, pericytes, and astrocytic end-feet, which together restrict the passage of solutes from the bloodstream into the brain. The BBB is a major obstacle in the treatment of neurological disorders, as it prevents many drugs from reaching the brain.

Understanding the permeability of molecules to the BBB is therefore of great interest to facilitate the development of new neurotherapeutics. Previous work has attempted to predict BBB permeability (for example, see [ayushnoori/graph-bbb](https://github.com/ayushnoori/graph-bbb) on GitHub), but this work has been limited by lack of molecular diversity and interpretability.

Here, we use techniques learned during the Fall 2023 semester in PHYSCI 2 Lab at Harvard College to investigate the relationships between several molecular properties and BBB permeability. We leverage a new diverse molecular database of BBB permeability with chemical descriptors, recently published in Nature Scientific Data in 2021:

Meng, F., Xi, Y., Huang, J. & Ayers, P. W. [A curated diverse molecular database of blood-brain barrier permeability with chemical descriptors.](https://www.nature.com/articles/s41597-021-01069-5) *Sci Data* **8**, 289 (2021).

Please also see [theochem/B3DB](https://github.com/theochem/B3DB) and [Issue #174 of mims-harvard/TDC](https://github.com/mims-harvard/TDC/issues/174) on GitHub. 

After retrieving and pre-processing our data, we calculate several molecular features of 1058 compounds as well as numerical logBB values for each compound, where logBB is the logarithm of the brain-plasma concentration ratio:
$$\log{BB} = \log{\frac{C_{brain}}{C_{blood}}}$$

Then, we use curve fitting methods learned in Lab 4 and Lab 5 to fit various models to the data. We visualize our data and results and, based on visual inspection, generate hypotheses for relationships between molecular features and logBB. Finally, we use $\chi^2_{red}$-testing to select from multiple competing models of the data and compare the goodness-of-fit of each model.

## Installation

To install the code, please clone this repository with the following:

```bash
git clone git@github.com:ayushnoori/ps2-lab.git
cd ps2-lab
```

Create a virtual environment.

```
conda deactivate
pip install virtualenv
virtualenv lab_env
source lab_env/bin/activate
```

Install necessary packages specified in `requirements.txt`.

```bash
pip install -r requirements.txt
```

To save the specific versions of each package required, run the following:

```bash
pip freeze > requirements-frozen.txt
```

Activate the `lab_env` virtual environment with the following:

```
source setup.sh
```
If desired, a Jupyter server can be created with the following:

```
source setup_jupyter.sh
```
