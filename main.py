import csvLite, os

recentScoresWP, recentScoresNP, recentScoresA = dict(), dict(), dict()
schoolsWP, schoolsNP, schoolsA = [], [], []

recentScores = dict()
schools = []


def openFile(fileName):
  with open(os.path.join(os.sys.path[0], fileName), 'r') as infile:
    d_Reader = csvLite.DictReader(infile)
    data = []
    for row in d_Reader:
      data.append(row)
    infile.close()
    return data, d_Reader.fieldnames

def cleanData(data):
  for entry in data:
    try:
      for key in entry:
        if key not in ['School','Location', 'Division']:
          split = entry[key].split(' ')
          entry[key] = split[0]
    except:
      print("Error Code: 2")
  return data


def dispSchool(selectedSchools, count, dataBase):
  if type(selectedSchools) == str:
    selectedSchools = [selectedSchools]
  selectedSchools = [dataBase[school] for school in selectedSchools]
  if count == False:
    for school in selectedSchools:
      print('----------------'*3)
      for key in school:
        if key == 'Total':
          print(f'{key}:\t\t\t  {school[key]}\n')
        elif key in ['School']:
          print(f'{key}:\t\t\t  {school[key]}')
        elif key in ['Overall Effect - Visual']:
          print(f'{key}:  {school[key]}')
        elif key in ['Ensemble Visual', 'Overall Effect - Music', 'High Overall Effect']:
          print(f'{key}:\t  {school[key]}')
        elif key in ['Rank']:
          pass
        else:
          print(f'{key}:\t\t  {school[key]}')
      print('----------------'*3,'\n')
  if count == True:
    for i in range(len(selectedSchools)):
      print('----------------'*3)
      print(f"Ranking:\t\t  {i+1}")
      for key in selectedSchools[i]:
        if key == 'Total':
          print(f'{key}:\t\t\t  {selectedSchools[i][key]}\n')
        elif key in ['School']:
          print(f'{key}:\t\t\t  {selectedSchools[i][key]}')
        elif key in ['Overall Effect - Visual']:
          print(f'{key}:  {selectedSchools[i][key]}')
        elif key in ['Ensemble Visual', 'Overall Effect - Music', 'High Overall Effect']:
          print(f'{key}:\t  {selectedSchools[i][key]}')
        elif key in ["Rank"]:
          pass
        else:
          print(f'{key}:\t\t  {selectedSchools[i][key]}')
      print('----------------'*3,'\n')


def getDivisionSchools(divisions, selectedSchools, dataBase):
  if type(divisions) == type([]):
    divisionSchools = []
    for division in divisions:
      for school in selectedSchools:
        if dataBase[school]['Division'] == division:
          divisionSchools.append(school)
    return divisionSchools
  else:
    divisionSchools = []
    for school in selectedSchools:
      if dataBase[school]['Division'] == divisions:
        divisionSchools.append(school)
    return divisionSchools


def rankSchools(schools, selection, dataBase):
  selectedSchools = [i for i in schools]
  ranking = dict()
  for school in selectedSchools:
      ranking[school] = dataBase[school][selection]
  for i in range(len(selectedSchools)):
      for i in range(len(selectedSchools)):
          if i != len(selectedSchools) - 1:
              if (
                  ranking[selectedSchools[i]] < ranking[selectedSchools[i + 1]]
                  or ranking[selectedSchools[i]] == ranking[selectedSchools[i + 1]]
              ):
                  selectedSchools[i], selectedSchools[i + 1] = (
                      selectedSchools[i + 1],
                      selectedSchools[i],
                  )
  ranked_schools = {}
  for i, school in enumerate(selectedSchools):
      ranked_schools[school] = {
          "Rank": i + 1,
          "Total": dataBase[school][selection],
      }
  return ranked_schools


