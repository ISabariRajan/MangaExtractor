from MangaStripper import ChapMangaNelo
from Utilities import log, join_path

log("Starting ->")

manga_tracker = join_path("Mangas", "manga_tracker.txt")
completed_manga = join_path("Mangas", "completed_manga.txt")
error_manga = join_path("Mangas", "error_manga.txt")
mangas = []
completed = []
error = []

log("Reading Manga Tracker ...")
with open(manga_tracker, "r") as f:
    mangas = f.readlines()

mangastripper = ChapMangaNelo(browser="firefox")
for manga in mangas:
    manga = manga.replace("\n", "").strip()
    http_split = manga.split("//")
    temp = ""
    if len(http_split) > 1:
        temp += http_split[0]
        http_split = http_split[1].split("/")
        temp += "//" + "/".join(http_split[:2])
        manga = temp
    if mangastripper.extract_manga(manga):
        completed.append(manga + "\n")
    else:
        error.append(manga + "\n")

mangastripper.close()

log("Writing Complated Manga Details...")
with open(completed_manga, "w") as f:
    f.writelines(completed)

log("Writing Error Manga Details...")
with open(error_manga, "w") as f:
    f.writelines(error)