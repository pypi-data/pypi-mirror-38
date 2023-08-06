/* This code was originally copied from Pendulum
(https://github.com/sdispater/pendulum/blob/13ff4a0250177f77e4ff2e7bd1f442d954e66b22/pendulum/parsing/_iso8601.c#L176)
Pendulum (like ciso8601) is MIT licensed, so we have included a copy of its
license here.
*/

/*
Copyright (c) 2015 Sébastien Eustace

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <Python.h>
#include <datetime.h>
#include <structmember.h>

#include "timezone.h"

#define SECS_PER_MIN 60
#define SECS_PER_HOUR (60 * SECS_PER_MIN)

/*
 * class FixedOffset(tzinfo):
 */
typedef struct {
    PyObject_HEAD int offset;
} FixedOffset;

/*
 * def __init__(self, offset):
 *     self.offset = offset
 */
static int
FixedOffset_init(FixedOffset *self, PyObject *args, PyObject *kwargs)
{
    int offset;
    if (!PyArg_ParseTuple(args, "i", &offset))
        return -1;

    self->offset = offset;
    return 0;
}

/*
 * def utcoffset(self, dt):
 *     return timedelta(seconds=self.offset * 60)
 */
static PyObject *
FixedOffset_utcoffset(FixedOffset *self, PyObject *args)
{
    return PyDelta_FromDSU(0, self->offset, 0);
}

/*
 * def dst(self, dt):
 *     return timedelta(seconds=self.offset * 60)
 */
static PyObject *
FixedOffset_dst(FixedOffset *self, PyObject *args)
{
    return PyDelta_FromDSU(0, self->offset, 0);
}

/*
 * def tzname(self, dt):
 *     sign = '+'
 *     if self.offset < 0:
 *         sign = '-'
 *     return "%s%d:%d" % (sign, self.offset / 60, self.offset % 60)
 */
static PyObject *
FixedOffset_tzname(FixedOffset *self, PyObject *args)
{
    char result_tzname[7] = {0};
    char sign = '+';
    int offset = self->offset;

    if (offset < 0) {
        sign = '-';
        offset *= -1;
    }

    sprintf(result_tzname, "%c%02d:%02d", sign, offset / SECS_PER_HOUR,
            offset / SECS_PER_MIN % SECS_PER_MIN);

    return PyUnicode_FromString(result_tzname);
}

/*
 * def __repr__(self):
 *     return self.tzname()
 */
static PyObject *
FixedOffset_repr(FixedOffset *self)
{
    return FixedOffset_tzname(self, NULL);
}

/*
 * def __getinitargs__(self):
 *     return (self.offset,)
 */
static PyObject *
FixedOffset_getinitargs(FixedOffset *self)
{
    PyObject *args = PyTuple_Pack(1, PyLong_FromLong(self->offset));

    if (args == NULL) /* TODO: Test */
        return NULL;

    return args;
}

/*
 * Class member / class attributes
 */
static PyMemberDef FixedOffset_members[] = {
    {"offset", T_INT, offsetof(FixedOffset, offset), 0, "UTC offset"}, {NULL}};

/*
 * Class methods
 */
static PyMethodDef FixedOffset_methods[] = {
    {"utcoffset", (PyCFunction)FixedOffset_utcoffset, METH_VARARGS, ""},
    {"dst", (PyCFunction)FixedOffset_dst, METH_VARARGS, ""},
    {"tzname", (PyCFunction)FixedOffset_tzname, METH_VARARGS, ""},
    {"__getinitargs__", (PyCFunction)FixedOffset_getinitargs, METH_VARARGS,
     ""},
    {NULL}};

static PyTypeObject FixedOffset_type = {
    PyVarObject_HEAD_INIT(
        NULL, 0) "backports.datetime_fromisoformat.FixedOffset", /* tp_name */
    sizeof(FixedOffset),                      /* tp_basicsize */
    0,                                        /* tp_itemsize */
    0,                                        /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_as_async */
    (reprfunc)FixedOffset_repr,               /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash  */
    0,                                        /* tp_call */
    (reprfunc)FixedOffset_repr,               /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "TZInfo with fixed offset",               /* tp_doc */
};

/*
 * Instantiate new FixedOffset_type object
 * Skip overhead of calling PyObject_New and PyObject_Init.
 * Directly allocate object.
 * Note that this also doesn't do any validation of the offset parameter.
 * Callers must ensure that offset is within the range (-1440,1440), exclusive.
 */
PyObject *
new_fixed_offset_ex(int offset, PyTypeObject *type)
{
    FixedOffset *self = (FixedOffset *)(type->tp_alloc(type, 0));

    if (self != NULL)
        self->offset = offset;

    return (PyObject *)self;
}

PyObject *
new_fixed_offset(int offset)
{
    return new_fixed_offset_ex(offset, &FixedOffset_type);
}

/* ------------------------------------------------------------- */

int
initialize_timezone_code(PyObject *module)
{
    int ready_result = 0;
    PyDateTime_IMPORT;
    FixedOffset_type.tp_new = PyType_GenericNew;
    FixedOffset_type.tp_base = PyDateTimeAPI->TZInfoType;
    FixedOffset_type.tp_methods = FixedOffset_methods;
    FixedOffset_type.tp_members = FixedOffset_members;
    FixedOffset_type.tp_init = (initproc)FixedOffset_init;

    ready_result = PyType_Ready(&FixedOffset_type);

    Py_INCREF(&FixedOffset_type);
    PyModule_AddObject(module, "FixedOffset", (PyObject *)&FixedOffset_type);

    return ready_result;
}
