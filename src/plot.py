
import sys
import warnings
import wave

# supress mpl warning
# https://stackoverflow.com/a/60470942/12231900
warnings.filterwarnings(
    "ignore",
    "(?s).*MATPLOTLIBDATA.*",
    category=UserWarning)
from pylab import *

# stolen from
# https://web.archive.org/web/20161203074728/http://jaganadhg.freeflux.net:80/blog/archive/2009/09/09/plotting-wave-form-and-spectrogram-the-pure-python-way.html


def draw_window(file):
    spf = wave.open(file, 'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')
    f = spf.getframerate()

    subplot(211)
    plot(sound_info)
    title('Wave from and spectrogram of %s' % file)

    subplot(212)
    spectrogram = specgram(
        sound_info,
        Fs=f,
        scale_by_freq=True,
        sides='default')

    show()
    spf.close()
