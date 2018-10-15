import re
import csv

# git diff last_version..new_version > buffer

with open('patch.diff') as diffFile:
    diff = diffFile.readlines()

params = []
for line in diff:
    lineMatch = re.search('^(\+|\-)\ +initConfig\w+\(\ *"([\w_]+)"\ *,*\ *&([\w_]+).+$', line)
    if lineMatch:
        params.append([lineMatch.group(1), lineMatch.group(2), lineMatch.group(3)])

paramCounts = {}
for param in params:
    thisParamCount = params.count(param)
    otherParam = list(param)
    otherParam[0] = '+' if otherParam[0] == '-' else '-'
    otherParamCount = params.count(otherParam)
    # if thisParamCount == 1 and otherParamCount == 1:
    #     continue  # Trivial case: go past
    paramCounts[(param[1], param[2])] = [thisParamCount, otherParamCount]
    print('{0},{1},{2}'.format(param[0], param[1], param[2]))


# with open('patch.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile)
#     for key in paramCounts.keys():
#         writer.writerow([key[0], key[1], paramCounts[key][0], paramCounts[key][1]])
#
# go through the whole structure and look for exact pairs of + or - (and throw a notice if it's not a pair)
# write what's left to a CSV file'