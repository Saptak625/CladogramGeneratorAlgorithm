from ete3 import Tree

#Getting Input(Input Medium Soon to Change)
with open('input.txt', 'r+') as f:
  dcLabels=f.readline().replace('\n', '').split(',')
  speciesLabels=f.readline().replace('\n', '').split(',')
  dimensions=(len(speciesLabels), len(dcLabels)) #Columns by rows
  inputTable=[list(i) for i in f.read().split('\n')]

#Input Preprocessing
#L Processing with R and T substitution
preprocessedInput = [[False for j in range(dimensions[1])] for i in range(dimensions[0])]
for i1, l in enumerate(inputTable):
  for i2, char in enumerate(l):
    if inputTable[i1][i2] == 'L':
      newDCName = 'Loss of ' + dcLabels[i2]
      if newDCName in dcLabels:
        ind = dcLabels.index(newDCName)
        preprocessedInput[i1][i2]=True
      else:
        dcLabels.append(newDCName)
        for ci, pl in enumerate(preprocessedInput):
          pl.append(ci == i1)
      preprocessedInput[i1][i2]=True
    else:
      preprocessedInput[i1][i2] = (inputTable[i1][i2] != ' ')
dimensions=(len(speciesLabels), len(dcLabels)) #Columns by rows

#Calculating sums of each row
speciesSums = sorted([(speciesLabels[ind], i.count(True)) for ind, i in enumerate(preprocessedInput)], key = lambda x: x[1])
dcSums = sorted([(dcLabels[i], [preprocessedInput[j][i] for j in range(dimensions[0])].count(True)) for i in range(dimensions[1])], key = lambda x: x[1], reverse=True)
dcDict = {i[0]: i[1] for i in dcSums}

#Species and DC Profiles
speciesToProfiles = {label: ' '.join([str(j) for j, b in enumerate(preprocessedInput[i]) if b]) for i, label in enumerate(speciesLabels)}
profilesToSpecies = {}
for species in speciesToProfiles:
  profile = speciesToProfiles[species]
  if profile in profilesToSpecies:
    profilesToSpecies[profile].append(species)
  else:
    profilesToSpecies[profile] = [species]
dcToProfiles = {label: ' '.join([str(j) for j in range(dimensions[0]) if preprocessedInput[j][i]]) for i, label in enumerate(dcLabels)}
profilesToDC = {}
for dc in dcToProfiles:
  profile = dcToProfiles[dc]
  if profile in profilesToDC:
    profilesToDC[profile].append(dc)
  else:
    profilesToDC[profile] = [dc]

class EvoBranch:
  def __init__(self, species=None, derivedCharacteristic=[], dcRemaining = [i[0] for i in dcSums], parent = None):
    self.branches = []
    self.species = species
    self.derivedCharacteristic = []
    self.currentDerivedCharacteristic = []
    self.dcProfileRequirement = None
    self.dcRemaining = dcRemaining
    if parent:
      self.currentDerivedCharacteristic = parent.currentDerivedCharacteristic[:]
      self.dcRemaining = parent.dcRemaining[:]
    if derivedCharacteristic:
      self.addDerivedCharacteristics(derivedCharacteristic)

  def addDerivedCharacteristics(self, derivedCharacteristic):
    self.derivedCharacteristic = derivedCharacteristic
    self.dcProfileRequirement = dcToProfiles[derivedCharacteristic[0]]
    self.currentDerivedCharacteristic += derivedCharacteristic

  def addBranch(self, b):
    self.branches.append(b)

  def __str__(self):
    return f'Branch(id={self.__repr__()}, species: {self.species}, derivedCharacteristic: {self.derivedCharacteristic}, currentDerivedCharacteristic: {self.currentDerivedCharacteristic}, branches: {self.branches})'

  def toNewickString(self):
    if self.species:
      return self.species
    return '(' + ','.join([b.toNewickString() for b in self.branches]) + ')'

def isSubset(subset, biggerList):
  for i in subset:
    if i not in biggerList:
      return False
  return True

