import segyio
import numpy as np
import textwrap


def dt(f, fallback_dt=4000.0):
    """Delta-time

    Infer a ``dt``, the sample rate, from the file. If none is found, use the
    fallback.

    Parameters
    ----------

    f : segyio.SegyFile
    fallback_dt : float
        delta-time to fall back to, in microseconds

    Returns
    -------
    dt : float

    Notes
    -----

    .. versionadded:: 1.1

    """
    return f.xfd.getdt(fallback_dt)


def sample_indexes(segyfile, t0=0.0, dt_override=None):
    """
    Creates a list of values representing the samples in a trace at depth or time.
    The list starts at *t0* and is incremented with am*dt* for the number of samples.
    If a *dt_override* is not provided it will try to find a *dt* in the file.


    Parameters
    ----------
    segyfile :  segyio.SegyFile
    t0 : float
        initial sample, or delay-recording-time
    dt_override : float or None

    Returns
    -------
    samples : array_like of float

    Notes
    -----

    .. versionadded:: 1.1

    """
    if dt_override is None:
        dt_override = dt(segyfile)

    return [t0 + t * dt_override for t in range(len(segyfile.samples))]


def create_text_header(lines):
    """Format textual header

    Create a "correct" SEG-Y textual header.  Every line will be prefixed with
    C## and there are 40 lines. The input must be a dictionary with the line
    number[1-40] as a key. The value for each key should be up to 76 character
    long string.

    Parameters
    ----------

    lines : dict
        `lines` dictionary with fields:

        - ``no`` : line number (`int`)
        - ``line`` : line (`str`)

    Returns
    -------

    text : str

    """

    rows = []
    for line_no in range(1, 41):
        line = ""
        if line_no in lines:
            line = lines[line_no]
        row = "C{0:>2} {1:76}".format(line_no, line)
        rows.append(row)

    rows = ''.join(rows)
    return rows

def wrap(s, width=80):
    """
    Formats the text input with newlines given the user specified width for
    each line.

    Parameters
    ----------

    s : str
    width : int

    Returns
    -------

    text : str

    Notes
    -----

    .. versionadded:: 1.1

    """
    return '\n'.join(textwrap.wrap(str(s), width=width))


def native(data,
           format = segyio.SegySampleFormat.IBM_FLOAT_4_BYTE,
           copy = True):
    """Convert numpy array to native float

    Converts a numpy array from raw segy trace data to native floats. Works for numpy ndarrays.

    Parameters
    ----------

    data : numpy.ndarray
    format : int or segyio.SegySampleFormat
    copy : bool
        If True, convert on a copy, and leave the input array unmodified

    Returns
    -------

    data : numpy.ndarray

    Notes
    -----

    .. versionadded:: 1.1

    Examples
    --------

    Convert mmap'd trace to native float:

    >>> d = np.memmap('file.sgy', offset = 3600, dtype = np.uintc)
    >>> samples = 1500
    >>> trace = segyio.tools.native(d[240:240+samples])

    """

    data = data.view( dtype = np.single )
    if copy:
        data = np.copy( data )

    format = int(segyio.SegySampleFormat(format))
    return segyio._segyio.native(data, format)

def collect(itr):
    """Collect traces or lines into one ndarray

    Eagerly copy a series of traces, lines or depths into one numpy ndarray. If
    collecting traces or fast-direction over a post-stacked file, reshaping the
    resulting array is equivalent to calling ``segyio.tools.cube``.

    Parameters
    ----------

    itr : iterable of numpy.ndarray

    Returns
    -------

    data : numpy.ndarray

    Notes
    -----

    .. versionadded:: 1.1

    Examples
    --------

    collect-cube identity:

    >>> f = segyio.open('post-stack.sgy')
    >>> x = segyio.tools.collect(f.traces[:])
    >>> x = x.reshape((len(f.ilines), len(f.xlines), f.samples))
    >>> numpy.all(x == segyio.tools.cube(f))

    """
    return np.stack([np.copy(x) for x in itr])

def cube(f):
    """Read a full cube from a file

    Takes an open segy file (created with segyio.open) or a file name.

    If the file is a prestack file, the cube returned has the dimensions
    ``(fast, slow, offset, sample)``. If it is post-stack (only the one
    offset), the dimensions are normalised to ``(fast, slow, sample)``

    Parameters
    ----------

    f : str or segyio.SegyFile

    Returns
    -------

    cube : numpy.ndarray

    Notes
    -----

    .. versionadded:: 1.1

    """

    if not isinstance(f, segyio.SegyFile):
        with segyio.open(f) as fl:
            return cube(fl)

    ilsort = f.sorting == segyio.TraceSortingFormat.INLINE_SORTING
    fast = f.ilines if ilsort else f.xlines
    slow = f.xlines if ilsort else f.ilines
    fast, slow, offs = len(fast), len(slow), len(f.offsets)
    smps = len(f.samples)
    dims = (fast, slow, smps) if offs == 1 else (fast, slow, offs, smps)
    return f.trace.raw[:].reshape(dims)

