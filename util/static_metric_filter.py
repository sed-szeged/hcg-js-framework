with open('util/original.csv', 'r') as original:
    data = original.readlines()

merged_data = {}

repo_names = {}

for row in data[1:]:
    repo_link = row.split(',')[3]
    repo_github_link = repo_link.split('blob')[0]

    if repo_github_link in repo_names:
        repo_names[repo_github_link] += 1
    else:
        repo_names[repo_github_link] = 1

with open('util/sheets_data.csv', 'r') as original:
    sheets_data = original.readlines()


sheets_repo_data = {}

for row in sheets_data:
    row = row.split()
    sheets_repo_data[row[0]] = row[1]


for k, v in sheets_repo_data.items():
    merged_data[k] = [int(v)]

for k, v in repo_names.items():
    if k in merged_data:
        merged_data[k].append(v)

for k, v in merged_data.items():
    # print(k, v[0], v[1])
    pass

import csv

with open('filtered.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # header = "Name;Long Name;Path;Repo Name".split(';')

    # sort data by repo name
    data.sort(key=lambda x: x.split(',')[3])

    header = data[0].split(',')
    header.insert(0, 'repo_name')

    writer.writerow(header)

    for i in data[1:]:
        row = i.split(',')
        row[-1] = row[-1].strip()
        repo_github_link = row[3].split('blob')[0]
        repo_name = repo_github_link.split('/')[-2]
        row.insert(0, repo_name)

        if repo_github_link in sheets_repo_data.keys():
            writer.writerow(row)

    print("Filtered.csv done!:)")

# with open('filtered.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#
#     repo_names = set()
#     data = []
#     for row in csv_reader:
#         repo_names.add(row[0].split(';')[3])
#         data.append(row[0].split(';'))

# print(f"Number of repos in filter: {len(repo_names)}")

# print each repo SM count

# print(f"{'Repo Name':20} : SM")
# print("-------------------------")
# for repo_name in repo_names:
#     SM = 0
#     for row in data:
#         if repo_name == row[3]:
#             SM += 1
#
#     print(f"{repo_name:20} : {SM}")
#
# print(f"\n SM sum: {len(data)}")