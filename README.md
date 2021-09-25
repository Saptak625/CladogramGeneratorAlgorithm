# CladogramGeneratorAlgorithm V1.0
Cladogram Generation is based on a custom-built Merge Sort with Common Ancestor Backtracing and Derived Characteristics Pruning Algorithm created in Python. Demo Link can be found here(https://replit.com/join/prkmzusdhq-24sdas)

## Documentation
### Usage
Input data in a 4-input type table(see Input section for details). This data is preprocessed and solved by the algorithm to make a EvoBrach Tree, which can be visualized in many ways(see Output section for details).

### Definitions
* Species - A Specific Organism in the Cladogram
* Derived Characteristic(DC) - A characteristic that is passed throughout 
* Profile - A string of numbers seperated by spaces that represent the indexes of a series of labels(D

## Merge Sort with Common Ancestor Backtracing and Derived Characteristics Pruning Algorithm
This algorithm was custom-built and developed by me. The algorithm was developed with generalization in mind. However, if any exception cases are found, please report them as an issue here. Here is a description of the following steps and logic of the algorithm:

### Input
This generator takes input in a form of a Species vs Derived Characteristics Table. This table takes 4 types of inputs to create the according cladogram, which are:
* Empty(''): Indicates that the given species does not have the given characteristic EVER
* True('T'): Indicates that the given species has the given characteristic CURRENTLY
* Replaced('R'): Indicates that the given species HAD the given characteristic, but was REPLACED by another characteristic. This other characteristic likely evolved from the given characteristic.
* Lost('L'): Indicates that the given species HAD the given characteristic, but was LOST through the cladogram. 

### Input Preprocessing
All 4-input types need to be reduced to boolean inputs only. This is done through the following logic.
* Empty(''): No Changes Needed.
* True('T'): No Changes Needed.
* Replaced('R'): Replace with 'T'
* Lost('L'): Create a new DC column labeled "Loss of" of the characteristic. Replace with 'T' in current column and new column.

### Input Measures Processing
Measures needed for the Algorithm include:
* speciesSums: Sums of species rows
* dcSums: Sums of DC columns
* 

### Algorithm Processing

#### Merge Sort


### Output
This generator creates an EvoBranch tree starting with the root branch. This tree can be manipulated to display as needed(currently only supports non-visual print logs). 