def setup(fileName):
  data, headers = openFile(fileName)
  data  = cleanData(data)
  for entry in data:
    recentScores[entry['School']] = entry
  for school in recentScores:
    schools.append(school)
  schools.sort()
  divisions = set()
  for school in schools:
    divisions.add(recentScores[school]['Division'])
  return data, headers, schools, divisions


def manualSelection(headers, schools, divisions):
  print("Note: All Selections Are Case Sensitive.\n")
  
  selectionInput = False
  while selectionInput not in ['s', 'd']:
    selectionInput = input("Would You Like To Sort By School(s) Or Division(s)? ").lower()[0]
  print()
  
  if selectionInput == 'd':
    print("Divisions:\n", divisions,'\n')
    selectedDivisions = []
    divisionInput = False
    while divisionInput != '0':
      divisionInput = (input("Select A Divison(s). Type 0 To Continue. ")).rstrip()
      if divisionInput in divisions and divisionInput not in selectedDivisions:
        selectedDivisions.append(divisionInput)
        print("Division Added.")
      else:
        if divisionInput != '0':
          print("Division Not Added.")
    selectedSchools = getDivisionSchools(selectedDivisions, schools, recentScores)

  elif selectionInput == 's':
    print("Schools:\n", schools,'\n')
    selectedSchools = []
    schoolInput = False
    while schoolInput != '0':
      schoolInput = (input("Select A School(s). Type 0 To Continue. ")).rstrip()
      if schoolInput in schools and schoolInput not in selectedSchools:
        selectedSchools.append(schoolInput)
        print("School Added.")
      else:
        if schoolInput != '0':
          print("School Not Added.")
  print()
  
  selectionInput = False
  while selectionInput not in ['y', 'n']:
    selectionInput = input("Would You Like To Sort By A Category? (Yes Or No) ").lower()[0]
  print()
  
  if selectionInput == 'y':
    print("Categories:\n", headers,'\n')
    categoryInput = False
    while categoryInput not in headers:
      categoryInput = input("Select A Category To Sort By. ").strip()
    print()
    
    rankedSchools = rankSchools(selectedSchools, categoryInput, recentScores)
    dispSchool(rankedSchools, True, recentScores)
  
  if selectionInput == 'n':
    dispSchool(selectedSchools, False, recentScores)


def dataWithPercussion():
  data, headers, schools, divisions = setup('dataWP.csv')
  
  choice = False
  while choice not in ['1', '2']:
    choice = input("Type 1 For Schools Ranked By Percussion Or 2 For Manual Selection. ")

  if choice == '1':
    rankedSchoolsPercussion = rankSchools(schools, "Percussion", recentScores)
    dispSchool(rankedSchoolsPercussion, True, recentScores)
  if choice == '2':
    manualSelection(headers, schools, divisions)
    
def dataNoPercussion():
  data, headers, schools, divisions = setup('dataNP.csv')
    
  choice = False
  while choice not in ['1', '2']:
    choice = input("Type 1 For All Schools Ranked Or 2 For Manual Selection. ")
  
  if choice == '1':
    rankedSchoolsTotal = rankSchools(schools, "Total", recentScores)
    dispSchool(rankedSchoolsTotal, True, recentScores)
  if choice == '2':
    manualSelection(headers, schools, divisions)

def dataAuxiliary():
  data, headers, schools, divisions = setup('dataA.csv')
  
  choice = False
  while choice not in ['1', '2']:
    choice = input("Type 1 For All Schools Ranked By Auxiliary Or 2 For Manual Selection. ")

  if choice == '1':
    rankedSchoolsAuxiliary = rankSchools(schools, "Auxiliary", recentScores)
    dispSchool(rankedSchoolsAuxiliary, True, recentScores)
  if choice == '2':
    manualSelection(headers, schools, divisions)

    
