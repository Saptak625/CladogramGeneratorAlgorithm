# CladogramGeneratorAlgorithm V1.0
Cladogram Generation is based on a custom-built Merge Sort with Common Ancestor Backtracing and Derived Characteristics Pruning Algorithm created in Python. Demo Link can be found here(https://replit.com/join/prkmzusdhq-24sdas). The idea of this algorithm started from the Nova Evolution Lab(https://www.pbs.org/wgbh/nova/labs/lab/evolution/)

## Documentation
### Basic Usage
Input data in a 4-input type table(see Input section for details). This data is preprocessed and solved by the algorithm to make a EvoBrach Tree, which can be visualized in many ways(see Output section for details).

### Definitions
* Species - A Specific Organism in the Cladogram
* Derived Characteristic(DC) - A characteristic that is passed through a cladogram
* Profile - A string of numbers seperated by spaces that represent the indexes of a series of labels(D.C's or species)
* Subset - A set is a subset of a larger set only if the larger set contains all elements of the smaller set
* EvoBranch - Custom Phylogentic Tree Branch structure inspired by the Nova Evolution Lab(https://www.pbs.org/wgbh/nova/labs/lab/evolution/)

## Merge Sort with Common Ancestor Backtracing and Derived Characteristics Pruning Algorithm
This algorithm was custom-built and developed by me. The algorithm was developed with generalization in mind. However, if any exception cases are found, please report them as an issue here. Here is a description of the following steps and logic of the algorithm:

### EvoBranch Class Structure
The EvoBranch Class Structure was designed with the following properties in mind:
* self.branches - The branches that this branch connects to(children branches) 
* self.species - The species on this branches end(leaf node)
* self.derivedCharacteristic - The derived characteristics on this immediate branch
* self.currentDerivedCharacteristic - The derived characteristics up to and including this branch
* self.dcProfileRequirement - DC Profile Requirement to decide whether to stay or branch DC
* self.dcRemaining - The DC's remaining on a specific branches path to the top of the cladogram(including pruning)
* parent - The parent branch from which branch descends from. Used for determining dcRemaining and currentDerivedCharacteristic

### Input
This generator takes input in a form of a Species vs Derived Characteristics Table. This table takes 4 types of inputs to create the according cladogram, which are:
* Empty(''): Indicates that the given species does not have the given characteristic EVER
* True('T'): Indicates that the given species has the given characteristic CURRENTLY
* Replaced('R'): Indicates that the given species HAD the given characteristic, but was REPLACED by another characteristic. This other characteristic likely evolved from the given characteristic.
* Lost('L'): Indicates that the given species HAD the given characteristic, but was LOST through the cladogram. 
![Input Example](https://github.com/Saptak625/CladogramGeneratorAlgorithm/blob/main/images/CladogramGeneratorInput.png)

### Input Preprocessing
All 4-input types need to be reduced to boolean inputs only. This is done through the following logic.
* Empty(''): No Changes Needed.
* True('T'): No Changes Needed.
* Replaced('R'): Replace with 'T'
* Lost('L'): Create a new DC column labeled "Loss of" of the characteristic. Replace with 'T' in current column and new column.
![Processed Input Example](https://github.com/Saptak625/CladogramGeneratorAlgorithm/blob/main/images/CladogramGeneratorPreprocessedInput.png)

### Input Measures Processing
Measures needed for the Algorithm include:
* speciesSums: Sorted Sums of species rows in tuple form with species
* dcSums: Sorted Sums of DC columns in tuple form with characteristic
* dcDict: Dictionary of dcSums with characteristic as key and sum as value
* speciesToProfiles: Dictionary of species as key and string profile
* profilesToSpecies: Dictionary of string profile as key and list of species as value
* dcToProfiles: Dictionary of species as key and string profile
* profilesToDC: Dictionary of string profile as key and list of species as value

### Algorithm Processing
#### Merge Sort with Common Ancestor Backtracing and Derived Characteristics Pruning Algorithm
The basis of the algorithm is try to add species(if possible based on branch currentDerivedCharacteristic) and add derived characteristics(along with pruning) to enable this until you reach a species branch, where you backtrace and continue the process.
1. Create rootBranch(root of tree), currentBranch(tree traversal pointer), speciesRemaining(species(sorted by number of DC's) not yet added to tree), allNodes(history of all nodes that have been traversed), and currentSpecies(first species from speciesRemaining).
2. If currentBranch is a species branch, continue to step 3. Otherwise continue to step 4. 
3. Backtrace from this branch to largest existing branch subset of currentSpecies. Set currentBranch to this largest subset. Return to step 2.
4. If currentSpecies profile matches currentBranch profile, continue to step 5. Otherwise continue to step 6.
5. Find all species with the same profile as currentSpecies. If dc is not needed for the currentSpecies, then continue to step 9. Otherwise, continue following. If there are more than 1 occurences of the last currentBranch currentDerivedCharacteristic in data, then create a new branch, add species to the branch, add new branch to allNodes, and set currentBranch to new branch for all species. Else, add species to the currentBranch. Regardless of last choice, remove all species from speciesRemaing. Finally, check whether speciesRemaining is empty. If so, algorithm is finished and tree has been generated from root node! Else, return to step 2.
6. Find all DC's with the same profile as the new DC to add. If branch there is a dcProfileRequirement, continue to step 7.
7. Create a new branch, add dc's to the branch, add new branch to allNodes, and set currentBranch to new branch. 
8. This means this is the root node. If all species have the current dc, then add dc's to the current branch. Else, return to step 7.
9. If you came from step 5, all dc's with same profile will be removed. Else, this is simply removing after use already. Either way, just remove each of the dc's from the currentBranch. Then, return to step 2.

### Output
This generator creates an EvoBranch tree starting with the root branch. This tree can be manipulated to display as needed(currently only supports non-visual print logs). 
