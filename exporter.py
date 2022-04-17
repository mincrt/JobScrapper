import csv

def save_to_file(word, jobs):
    file = open(f"{word}.csv",mode="w", encoding = "utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
        # print(list(job.values()))
    return
