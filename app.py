import click
import textwrap
import datetime
import platform
import os
from gtts import gTTS
from moviepy.editor import *
from api import get_top
from uploader import upload_video
from random import choice
from string import ascii_letters, digits
from ast import literal_eval
from notifypy import Notify


elements = []
tracks = []
ids = []


def generate_id(length):
    sequence = ascii_letters + digits
    s = ""
    for i in range(length):
        s += choice(sequence)
    return s


def generate_exit_id():
    s = generate_id(3)
    return f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}_{s}"


def generate_audio_id():
    s = generate_id(5)
    ids.append(s)
    return s


def create_tts(text, start_time, id):
    tts = gTTS(text, lang='en', tld="co.za")
    tts.save("./tmp/" + id + ".mp3")

    clip = AudioFileClip(
        "./tmp/" + id + ".mp3").set_start(start_time)
    tracks.append(clip)

    return clip.duration


def add_text(label, start_time, duration):
    t = TextClip("\n".join(textwrap.wrap(label, 70)), color="white", fontsize=56, font="Arial-regular").set_position(
        "center").set_start(start_time).set_duration(duration)
    elements.append(t)


@click.group()
def cli():
    pass


@cli.command('compile', short_help="create post compilation")
@click.option('--filename')
@click.option('--intro')
@click.option('--broll')
@click.option('--background')
@click.option('--limit', type=click.INT)
@click.option('--upload', default=False, is_flag=True)
@click.option('--title')
@click.option('--description')
@click.option('--tags')
def compile(filename, intro, broll, background, limit, upload, title, description, tags):

    notif = Notify()
    notif.title = "Reddyt"
    notif.message = f"Creating Reddit compilation: {title}"
    notif.icon = "assets/logo.png"
    notif.send()

    intro_clip = VideoFileClip(intro,
                               audio=True).set_start(0).subclip(0, 5)
    results = get_top(limit)
    start_time = intro_clip.duration + 1

    for result in results:
        audio_id = generate_audio_id()
        t = create_tts(result, start_time, audio_id)
        add_text(result, start_time, t)
        start_time += t

    b_roll_clip = VideoFileClip(
        broll, audio=False).set_start(intro_clip.duration + 1).set_duration(start_time).crop(1920, 1080)  # .fl_image(blur)

    background_clip = AudioFileClip(background).set_start(
        intro_clip.duration + 1).fx(afx.volumex, 0.4)

    elements.insert(0, b_roll_clip)
    tracks.insert(0, background_clip)

    final = CompositeVideoClip([intro_clip, *elements])
    final.audio = CompositeAudioClip([intro_clip.audio, *tracks])
    final.set_duration(start_time).write_videofile("./tmp/" +
                                                   filename + ".mp4", fps=24)

    dirname = os.path.dirname(__file__)
    if upload:
        filename = os.path.join(dirname, 'tmp/' + filename + '.mp4')

        upload_video(filename, title, description, [])

    for file in os.listdir(dirname):
        if file.endswith(".mp3"):
            os.remove(os.path.join(dirname, file))


if "__main__" == __name__:
    cli()