print('----------------------ALGO START----------------------')
#Tree Generation(Merge Sort with Backtracing)
rootBranch = EvoBranch()
currentBranch = rootBranch
speciesRemaining = [i[0] for i in speciesSums]
allNodes = []
currentSpecies = speciesRemaining[0]
while True:
  if currentBranch.species: #Backtrace
    print(f'Backtracing from {currentBranch.species} to {currentSpecies}')
    #Perform Backtracing
    longestSubset = None
    for n in allNodes:
      if isSubset(' '.join([str(i) for i in sorted([dcLabels.index(i) for i in n.currentDerivedCharacteristic])]), speciesToProfiles[currentSpecies]):
        if not longestSubset:
          longestSubset = n
        else:
          if len(longestSubset.currentDerivedCharacteristic) < len(n.currentDerivedCharacteristic):
            longestSubset = n
    if currentBranch not in allNodes:
      allNodes.append(currentBranch)
    print(f'Backtraced to {longestSubset}')
    currentBranch = longestSubset #Setting longestSubset to last common ancestor starting location
  else:
    if ' '.join([str(i) for i in sorted([dcLabels.index(i) for i in currentBranch.currentDerivedCharacteristic])]) == speciesToProfiles[currentSpecies]: #Profile of species matches with profile of current branch
      #Find other species using profileToSpecies and depending on dcSums of last characteristic, create new branch or add species to branch here
      allSpecies = profilesToSpecies[speciesToProfiles[currentSpecies]]
      print(f'Adding species {allSpecies}')
      for i, species in enumerate(allSpecies):
        if currentBranch.currentDerivedCharacteristic:
          if dcDict[currentBranch.currentDerivedCharacteristic[-1]] > 1: #Add new branches
            newBranch = EvoBranch(species = species, parent=currentBranch)
            if currentBranch not in allNodes:
              allNodes.append(currentBranch)
            currentBranch.addBranch(newBranch)
            if i < len(allSpecies) - 1:
              allNodes.append(currentBranch)
            else:
              currentBranch = newBranch
            print('Branching')
          else: #Update Species
            currentBranch.species = species
            print('No Branching')
        else:
          newBranch = EvoBranch(species = species, parent=currentBranch)
          if currentBranch not in allNodes:
            allNodes.append(currentBranch)
          currentBranch.addBranch(newBranch)
          if i < len(allSpecies) - 1:
            allNodes.append(newBranch)
          else:
            currentBranch = newBranch
          print('Branching')
        speciesRemaining.remove(species)
      if not speciesRemaining:
        if currentBranch not in allNodes:
          allNodes.append(currentBranch)
        break
      currentSpecies = speciesRemaining[0]
      speciesIndex = speciesLabels.index(currentSpecies) 
    else:
      #Add next derived characteristic and find other dc's using dcToProfile and depending on the profile of branch create new branch or add dc's to branch here
      newDC=currentBranch.dcRemaining[0]
      allDC=profilesToDC[dcToProfiles[newDC]]
      if str(dcLabels.index(allDC[0])) in speciesToProfiles[currentSpecies]:
        print(f'Adding DC {allDC}')
        if currentBranch.dcProfileRequirement: #If there is a requirement
          newBranch=EvoBranch(derivedCharacteristic=allDC, parent=currentBranch)
          if currentBranch not in allNodes:
            allNodes.append(currentBranch)
          currentBranch.addBranch(newBranch)
          currentBranch = newBranch
          print('Branching')
        else:
          if dcDict[allDC[0]] == dimensions[0]:
            currentBranch.addDerivedCharacteristics(allDC)
            print('No Branching')
          else:
            newBranch=EvoBranch(derivedCharacteristic=allDC, parent=currentBranch)
            if currentBranch not in allNodes:
              allNodes.append(currentBranch)
            currentBranch.addBranch(newBranch)
            currentBranch = newBranch
            print('Branching')
      else:
        print('Pruning Characteristic for Species Branch')
      for dc in allDC:
        currentBranch.dcRemaining.remove(dc)
  print()

print('Success!!!\n')

#Writing to File
branchesInLayer = [rootBranch]
with open('output.txt', 'w+') as f:
  i = 0
  while branchesInLayer:
    newBranches = []
    f.write(f'i={i}\n')
    for b in branchesInLayer:
      f.write(str(b)+'\n\n')
      newBranches += b.branches
    f.write('\n\n')
    branchesInLayer = newBranches
    i+=1

print(rootBranch.toNewickString()+';')
t = Tree(rootBranch.toNewickString()+';')
t.render("mytree.png")