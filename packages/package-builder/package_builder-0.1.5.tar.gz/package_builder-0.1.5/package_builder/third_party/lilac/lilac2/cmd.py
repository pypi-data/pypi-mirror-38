import os
import logging
import subprocess
import signal
import sys
import re
from subprocess import CalledProcessError
from typing import Optional
import types

from .typing import Cmd

logger = logging.getLogger(__name__)

def git_pull() -> bool:
  output = run_cmd(['git', 'pull', '--no-edit'])
  return 'up-to-date' not in output

def git_push() -> None:
  while True:
    try:
      run_cmd(['git', 'push'])
      break
    except CalledProcessError as e:
      if 'non-fast-forward' in e.output or 'fetch first' in e.output:
        run_cmd(["git", "pull", "--rebase"])
      else:
        raise

def run_cmd(cmd: Cmd, *, use_pty: bool = False, silent: bool = False,
            cwd: Optional[os.PathLike] = None) -> str:
  logger.debug('running %r, %susing pty,%s showing output', cmd,
               '' if use_pty else 'not ',
               ' not' if silent else '')
  if use_pty:
    rfd, stdout = os.openpty()
    stdin = stdout
    # for fd leakage
    logger.debug('pty master fd=%d, slave fd=%d.', rfd, stdout)
  else:
    stdin = subprocess.DEVNULL
    stdout = subprocess.PIPE

  exited = False
  def child_exited(signum: int, sigframe: types.FrameType) -> None:
    nonlocal exited
    exited = True
  old_hdl = signal.signal(signal.SIGCHLD, child_exited)

  p = subprocess.Popen(
    cmd, stdin = stdin, stdout = stdout, stderr = subprocess.STDOUT,
    cwd = cwd,
  )
  if use_pty:
    os.close(stdout)
  else:
    rfd = p.stdout.fileno()
  out = []

  while True:
    try:
      r = os.read(rfd, 4096)
      if not r:
        if exited:
          break
        else:
          continue
    except InterruptedError:
      continue
    except OSError as e:
      if e.errno == 5: # Input/output error: no clients run
        break
      else:
        raise
    r = r.replace(b'\x0f', b'') # ^O
    if not silent:
      sys.stderr.buffer.write(r)
    out.append(r)

  code = p.wait()
  if use_pty:
    os.close(rfd)
  if old_hdl is not None:
    signal.signal(signal.SIGCHLD, old_hdl)

  outb = b''.join(out)
  outs = outb.decode('utf-8', errors='replace')
  outs = outs.replace('\r\n', '\n')
  outs = re.sub(r'.*\r', '', outs)
  if code != 0:
      raise subprocess.CalledProcessError(code, cmd, outs)
  return outs