def rotation(f, line = 'fast'):
    """ Find rotation of the survey

    Find the clock-wise rotation and origin of `line` as ``(rot, cdpx, cdpy)``

    The clock-wise rotation is defined as the angle in radians between line
    given by the first and last trace of the first line and the axis that gives
    increasing CDP-Y, in the direction that gives increasing CDP-X.

    By default, the first line is the 'fast' direction, which is inlines if the
    file is inline sorted, and crossline if it's crossline sorted.


    Parameters
    ----------

    f : SegyFile
    line : { 'fast', 'slow', 'iline', 'xline' }

    Returns
    -------

    rotation : float
    cdpx : int
    cdpy : int


    Notes
    -----

    .. versionadded:: 1.2

    """

    if f.unstructured:
        raise ValueError("Rotation requires a structured file")

    lines = { 'fast': f.fast,
              'slow': f.slow,
              'iline': f.iline,
              'xline': f.xline,
            }

    if line not in lines:
        error = "Unknown line {}".format(line)
        solution = "Must be any of: {}".format(' '.join(lines.keys()))
        raise ValueError('{} {}'.format(error, solution))

    l = lines[line]
    origin = f.header[0][segyio.su.cdpx, segyio.su.cdpy]
    cdpx, cdpy = origin[segyio.su.cdpx], origin[segyio.su.cdpy]

    rot = f.xfd.rotation( len(l),
                          l.stride,
                          len(f.offsets),
                          np.fromiter(l.keys(), dtype = np.intc) )
    return rot, cdpx, cdpy

def metadata(f):
    """Get survey structural properties and metadata

    Create a description object that, when passed to ``segyio.create()``, would
    create a new file with the same structure, dimensions, and metadata as
    ``f``.

    Takes an open segy file (created with segyio.open) or a file name.

    Parameters
    ----------

    f : str or segyio.SegyFile

    Returns
    -------
    spec : segyio.spec

    Notes
    -----

    .. versionadded:: 1.4

    """

    if not isinstance(f, segyio.SegyFile):
        with segyio.open(f) as fl:
            return metadata(fl)

    spec = segyio.spec()

    spec.iline = f._il
    spec.xline = f._xl
    spec.samples = f.samples
    spec.format = f.format

    spec.ilines = f.ilines
    spec.xlines = f.xlines
    spec.offsets = f.offsets
    spec.sorting = f.sorting

    spec.tracecount = f.tracecount

    spec.ext_headers = f.ext_headers
    spec.endian = f.endian

    return spec

def resample(f, rate = None, delay = None, micro = False,
                                           trace = True,
                                           binary = True):
    """Resample a file

    Resample all data traces, and update the file handle to reflect the new
    sample rate. No actual samples (data traces) are modified, only the header
    fields and interpretation.

    By default, the rate and the delay are in millseconds - if you need higher
    resolution, passing micro=True interprets rate as microseconds (as it is
    represented in the file). Delay is always milliseconds.

    By default, both the global binary header and the trace headers are updated
    to reflect this. If preserving either the trace header interval field or
    the binary header interval field is important, pass trace=False and
    binary=False respectively, to not have that field updated. This only apply
    to sample rates - the recording delay is only found in trace headers and
    will be written unconditionally, if delay is not None.

    .. warning::
        This function requires an open file handle and is **DESTRUCTIVE**. It
        will modify the file, and if an exception is raised then partial writes
        might have happened and the file might be corrupted.

    This function assumes all traces have uniform delays and frequencies.

    Parameters
    ----------

    f : SegyFile
    rate : int
    delay : int
    micro : bool
        if True, interpret rate as microseconds
    trace : bool
        Update the trace header if True
    binary : bool
        Update the binary header if True

    Notes
    -----

    .. versionadded:: 1.4

    """

    if rate is not None:
        if not micro: rate *= 1000

        if binary: f.bin[segyio.su.hdt] = rate
        if trace: f.header = { segyio.su.dt: rate}

    if delay is not None:
        f.header = { segyio.su.delrt: delay }

    t0 = delay if delay is not None else f.samples[0]
    rate = rate / 1000 if rate is not None else f.samples[1] - f.samples[0]

    f._samples = (np.arange(len(f.samples)) * rate) + t0

    return f
