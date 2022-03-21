from youtube_transcript_api import YouTubeTranscriptApi
import re, os

'''
Levels of badness:

Clean: No bad words whatsoever

OK: Some mild mean stuff

Medium: Some mean stuff

Bad: Some bad stuff

Very Bad: Some very bad stuff

'''

class Rater(object): # 1 (best) - 5 (worst)
    LEVEL_FILES_FOLDER = "words"
    LEVEL_FILES = [f"words/l{n}.txt" for n in range(2, 6)]
    VID_ID_REGEX = re.compile("v=[a-zA-Z\d\-_]*")
    FILE_WORDS_SPLITTER_REGEX = "(;|,|\.|\n)"
    RATINGS = "Clean", "OK", "Medium", "Bad", "Very Bad"

    def __init__(self):
        print("Setting Up Files\n")
        self.setup_files()
        print("\nFile Setup Complete\n----")
        self.compiled_words = self.compile_words()

    def setup_files(self):
        try:
            print(f"Creating Folder \"{Rater.LEVEL_FILES_FOLDER}\"")
            os.mkdir(Rater.LEVEL_FILES_FOLDER)
        except FileExistsError:
            print(f"Folder \"{Rater.LEVEL_FILES_FOLDER}\" Already Exists")
        for level_file in Rater.LEVEL_FILES:
            print(f"Creating \"{level_file}\"")
            if os.path.exists(level_file):
                print(f"File \"{level_file}\" Already Exists")
            else:
                open(level_file, "w").close()

    def compile_words(self):
        ret = []
        for level_file in Rater.LEVEL_FILES:
            with open(level_file, "r") as file:
                ret.append(sorted([_.strip().lower() for _ in re.split(Rater.FILE_WORDS_SPLITTER_REGEX, file.read()) if _.strip().lower()], key=len)[::-1])
        return ret

    def get_transcript_from_link(self, link):
        vid_id = Rater.VID_ID_REGEX.findall(link)[-1][2:]  # because the regex includes "v="
        tran_json = YouTubeTranscriptApi.get_transcript(vid_id)
        return "\n".join([dict['text'] for dict in tran_json])

    def combine_stats(self, lst):  # (name, count)
        dict = {}
        for key, value in lst:
            if key in dict:
                dict[key] += value
            else:
                dict[key] = value
        ret = []
        for key in dict:
            ret.append((key, dict[key]))
        return ret

    def rate(self, transcript):
        formatted_transcript = transcript.lower().strip()
        level = None
        for i, level_words in list(enumerate(self.compiled_words))[::-1]:
            for word in level_words:
                if re.findall(f"[^a-zA-Z]({word})[^a-zA-Z]", formatted_transcript):
                    level = i + 2
                    break
            if level is not None:
                break
        else:
            return 1, Rater.RATINGS[0], []
        stats = []
        for lst in self.compiled_words[:level-1][::-1]:  # reverse unnecessary - just so worst words first
            for word in lst:
                count = len(re.findall(f"[^a-zA-Z]({word})[^a-zA-Z]", formatted_transcript))
                if count > 0:
                    stats.append((word if word != "[ __ ]" and word != "\[ __ \]" else "*BEEP*", count))
                    formatted_transcript = re.sub(f"[^a-zA-Z]({word})[^a-zA-Z]", " ", formatted_transcript)  # to remove repeat within words
        stats = self.combine_stats(stats)
        return level, Rater.RATINGS[level-1], stats

def rate_link(link, rater=None):
    if rater is None:
        rater = Rater()
    try:
        transcript = rater.get_transcript_from_link(link)
    except:
        return False
    return rater.rate(transcript)