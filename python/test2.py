from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def spotify(persentage):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            volume.SetMasterVolume(persentage, None)


if __name__ == "__main__":
    spotify(1)