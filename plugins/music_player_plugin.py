import os

import winsdk.windows.media.control as win_med_ctrl
import winsdk.windows.storage as win_store
import winsdk.windows.storage.streams as win_store_streams

from stdqt import *

import asyncio

"""
Windows Runtime API Reference:
https://learn.microsoft.com/zh-cn/uwp/
"""

def quick_async_run(func):
    def _run(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return _run

async def get_win_med_sessions():   
    return await win_med_ctrl.GlobalSystemMediaTransportControlsSessionManager.request_async()

async def get_win_med_current_session() -> win_med_ctrl.GlobalSystemMediaTransportControlsSession:
    sessions = await get_win_med_sessions()
    return sessions.get_current_session()

@quick_async_run
async def win_med_quick_playing_status_switch() -> int:
    _s = await get_win_med_current_session()
    _pbin = _s.get_playback_info()
    _pbs = _pbin.playback_status
    if _pbs == 5:
        await _s.try_play_async()
    elif _pbs == 4:
        await _s.try_pause_async()
    return 9 - _pbs

@quick_async_run
async def win_med_quick_get_thumbnail() -> str:
    _s = await get_win_med_current_session()
    _smp = await _s.try_get_media_properties_async()
    _fp = f"{os.getenv("TEMP")}/mppt"
    _thbn = await _smp.thumbnail.open_read_async()
    if not os.path.exists(_fp):
        with open(_fp, "wb") as f:
            pass
    _f = await win_store.StorageFile.get_file_from_path_async(f"{os.getenv("TEMP")}/mppt")
    _ofs = await _f.open_async(win_store.FileAccessMode.READ_WRITE)
    _wr = await win_store_streams.RandomAccessStream.copy_and_close_async(_thbn.get_input_stream_at(0), _ofs)
    return _fp

def quick_play(fp:str, parent:QApplication) -> QMediaPlayer:
    qmp = QMediaPlayer(parent=parent)
    qmp.setMedia(QMediaContent(QUrl.fromLocalFile(fp)))
    qmp.setVolume(30)
    qmp.play()
    return qmp

if __name__ == '__main__':
    ''
    print(win_med_quick_playing_status_switch())
    print(win_med_quick_get_thumbnail())
    #get_win_med_current_session().get_playback_info()
    #quick_play('D:\\python_works\\obs\\大喜.flac')