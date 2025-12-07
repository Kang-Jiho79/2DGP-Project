from pico2d import load_music, load_wav

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        self._music_cache = {}   # path -> music_object
        self._sfx_cache = {}     # key/path -> wav_object
        self.current_music = None
        self.current_music_path = None
        self.music_volume = 1.0  # 0.0 ~ 1.0
        self.sfx_volume = 1.0    # default sfx volume

    # --- Music (BGM) ---
    def load_music(self, path):
        if path in self._music_cache:
            return self._music_cache[path]
        m = load_music(path)
        self._music_cache[path] = m
        return m

    def play_music(self, path=None, loop=True):
        if path is not None:
            m = self.load_music(path)
            self.current_music = m
            self.current_music_path = path
        else:
            m = self.current_music
        if m is None:
            return
        self._apply_music_volume()
        # prefer repeat_play for looping if available
        if loop and hasattr(m, 'repeat_play'):
            m.repeat_play()
        elif hasattr(m, 'play'):
            m.play()

    def stop_music(self):
        if self.current_music and hasattr(self.current_music, 'stop'):
            self.current_music.stop()

    def pause_music(self):
        if self.current_music and hasattr(self.current_music, 'pause'):
            self.current_music.pause()

    def resume_music(self):
        if self.current_music and hasattr(self.current_music, 'resume'):
            self.current_music.resume()

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, float(volume)))
        self._apply_music_volume()

    def _apply_music_volume(self):
        if not self.current_music:
            return
        vol = self.music_volume
        # many pico2d music objects expect integer 0..100-ish
        if hasattr(self.current_music, 'set_volume'):
            try:
                self.current_music.set_volume(int(vol * 100))
            except Exception:
                try:
                    self.current_music.set_volume(vol)
                except Exception:
                    pass

    # --- SFX ---
    def load_sfx(self, path, key=None):
        k = key or path
        if k in self._sfx_cache:
            return self._sfx_cache[k]
        s = load_wav(path)
        self._sfx_cache[k] = s
        return s

    def play_sfx(self, key_or_path, volume=None):
        # if key exists in cache use it, otherwise try loading by path
        s = self._sfx_cache.get(key_or_path)
        if s is None:
            try:
                s = self.load_sfx(key_or_path)
            except Exception:
                return
        vol = self.sfx_volume if volume is None else max(0.0, min(1.0, float(volume)))
        if hasattr(s, 'set_volume'):
            try:
                s.set_volume(int(vol * 100))
            except Exception:
                try:
                    s.set_volume(vol)
                except Exception:
                    pass
        if hasattr(s, 'play'):
            s.play()

    def stop_sfx(self, key_or_path):
        s = self._sfx_cache.get(key_or_path)
        if s and hasattr(s, 'stop'):
            s.stop()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, float(volume)))
        # optionally apply to cached sfx (not strictly necessary)
        for s in self._sfx_cache.values():
            if hasattr(s, 'set_volume'):
                try:
                    s.set_volume(int(self.sfx_volume * 100))
                except Exception:
                    try:
                        s.set_volume(self.sfx_volume)
                    except Exception:
                        pass

# 사용 예시 (코드 주석)
# sm = SoundManager()
# sm.play_music('res/bgm.mp3', loop=True)
# sm.play_sfx('res/hit.wav')
# sm.set_music_volume(0.5)
# sm.set_sfx_volume(0.8)