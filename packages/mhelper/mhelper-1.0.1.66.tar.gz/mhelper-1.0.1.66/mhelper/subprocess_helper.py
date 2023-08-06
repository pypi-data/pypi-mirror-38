from queue import Empty, Queue
from threading import Event, Thread
from typing import Callable, IO, List, Union, Sequence

import os
import subprocess
import warnings

from mhelper import ansi, exception_helper


__DOnOutput = Callable[[str], None]


def execute( command: List[str],
             *,
             dir: str = None,
             on_stdout: __DOnOutput = None,
             on_stderr: __DOnOutput = None,
             echo: bool = False,
             err: bool = False,
             tx: str = None,
             keep_lines: bool = False,
             rx_stdout: bool = False,
             rx_stderr: bool = False,
             rx_out: bool = False,
             rx_code: bool = False ) -> Union[str, int, list, tuple]:
    """
    Executes an external command.
    This function blocks until it completes, but the command is executed in its own thread to allow
    output to be diverted to the provided functions.
    
    :param command:             Command sequence to run.
                                See `Popen`. 
    :param dir:                 Working directory.
                                The original is restored after execution.
                                `None`: Do not change
    :param on_stdout:           Callable that receives lines (`str`) from stdout. 
    :param on_stderr:           Callable that receives lines (`str`) from stderr.
    :param echo:                When `True`, the command line, stdout and stderr are printed. 
    :param err:                 When `True`, a non-zero return code raises a `SubprocessError`. 
    :param tx:                  Input to send to `stdin`.
                                `None`: Send nothing 
    :param rx_stdout:           When `True`, stdout is buffered and returned.
    :param rx_stderr:           When `True`, stderr is buffered and returned. 
    :param rx_out:              When `True`, a common stdout and stderr buffer is created and
                                returned.
    :param keep_lines:          When `True`, buffers are returned as lists.
    :param rx_code:             When `True`, the exit code is returned.
                                This is implicit if no other `rx_` arguments are passed.
    :return: Either a single value, or a tuple if multiple collect statements are specified.
             In this case the following order is used: out, stdout, stderr, code.
    """
    # Stream arguments?
    if on_stdout is None:
        on_stdout = __ignore
    
    if on_stderr is None:
        on_stderr = __ignore
    
    # Echo argument?
    if echo:
        print( ansi.FORE_YELLOW + "{}".format( command ) + ansi.RESET )
        on_stdout = __PrintStdOut( "O>" + ansi.DIM + ansi.FORE_GREEN, on_stdout )
        on_stderr = __PrintStdOut( "E>" + ansi.DIM + ansi.FORE_RED, on_stderr )
    
    # Collect arguments?
    common_array = []
    stdout_array = []
    stderr_array = []
    
    if rx_out:
        on_stdout = __Collect( common_array, on_stdout )
        on_stderr = __Collect( common_array, on_stderr )
    
    if rx_stdout:
        on_stdout = __Collect( stdout_array, on_stdout )
    
    if rx_stderr:
        on_stderr = __Collect( stderr_array, on_stderr )
    
    # Directory argument?
    cwd = None
    
    if dir:
        if not os.path.isdir( dir ):
            raise FileNotFoundError( "Not a directory: " + dir )
        
        cwd = os.getcwd()
        os.chdir( dir )
    
    # Invoke process
    try:
        process = subprocess.Popen( command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE )
        
        # Stdin argument?
        if tx is not None:
            process.stdin.write( tx.encode( "UTF-8" ) )
        
        process.stdin.close()
        
        # Read asynchronously
        stdout_queue = Queue()
        stderr_queue = Queue()
        event = Event()
        
        thread_1 = Thread( target = __enqueue_stream, args = (process.stdout, stdout_queue, event) )
        thread_1.name = "async_run.stdout_thread(" + " ".join( command ) + ")"
        thread_1.daemon = True
        thread_1.start()
        
        thread_2 = Thread( target = __enqueue_stream, args = (process.stderr, stderr_queue, event) )
        thread_2.name = "async_run.stderr_thread(" + " ".join( command ) + ")"
        thread_2.daemon = True
        thread_2.start()
        
        thread_3 = Thread( target = __wait_exit, args = (process, event) )
        thread_2.name = "async_run.exit_thread(" + " ".join( command ) + ")"
        thread_3.daemon = True
        thread_3.start()
        
        while process.returncode is None:
            event.wait()
            event.clear()
            used = True
            
            while used:
                used = False
                
                try:
                    line = stdout_queue.get_nowait()
                except Empty:
                    pass
                else:
                    on_stdout( line )
                    used = True
                
                try:
                    line = stderr_queue.get_nowait()
                except Empty:
                    pass
                else:
                    on_stderr( line )
                    used = True
    finally:
        if cwd is not None:
            os.chdir( cwd )
    
    if err and process.returncode:
        raise exception_helper.SubprocessError(
                "SubprocessError 2. The command «{}» exited with error code «{}». "
                "If available, checking the output may provide more details."
                    .format( " ".join( '"{}"'.format( x ) for x in command ),
                             process.returncode ),
                return_code = process.returncode )
    
    r = []
    
    if rx_out:
        r.append( __as( keep_lines, common_array ) )
    
    if rx_stdout:
        r.append( __as( keep_lines, stdout_array ) )
    
    if rx_stderr:
        r.append( __as( keep_lines, stderr_array ) )
    
    if rx_code or not r:
        r.append( process.returncode )
    
    if len( r ) == 1:
        return r[0]
    else:
        return tuple( r )


def __enqueue_stream( out: IO, queue: Queue, event ) -> None:
    for line in out:
        line = line.decode()
        if line.endswith( "\n" ):
            line = line[:-1]
        queue.put( line )
        event.set()
    
    out.close()


def __wait_exit( process: subprocess.Popen, event: Event ) -> None:
    process.wait()
    event.set()


class __PrintStdOut:
    def __init__( self, pfx, orig ):
        self.pfx = pfx
        self.orig = orig
    
    
    def __call__( self, line ):
        print( self.pfx + line + ansi.RESET )
        self.orig( line )


class __Collect:
    def __init__( self, arr, orig ):
        self.arr = arr
        self.orig = orig
    
    
    def __call__( self, line ):
        self.arr.append( line )
        self.orig( line )


def __ignore( _ ):
    pass


def __as( keep_lines, array ):
    if keep_lines:
        return array
    else:
        return "\n".join( array )


# region Deprecated
def run( wd: str, cmd: Union[str, Sequence[str]], *, echo = False ):
    warnings.warn( "Deprecated - use execute", DeprecationWarning )
    if isinstance( cmd, str ):
        cmd = cmd.split( " " )
    return execute( dir = wd,
                    command = cmd,
                    echo = echo,
                    rx_stdout = True )


def run_subprocess( wd: str, cmd: Union[str, Sequence[str]], *, echo = False ) -> str:
    warnings.warn( "Deprecated - use execute", DeprecationWarning )
    if isinstance( cmd, str ):
        cmd = cmd.split( " " )
    return execute( dir = wd,
                    command = cmd,
                    echo = echo,
                    rx_stdout = True )
# endregion
