import os
import win32con
import win32event
import win32file
import win32pipe
from jupyter_core.paths import jupyter_runtime_dir
from twisted.internet import abstract, defer, task

def get_pipe_path(name):
    return "\\\\.\\pipe\\ilua_{}_{}".format(name, os.getpid())

class Win32NamedPipe(abstract.FileDescriptor):
    BUFF_SIZE = 8192
    def __init__(self, path, mode, reactor=None):
        super(Win32NamedPipe, self).__init__(reactor=reactor)
        self.path = path
        self.mode = mode

        self._write_in_progress = 0
        self._write_queue = []

        self._actual_mode = win32con.FILE_FLAG_OVERLAPPED
        if 'r' in self.mode:
            self._actual_mode |= win32con.PIPE_ACCESS_INBOUND
        elif 'w' in self.mode:
            self._actual_mode |= win32con.PIPE_ACCESS_OUTBOUND
        else:
            raise ValueError("mode must be 'r' or 'w'")

        self._handle = win32pipe.CreateNamedPipe(self.path, self._actual_mode,
                                                 win32con.PIPE_TYPE_BYTE,
                                                 1, 0, 0, 2000, # Arbitrary?
                                                 None)

    def pipeOpened(self):
        pass

    def dataReceived(self, data):
        pass

    def _connected(self):
        self._connect_deferred.callback(None)

    @defer.inlineCallbacks
    def open(self):
        self._olapped_io = win32file.OVERLAPPED()
        if 'w' in self.mode:
            self._olapped_io.hEvent = win32event.CreateEvent(None, False,
                                                             False, None)
            self.reactor.addEvent(self._olapped_io.hEvent, self,
                                  'pipeWrite')
        else:
            self._olapped_io.hEvent = win32event.CreateEvent(None, True,
                                                             False, None)
            self.reactor.addEvent(self._olapped_io.hEvent, self,
                                  'pipeRead')

        self._olapped_connect = win32file.OVERLAPPED()
        self._olapped_connect.hEvent = win32event.CreateEvent(None, True,
                                                              False, None)

        self._connect_deferred = defer.Deferred()
        win32pipe.ConnectNamedPipe(self._handle, self._olapped_connect)
        self.reactor.addEvent(self._olapped_connect.hEvent, self, '_connected')
        yield self._connect_deferred
        self.reactor.removeEvent(self._olapped_connect.hEvent)

        if 'r' in self.mode:
            self._read_buffer = win32file.AllocateReadBuffer(8192)
            win32file.ReadFile(self._handle, self._read_buffer,
                               self._olapped_io)

    def pipeRead(self):
        n = win32file.GetOverlappedResult(self._handle, self._olapped_io, 0)
        data = self._read_buffer[:n]
        self.dataReceived(data)
        win32event.ResetEvent(self._olapped_io.hEvent)
        win32file.ReadFile(self._handle, self._read_buffer, self._olapped_io)

    # Shamelessly ripped off twisted.internet._win32serialport
    def write(self, data):
        if data:
            if self._write_in_progress:
                self._write_queue.append(data)
            else:
                self._write_in_progress = 1
                win32file.WriteFile(self._handle, data, self._olapped_io)

    def writeSequence(self, data):
        for chunk in data:
            self.write(data)

    def pipeWrite(self):
        try:
            data = self._write_queue.pop(0)
        except IndexError:
            self._write_in_progress = 0
            return
        else:
            win32file.WriteFile(self._handle, data, self._olapped_io)

    def connectionLost(self, reason):
        super(Win32NamedPipe, self).connectionLost(reason)
        self.reactor.removeEvent(self._olapped_io.hEvent)
        self._handle.close()
