#!/usr/bin/env python

# Copyright (c) 2018, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy

import histbook.axis

class Exportable(object):
    """Mix-in for methods that export histograms to third-party software."""

    def pandas(self, *axis, **opts):
        """
        Exports the data in the histogram to a Pandas DataFrame.

        Parameters
        ----------
        *axis : :py:class:`Axis <histbook.axis.Axis>`, algebraic expression (lambda or string), or index position (integer)
            axis or axes to include in the table; if no axes or all :py:class:`profile <histbook.axis.profile>` axes, this function calls :py:meth:`Hist.table <histbook.proj.Projectable.table>`; if all :py:class:`cut <histbook.axis.cut>` axes, this function calls :py:meth:`Hist.fraction <histbook.proj.Projectable.fraction>`

        Keyword Arguments
        -----------------
        **opts : *any*
            passed to :py:meth:`Hist.table <histbook.proj.Projectable.table>` or :py:meth:`Hist.fraction <histbook.proj.Projectable.fraction>`; see these methods for options
        """
        import pandas as pd

        axis = [x if isinstance(x, histbook.axis.Axis) else self.axis[x] for x in axis]

        opts["recarray"] = True
        opts["columns"] = True

        if all(isinstance(x, histbook.axis.ProfileAxis) for x in axis):
            (content, columns) = self.table(*axis, **opts)
            allaxis = self._group + self._fixed

        elif all(isinstance(x, histbook.axis.cut) for x in axis):
            (content, columns), denomhist = self._fraction(axis, opts, True)
            allaxis = denomhist._group + denomhist._fixed

        else:
            raise TypeError("selected axis must be all profiles (for table) or all cuts (for fraction)")

        names = [None for x in allaxis]
        arrays = []
        keys = [[] for x in allaxis]

        def index(j, content, key):
            if j == len(allaxis):
                if len(self._fixed) == 0:
                    arrays.append(numpy.array([content]))

                for j, k in enumerate(key):
                    keys[j].append(k)

            else:
                axis = allaxis[j]
                names[j] = str(axis.expr)

                if isinstance(axis, histbook.axis.groupby):
                    for n in sorted(content):
                        index(j + 1, content[n], key + (n,))

                elif isinstance(axis, histbook.axis.groupbin):
                    closed = "left" if axis.closedlow else "right"
                    for n in sorted(content):
                        if n == "NaN":
                            index(j + 1, content[n], key + ("{NaN}",))
                        else:
                            index(j + 1, content[n], key + (pd.Interval(n, n + float(axis.binwidth), closed=closed),))

                else:
                    if content is not None:
                        arrays.append(content)

                    if isinstance(axis, histbook.axis.bin):
                        closed = "left" if axis.closedlow else "right"
                        if axis.underflow:
                            index(j + 1, None, key + (pd.Interval(float("-inf"), axis.low, closed=closed),))
                        last = axis.low
                        for i in range(axis.numbins):
                            this = (float(i + 1) / float(axis.numbins)) * float(axis.high - axis.low) + float(axis.low)
                            index(j + 1, None, key + (pd.Interval(last, this, closed=closed),))
                            last = this
                        if axis.overflow:
                            index(j + 1, None, key + (pd.Interval(axis.high, float("inf"), closed=closed),))
                        if axis.nanflow:
                            index(j + 1, None, key + ("{NaN}",))

                    elif isinstance(axis, histbook.axis.intbin):
                        if axis.underflow:
                            index(j + 1, None, key + (pd.Interval(float("-inf"), int(axis.min), closed="left"),))
                        for i in range(int(axis.min), int(axis.max) + 1):
                            index(j + 1, None, key + (str(i),))
                        if axis.overflow:
                            index(j + 1, None, key + (pd.Interval(int(axis.max), float("inf"), closed="right"),))

                    elif isinstance(axis, histbook.axis.split):
                        closed = "left" if axis.closedlow else "right"
                        if axis.underflow:
                            index(j + 1, None, key + (pd.Interval(float("-inf"), axis.edges[0], closed=closed),))
                        last = axis.edges[0]
                        for this in axis.edges[1:]:
                            index(j + 1, None, key + (pd.Interval(last, this, closed=closed),))
                            last = this
                        if axis.overflow:
                            index(j + 1, None, key + (pd.Interval(last, float("inf"), closed=closed),))
                        if axis.nanflow:
                            index(j + 1, None, key + ("{NaN}",))

                    elif isinstance(axis, histbook.axis.cut):
                        index(j + 1, None, key + (False,))
                        index(j + 1, None, key + (True,))

                    elif isinstance(axis, histbook.axis._nullaxis):
                        index(j + 1, None, key + ("",))

                    else:
                        raise AssertionError(axis)

        index(0, content, ())

        if len(arrays) == 0:
            return pd.DataFrame(index=pd.MultiIndex.from_arrays(keys, names=names),
                                columns=columns)
        else:
            arrays = numpy.concatenate(arrays)
            return pd.DataFrame(index=pd.MultiIndex.from_arrays(keys, names=names),
                                columns=arrays.dtype.names,
                                data=arrays.view(arrays.dtype[arrays.dtype.names[0]]).reshape(len(keys[0]), -1))

    def root(self, *axis, **opts):
        """
        Exports the data in the histogram to a ROOT histogram.

        The histogram may need to be selected (:py:meth:`Hist.select <histbook.proj.Projectable.select>`) or projected (:py:meth:`Hist.project <histbook.proj.Projectable.project>`) to make it useful in a ROOT histogram.

        Parameters
        ----------
        *axis : :py:class:`Axis <histbook.axis.Axis>`, algebraic expression (lambda or string), or index position (integer)
            axis or axes to include in the output; if no axes, this function returns a histogram of counts; if one :py:class:`profile <histbook.axis.profile>`, this function returns a profile; ...

        Keyword Arguments
        -----------------
        name : string
            name to give to the ROOT object *(default is the empty string)*

        title : string
            title to give to the ROOT object *(default is the empty string)*

        cache : dict-like object
            if supplied, the return value is inserted into ``cache`` keyed by its name; this for convenience (ROOT objects must be kept in scope to be drawn)
        """
        import ROOT

        name = opts.pop("name", "")
        title = opts.pop("title", "")
        cache = opts.pop("cache", {})
        if len(opts) > 0:
            raise TypeError("unrecognized options for Hist.root: {0}".format(" ".join(opts)))

        if len(axis) == 0:
            axis = self._group + self._fixed
        axis = [x if isinstance(x, histbook.axis.Axis) else self.axis[x] for x in axis]
        for x in axis:
            if x not in self._group + self._fixed + self._profile:
                raise IndexError("no such axis: {0}".format(x))

        binaxis = []
        profile = None
        for x in axis:
            if isinstance(x, histbook.axis.ProfileAxis):
                if profile is None:
                    profile = x
                else:
                    raise ValueError("only one profile axis allowed: {0}, {1}".format(profile, x))
            else:
                binaxis.append(x)

        projected = self.project(*binaxis)
        if profile is None:
            content = projected.table(count=True, error=(self._weightparsed is not None))
        else:
            content = projected.table(profile, count=True, error=True)

        if len(binaxis) == 0:
            raise TypeError("cannot present zero-axis data in ROOT")

        elif len(binaxis) == 1 and isinstance(binaxis[0], histbook.axis.groupby):
            if profile is None:
                raise NotImplementedError("TH1 with string-labeled x-axis")

            else:
                raise NotImplementedError("TProfile with string-labeled x-axis")

        elif len(binaxis) == 2 and isinstance(binaxis[0], histbook.axis.groupby) and isinstance(binaxis[1], histbook.axis.groupby):
            if profile is None:
                raise NotImplementedError("TH2 with string-labeled x-axis and y-axis")

            else:
                raise NotImplementedError("TProfile2 with string-labeled x-axis and y-axis")

        elif len(binaxis) == 2 and isinstance(binaxis[0], histbook.axis.groupby):
            if profile is None:
                raise NotImplementedError("TH2 with string-labeled x-axis only")

            else:
                raise NotImplementedError("TProfile2 with string-labeled x-axis only")

        elif len(binaxis) == 2 and isinstance(binaxis[1], histbook.axis.groupby):
            if profile is None:
                raise NotImplementedError("TH2 with string-labeled y-axis only")

            else:
                raise NotImplementedError("TProfile2 with string-labeled y-axis only")

        elif any(isinstance(x, histbook.axis.groupby) for x in binaxis):
            raise TypeError("cannot present more than two categorical axes in ROOT")

        elif any(isinstance(x, histbook.axis.groupbin) for x in binaxis):
            if profile is None:
                raise NotImplementedError("THnSparse with fixed axes converted to sparse")

            else:
                raise TypeError("cannot present sparsely binned profile plots in ROOT")

        elif len(binaxis) == 1:
            xaxis = binaxis[0]

            if profile is None:
                out = ROOT.TH1D(name, title, xaxis.numbins, xaxis.low, xaxis.high)

                entries = numpy.zeros(xaxis.numbins + 2, dtype=numpy.float64)
                entries[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1)] = content["count()"][: (-1 if xaxis.nanflow else None)]
                out.SetContent(entries)
                out.SetEntries(entries.sum())

                if "err(count())" in content.dtype.names:
                    errors = numpy.zeros(xaxis.numbins + 2, dtype=numpy.float64)
                    errors[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1)] = content["err(count())"][: (-1 if xaxis.nanflow else None)]
                    out.SetError(errors)

            else:
                out = ROOT.TProfile(name, title, xaxis.numbins, xaxis.low, xaxis.high)

                entries = numpy.zeros(xaxis.numbins + 2, dtype=numpy.float64)
                entries[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1)] = content[content.dtype.names[0]][: (-1 if xaxis.nanflow else None)]

                contents = numpy.zeros(xaxis.numbins + 2, dtype=numpy.float64)
                contents[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1)] = content[content.dtype.names[2]][: (-1 if xaxis.nanflow else None)]

                errors = numpy.zeros(xaxis.numbins + 2, dtype=numpy.float64)
                errors[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1)] = content[content.dtype.names[3]][: (-1 if xaxis.nanflow else None)]

                # you have to do crazy things to set TProfile bins by hand
                out.SetEntries(entries.sum())
                rootcontents = contents * entries
                rooterrors = numpy.sqrt(((errors**2 * entries) + contents**2) * entries)
                for i in range(xaxis.numbins + 2):
                    out.SetBinEntries(i, entries[i])
                    out.SetBinContent(i, rootcontents[i])
                    out.SetBinError(i, rooterrors[i])

        elif len(binaxis) == 2:
            xaxis = binaxis[0]
            yaxis = binaxis[1]

            if profile is None:
                out = ROOT.TH2D(name, title, xaxis.numbins, xaxis.low, xaxis.high, yaxis.numbins, yaxis.low, yaxis.high)

                entries = numpy.zeros((xaxis.numbins + 2, yaxis.numbins + 2), dtype=numpy.float64)
                entries[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1), (0 if yaxis.underflow else 1) : (None if yaxis.overflow else -1)] = content["count()"][: (-1 if xaxis.nanflow else None), : (-1 if yaxis.nanflow else None)]
                for idx, val in numpy.ndenumerate(entries):
                    out.SetBinContent(idx[0], idx[1], val)
                out.SetEntries(entries.sum())

                if "err(count())" in content.dtype.names:
                    errors = numpy.zeros(xaxis.numbins + 2, yaxis.numbins + 2, dtype=numpy.float64)
                    errors[(0 if xaxis.underflow else 1) : (None if xaxis.overflow else -1), (0 if yaxis.underflow else 1) : (None if yaxis.overflow else -1)] = content["err(count())"][: (-1 if xaxis.nanflow else None), : (-1 if yaxis.nanflow else None)]
                    for idx, val in numpy.ndenumerate(errors):
                        out.SetBinError(idx[0], idx[1], val)

            else:
                raise NotImplementedError("TProfile2D")

        elif len(binaxis) == 3:
            if profile is None:
                raise NotImplementedError("TH3")

            else:
                raise NotImplementedError("TProfile3D")

        else:
            if profile is None:
                raise NotImplementedError("THn")

            else:
                raise TypeError("cannot present more than 3-dimensional profile plots in ROOT")

        cache[out.GetName()] = out
        return out