def northernBreakdown():
  fileName1, fileName2, fileName3 = 'dataWP.csv', 'dataNP.csv', 'dataA.csv'
  dataWP, null = openFile(fileName1)
  dataNP, null = openFile(fileName2)
  dataA , null = openFile(fileName3)
  dataWP, dataNP, dataA  = cleanData(dataWP), cleanData(dataNP), cleanData(dataA)
  
  for entry in dataWP:
    recentScoresWP[entry['School']] = entry
  for entry in dataNP:
    recentScoresNP[entry['School']] = entry
  for entry in dataA:
    recentScoresA[entry['School']] = entry
  
  for school in recentScoresWP:
    schoolsWP.append(school)
  schoolsWP.sort()
  for school in recentScoresNP:
    schoolsNP.append(school)
  schoolsNP.sort()
  for school in recentScoresA:
    schoolsA.append(school)
  schoolsA.sort()
  
  divisionsWP, divisionsNP, divisionsA = set(), set(), set()
  for school in schoolsWP:
    divisionsWP.add(recentScoresWP[school]['Division'])
  for school in schoolsNP:
    divisionsNP.add(recentScoresNP[school]['Division'])
  for school in schoolsA:
    divisionsA.add(recentScoresA[school]['Division'])
  
  school = "Northern York"
  dispSchool(school, False, recentScoresWP)
  
  selectedSchoolsNP = getDivisionSchools("Liberty A", schoolsNP, recentScoresNP)
  ranksNP = rankSchools(selectedSchoolsNP, "Total", recentScoresNP)
  print(f'{school} Placed {ranksNP[school]["Rank"]} Out Of {len(selectedSchoolsNP)} In Liberty A.')
  
  ranksNP = rankSchools(schoolsNP, "Total", recentScoresNP)
  print(f'{school} Placed {ranksNP[school]["Rank"]} Out Of {len(schoolsNP)} Out Of Calvalcade.\n')
  

  selectedSchoolsWP = getDivisionSchools("Liberty A", schoolsWP, recentScoresWP)
  ranksWP = rankSchools(selectedSchoolsWP, "Percussion", recentScoresWP)
  print(f'{school}\'s Percussion Placed {ranksWP[school]["Rank"]} Out Of {len(selectedSchoolsWP)} In Liberty A.')
  
  ranksWP = rankSchools(schoolsWP, "Percussion", recentScoresWP)
  print(f'{school}\'s Percussion Placed {ranksWP[school]["Rank"]} Out Of {len(schoolsWP)} Out Of Calvalcade.\n')
  
  
  selectedSchoolsA = getDivisionSchools("Liberty A", schoolsA, recentScoresA)
  ranksA = rankSchools(selectedSchoolsA, "Auxiliary", recentScoresA)
  print(f'{school}\'s Gaurd Placed {ranksA[school]["Rank"]} Out Of {len(selectedSchoolsA)} In Liberty A.')
  
  ranksA = rankSchools(schoolsA, "Auxiliary", recentScoresA)
  print(f'{school}\'s Gaurd Placed {ranksA[school]["Rank"]} Out Of {len(schoolsA)} Out Of Calvalcade.\n')

  return recentScoresWP, recentScoresNP, recentScoresA
  

def main():
  choice = False
  while choice not in ['1', '2']:
    choice = input("Type 1 For Northern York Breakdown Or 2 For Manual Selection. ")
    
  if choice == '1':
    recentScoresWP, recentScoresNP, recentScoresA = northernBreakdown()
  
  if choice == '2':
    print("Databases:\n\t1: Comps With Percussion Judges\n\t2: Comps With No Special Judges\n\t3: Comps With Auxiliary Judges")
    selectionInput = False
    while selectionInput not in ['1', '2', '3']:
      selectionInput = input("\nWhat Database Would You Like To Look At? ").lower()
    print()
    
    if selectionInput == '1':
      dataWithPercussion()
    elif selectionInput == '2':
      dataNoPercussion()
    elif selectionInput == '3':
      dataAuxiliary()
  
  
if __name__ == '__main__':
  print("Cavalcade 2023 Analyzer\n")
  try:
    main()
  except:
    print("Error Code: 1")
  input("Press Enter To Close Program.")
