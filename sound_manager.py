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
        self._playing_handles = {}  # key -> ('channel'|'object', handle)
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
            try:
                self.current_music.stop()
            except Exception:
                pass

    def pause_music(self):
        if self.current_music and hasattr(self.current_music, 'pause'):
            try:
                self.current_music.pause()
            except Exception:
                pass

    def resume_music(self):
        if self.current_music and hasattr(self.current_music, 'resume'):
            try:
                self.current_music.resume()
            except Exception:
                pass

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, float(volume)))
        self._apply_music_volume()

    def _apply_music_volume(self):
        if not self.current_music:
            return
        vol = self.music_volume
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

    def play_sfx(self, key_or_path, volume=None, loop=False):
        k = key_or_path
        s = self._sfx_cache.get(k)
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

        # 먼저 기존에 루프 재생중인 핸들 있으면 제거(중복 방지)
        if loop and k in self._playing_handles:
            self.stop_sfx(k)

        # 루프 재생 처리: 가능한 모든 방식 시도하고 핸들 저장
        if loop:
            # prefer repeat_play if provided
            if hasattr(s, 'repeat_play'):
                try:
                    s.repeat_play()
                    self._playing_handles[k] = ('object', s)
                    return
                except Exception:
                    pass
            # try common play loop signatures, store returned channel if any
            try:
                ch = None
                try:
                    ch = s.play(-1)  # some libs accept -1 for infinite loop
                except TypeError:
                    try:
                        ch = s.play(loops=-1)
                    except TypeError:
                        ch = s.play()
                # store whatever handle or object so stop can attempt to stop it
                if ch is not None:
                    self._playing_handles[k] = ('channel', ch)
                else:
                    self._playing_handles[k] = ('object', s)
            except Exception:
                # fallback to single play if looping failed
                try:
                    if hasattr(s, 'play'):
                        s.play()
                except Exception:
                    pass
        else:
            # non-loop play once
            try:
                if hasattr(s, 'play'):
                    s.play()
            except Exception:
                pass

    def stop_sfx(self, key_or_path):
        k = key_or_path
        # first try any stored handle
        handle = self._playing_handles.pop(k, None)
        if handle:
            typ, obj = handle
            try:
                # channel-like stop
                if typ == 'channel' and hasattr(obj, 'stop'):
                    obj.stop()
                    return
                # object may have stop()
                if typ == 'object' and hasattr(obj, 'stop'):
                    obj.stop()
                    return
            except Exception:
                pass
        # fallback: stop cached sfx object directly
        s = self._sfx_cache.get(k)
        if s and hasattr(s, 'stop'):
            try:
                s.stop()
            except Exception:
                pass

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, float(volume)))
        for s in self._sfx_cache.values():
            if hasattr(s, 'set_volume'):
                try:
                    s.set_volume(int(self.sfx_volume * 100))
                except Exception:
                    try:
                        s.set_volume(self.sfx_volume)
                    except Exception:
                        pass