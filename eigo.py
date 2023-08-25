import argparse
import os
import random
import tempfile
import time

from gtts import gTTS
from playsound import playsound


def read_sentences(path):
    sentences = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.rstrip().split("\t")
            sentences.append((s[0], s[1]))
    return sentences


def speak(text, lang="en", slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    mp3 = tempfile.NamedTemporaryFile(delete=False).name + ".mp3"
    tts.save(mp3)
    playsound(mp3)
    os.remove(mp3)


def speak_twice(text, lang="en", slow=False, delay=2):
    tts = gTTS(text=text, lang=lang, slow=slow)
    mp3 = tempfile.NamedTemporaryFile(delete=False).name + ".mp3"
    tts.save(mp3)
    playsound(mp3)
    time.sleep(delay)
    playsound(mp3)
    os.remove(mp3)


def main():
    parser = argparse.ArgumentParser(description="Read sentences from a file and speak them.")
    parser.add_argument("file_path", type=str, help="Path to the file containing the sentences.")
    parser.add_argument("-s", "--slow", action="store_true", default=False, help="Make the speech slow.")
    parser.add_argument("-r", "--random", action="store_true", default=False, help="Randomize the order of sentences.")
    parser.add_argument("-d", "--delay", type=int, default=2, help="Delay between repeated sentences in seconds.")
    parser.add_argument("-i", "--interval", type=int, default=4, help="Interval between sentences in seconds.")

    args = parser.parse_args()

    sentences = read_sentences(args.file_path)

    if args.random:
        random.shuffle(sentences)

    for en, _ in sentences:
        speak_twice(en, lang="en", slow=args.slow, delay=args.delay)
        time.sleep(args.interval)

    for en, jp in sentences:
        speak(en, lang="en", slow=args.slow)
        time.sleep(args.delay)
        speak(jp, lang="ja", slow=False)
        time.sleep(args.delay)
        speak(en, lang="en", slow=args.slow)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
