"""Konwersja zdjęć z FB/WhatsApp do webp + filmów do h264 (src-fb -> img/, video/)."""
import glob, os, subprocess, sys
from PIL import Image, ImageOps
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src-fb')
FF = imageio_ffmpeg.get_ffmpeg_exe()

def fb(n):
    return glob.glob(os.path.join(SRC, 'fb', f'{n:02d}-*.jpg'))[0]

def wa(name):
    return os.path.join(SRC, 'wa', name)

IMAGES = {
    # łazienki
    'lazienka-grafit-1': fb(32), 'lazienka-grafit-2': fb(41), 'lazienka-grafit-3': fb(39),
    'lazienka-grafit-4': fb(40), 'lazienka-granat': fb(29), 'lazienka-tropik': fb(30),
    'lazienka-drewno': fb(34), 'lazienka-okno': fb(35), 'kabina-led-1': fb(33), 'kabina-led-2': fb(36),
    'poddasze-1': fb(37), 'poddasze-2': fb(38), 'lazienka-beton-1': fb(56), 'lazienka-beton-2': fb(57),
    'lazienka-beton-3': fb(55), 'lazienka-zielen-1': fb(23), 'lazienka-zielen-2': fb(24),
    # mozaiki
    'mozaika-kot-czarny': wa('PHOTO-2026-10-23-13-52-09.jpg'), 'mozaika-kot-bialy': wa('PHOTO-2026-10-23-13-52-10.jpg'),
    'mozaika-pies': wa('PHOTO-2026-10-23-13-51-54 3.jpg'), 'mozaika-pies-detal': wa('PHOTO-2026-10-23-13-51-54 4.jpg'),
    'mozaika-twarz': wa('PHOTO-2026-10-23-13-51-54.jpg'), 'mozaika-kot-bialy-2': fb(25), 'mozaika-kot-czarny-2': fb(31),
    # schody, tarasy, podłogi
    'taras-1': fb(42), 'taras-2': fb(43), 'taras-3': fb(44), 'taras-4': fb(45), 'taras-przed': fb(47),
    'schody': fb(28), 'posadzka': fb(27),
    # wnętrza i zabudowy
    'zabudowa-luk-1': fb(22), 'zabudowa-luk-2': fb(6), 'pokoj-1': fb(8), 'pokoj-2': fb(10), 'zabudowa-1': fb(13),
    # w trakcie
    'trakcie-1': fb(26), 'trakcie-2': fb(51), 'trakcie-3': fb(52), 'trakcie-4': fb(54),
    'logo-src': fb(59),
}

def save(im, path, edge, q=80):
    im = im.copy(); im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(path, 'WEBP', quality=q, method=6)
    return im.size

def images():
    for name, src in IMAGES.items():
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        w, h = save(im, os.path.join(ROOT, 'img', f'{name}.webp'), 1800)
        save(im, os.path.join(ROOT, 'img', f'{name}-m.webp'), 860, 76)
        print(name, w, h)

VIDEOS = {
    'lazienka-led': ('reel-3609055772577253.mp4', 'scale=720:-2'),
    'lazienka-marmur': ('reel-39091812680433851.mp4', 'scale=476:-2'),
    'przed-po': ('wa-video.mp4', 'fps=30,scale=478:-2'),
    'lazienka-beton': ('reel-1473101354220182.mp4', 'scale=720:-2'),
}

def videos():
    for name, (src, vf) in VIDEOS.items():
        out = os.path.join(ROOT, 'video', f'{name}.mp4')
        subprocess.run([FF, '-v', 'error', '-y', '-i', os.path.join(SRC, src), '-vf', vf, '-an',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p',
                        '-movflags', '+faststart', out], check=True)
        subprocess.run([FF, '-v', 'error', '-y', '-ss', '2', '-i', out, '-frames:v', '1', '-q:v', '3',
                        os.path.join(SRC, f'poster-{name}.jpg')], check=True)
        im = Image.open(os.path.join(SRC, f'poster-{name}.jpg')).convert('RGB')
        save(im, os.path.join(ROOT, 'img', f'poster-{name}.webp'), 900, 74)
        print(name, os.path.getsize(out) // 1024, 'KB')

if __name__ == '__main__':
    what = sys.argv[1:] or ['images', 'videos']
    if 'images' in what: images()
    if 'videos' in what: videos()
