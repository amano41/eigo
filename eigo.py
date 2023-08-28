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
    mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    tts.save(mp3)
    playsound(mp3)
    os.remove(mp3)


def speak_twice(text, lang="en", slow=False, delay=2):
    tts = gTTS(text=text, lang=lang, slow=slow)
    mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    tts.save(mp3)
    playsound(mp3)
    time.sleep(delay)
    playsound(mp3)
    os.remove(mp3)


def main():
    parser = argparse.ArgumentParser(description="Read sentences from a file and speak them.")
    parser.add_argument("file", type=str, help="Path to the file containing the sentences.")
    parser.add_argument("-s", "--slow", action="store_true", default=False, help="Make the speech slow.")
    parser.add_argument("-r", "--random", action="store_true", default=False, help="Randomize the order of sentences.")
    parser.add_argument("-d", "--delay", type=int, default=2, help="Delay between repeated sentences in seconds.")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Interval between sentences in seconds.")

    args = parser.parse_args()

    sentences = read_sentences(args.file)

    if args.random:
        random.shuffle(sentences)

    speak(f"問題数は{len(sentences)}問です。", lang="ja")
    time.sleep(args.delay)

    for i, (en, _) in enumerate(sentences):
        speak(f"No.{i + 1}", lang="en")
        speak_twice(en, lang="en", slow=args.slow, delay=args.delay)
        time.sleep(args.interval)

    speak("答え合わせをしましょう。", lang="ja")
    time.sleep(args.delay)

    for i, (en, jp) in enumerate(sentences):
        speak(f"No.{i + 1}", lang="en")
        speak(en, lang="en", slow=args.slow)
        print(f"({i + 1}) {en}")
        time.sleep(args.delay)
        speak(jp, lang="ja")
        print(f"{jp}\n")
        time.sleep(args.delay)
        speak(en, lang="en", slow=args.slow)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
