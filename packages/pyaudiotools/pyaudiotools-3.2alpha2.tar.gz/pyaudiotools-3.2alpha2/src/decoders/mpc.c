#include "mpc.h"
#include "../framelist.h"

/********************************************************
 Audio Tools, a module and set of tools for manipulating audio data
 Copyright (C) 2007-2016  James Buren and Brian Langenberger

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*******************************************************/

#define BITS_PER_SAMPLE 16

static PyObject*
MPCDecoder_new(PyTypeObject *type,
               PyObject *args, PyObject *kwds)
{
    decoders_MPCDecoder *self;

    self = (decoders_MPCDecoder *)type->tp_alloc(type, 0);

    return (PyObject *) self;
}

int
MPCDecoder_init(decoders_MPCDecoder *self,
                PyObject *args, PyObject *kwds)
{
    char *filename;
    mpc_streaminfo si;

    self->reader.data = NULL;
    self->demux = NULL;

    self->channels = 0;
    self->sample_rate = 0;
    self->closed = 0;
    self->stream_finished = 0;

    self->audiotools_pcm = NULL;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return -1;

    if (mpc_reader_init_stdio(&self->reader, filename) == MPC_STATUS_FAIL) {
        PyErr_SetString(PyExc_ValueError, "error opening file");
        return -1;
    }

    if ((self->demux = mpc_demux_init(&self->reader)) == NULL) {
        PyErr_SetString(PyExc_ValueError, "error initializing demuxer");
        return -1;
    }

    mpc_demux_get_info(self->demux, &si);
    self->channels = si.channels;
    self->sample_rate = si.sample_freq;

    if ((self->audiotools_pcm = open_audiotools_pcm()) == NULL)
        return -1;

    return 0;
}

void
MPCDecoder_dealloc(decoders_MPCDecoder *self)
{
    Py_XDECREF(self->audiotools_pcm);

    if (self->demux) {
        mpc_demux_exit(self->demux);
    }

    if (self->reader.data) {
        mpc_reader_exit_stdio(&self->reader);
    }

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject*
MPCDecoder_sample_rate(decoders_MPCDecoder *self, void *closure)
{
    return Py_BuildValue("i", self->sample_rate);
}

static PyObject*
MPCDecoder_bits_per_sample(decoders_MPCDecoder *self, void *closure)
{
    return Py_BuildValue("i", BITS_PER_SAMPLE);
}

static PyObject*
MPCDecoder_channels(decoders_MPCDecoder *self, void *closure)
{
    return Py_BuildValue("i", self->channels);
}

static PyObject*
MPCDecoder_channel_mask(decoders_MPCDecoder *self, void *closure)
{
    switch(self->channels) {
        case 1: return Py_BuildValue("i", 0x4);
        case 2: return Py_BuildValue("i", 0x3);
        default: return Py_BuildValue("i", 0);
    }
}

static PyObject*
MPCDecoder_read(decoders_MPCDecoder* self, PyObject *args)
{
    MPC_SAMPLE_FORMAT buffer[MPC_FRAME_LENGTH * self->channels];
    mpc_frame_info fi = { .buffer = buffer };
    pcm_FrameList *frame;

    if (self->closed) {
        PyErr_SetString(PyExc_ValueError, "stream is closed");
        return NULL;
    }

    if (self->stream_finished) {
        return empty_FrameList(self->audiotools_pcm,
                               self->channels,
                               BITS_PER_SAMPLE);
    }

    if (mpc_demux_decode(self->demux, &fi) == MPC_STATUS_FAIL) {
        PyErr_SetString(PyExc_ValueError, "error decoding MPC frame");
        return NULL;
    }

    if (fi.bits == -1) {
        self->stream_finished = 1;
        return empty_FrameList(self->audiotools_pcm,
                               self->channels,
                               BITS_PER_SAMPLE);
    }

    frame = new_FrameList(self->audiotools_pcm,
                          self->channels,
                          BITS_PER_SAMPLE,
                          fi.samples);

#ifdef MPC_FIXED_POINT
    memcpy(frame->samples,
           buffer,
           sizeof(int) * fi.samples * self->channels);
#else
    float_to_int_converter(BITS_PER_SAMPLE)(fi.samples *
                                            self->channels,
                                            buffer,
                                            frame->samples);
#endif

    return (PyObject*)frame;
}

static PyObject*
MPCDecoder_close(decoders_MPCDecoder* self, PyObject *args)
{
    self->closed = 1;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject*
MPCDecoder_enter(decoders_MPCDecoder* self, PyObject *args)
{
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject*
MPCDecoder_exit(decoders_MPCDecoder* self, PyObject *args)
{
    self->closed = 1;
    Py_INCREF(Py_None);
    return Py_None;
}
