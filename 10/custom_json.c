#include <stdlib.h>
#include <stdio.h>
#include <Python.h>

static PyObject* key = NULL;
static PyObject* value = NULL;

// Function to parse a JSON string and return a Python dictionary
static PyObject* loads(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected a JSON string");
        return NULL;
    }

    if (json_str[0] != '{' || json_str[strlen(json_str) - 1] != '}') {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create dictionary");
        return NULL;
    }

    int number_brackets = 0;
    const char* ptr = json_str + 1;
    number_brackets = 1;

    while (*ptr && number_brackets > 0) {
        if (*ptr == '}') {
            number_brackets -= 1;
            break;
        }

        while (*ptr == ' ' || *ptr == '\n' || *ptr == ',') ptr++;

        if (*ptr == '\"') {
            const char* start = ++ptr;
            while (*ptr && *ptr != '\"') ptr++;
            if (!*ptr) {
                Py_DECREF(dict);
                PyErr_Format(PyExc_TypeError, "Unterminated JSON key");
                return NULL;
            }
            key = PyUnicode_FromStringAndSize(start, ptr - start);
            ptr++; // Skip closing quote
        }

        while (*ptr == ' ' || *ptr == ':') ptr++;

        if (*ptr == '\"') {
            const char* start = ++ptr;
            while (*ptr && *ptr != '\"') ptr++;
            if (!*ptr) {
                Py_DECREF(dict);
                Py_DECREF(key);
                PyErr_Format(PyExc_TypeError, "Unterminated JSON value");
                return NULL;
            }
            value = PyUnicode_FromStringAndSize(start, ptr - start);
            ptr++; // Skip closing quote
        } else if (*ptr == '-' || (*ptr >= '0' && *ptr <= '9')) {
            char* end_ptr;
            long num = strtol(ptr, &end_ptr, 10); // Support negative numbers
            value = PyLong_FromLong(num);
            ptr = end_ptr;
        } else {
            Py_DECREF(dict);
            Py_DECREF(key);
            PyErr_Format(PyExc_TypeError, "Invalid JSON value");
            return NULL;
        }

        if (key && value) {
            if (PyDict_SetItem(dict, key, value) < 0) {
                Py_DECREF(dict);
                Py_DECREF(key);
                Py_DECREF(value);
                return NULL;
            }
            Py_DECREF(key);
            Py_DECREF(value);
            key = NULL;
            value = NULL;
        }
    }

    return dict;
}

// Helper function to convert a Python object to a JSON string
static PyObject* to_json_string(PyObject* obj) {
    if (PyUnicode_Check(obj)) {
        return PyUnicode_FromFormat("\"%U\"", obj);
    } else if (PyLong_Check(obj)) {
        return PyObject_Str(obj);
    } else {
        PyErr_SetString(PyExc_TypeError, "Unsupported value type");
        return NULL;
    }
}

// Helper function to append a key-value pair to the result string
static int append_key_value(PyObject** result, PyObject* key, PyObject* value, int is_last) {
    PyObject* key_str = PyUnicode_FromFormat("\"%U\"", key);
    if (!key_str) return -1;

    PyObject* value_str = to_json_string(value);
    if (!value_str) {
        Py_DECREF(key_str);
        return -1;
    }

    PyUnicode_AppendAndDel(result, key_str);
    PyUnicode_AppendAndDel(result, PyUnicode_FromString(" : "));
    PyUnicode_AppendAndDel(result, value_str);

    if (!is_last) {
        PyUnicode_AppendAndDel(result, PyUnicode_FromString(", "));
    }

    return 0;
}

// Function to serialize a Python dictionary to a JSON string
static PyObject* dumps(PyObject* self, PyObject* args) {
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a dictionary");
        return NULL;
    }

    PyObject* keys = PyDict_Keys(dict);
    PyObject* values = PyDict_Values(dict);

    if (!keys || !values) {
        Py_XDECREF(keys);
        Py_XDECREF(values);
        PyErr_SetString(PyExc_RuntimeError, "Failed to retrieve dictionary items");
        return NULL;
    }

    PyObject* result = PyUnicode_FromString("{");
    Py_ssize_t size = PyList_Size(keys);

    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject* key = PyList_GetItem(keys, i);
        PyObject* value = PyList_GetItem(values, i);

        if (!PyUnicode_Check(key)) {
            Py_DECREF(keys);
            Py_DECREF(values);
            Py_DECREF(result);
            PyErr_SetString(PyExc_TypeError, "Dictionary keys must be strings");
            return NULL;
        }

        if (append_key_value(&result, key, value, i == size - 1) < 0) {
            Py_DECREF(keys);
            Py_DECREF(values);
            Py_DECREF(result);
            return NULL;
        }
    }

    PyUnicode_AppendAndDel(&result, PyUnicode_FromString("}"));
    Py_DECREF(keys);
    Py_DECREF(values);

    return result;
}

// Module method definitions
static PyMethodDef method[] = {
    {"loads", loads, METH_VARARGS, "Parse a JSON string into a Python dictionary"},
    {"dumps", dumps, METH_VARARGS, "Serialize a Python dictionary into a JSON string"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef custom_json_module = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    NULL,
    -1,
    method
};

// Module initialization
PyMODINIT_FUNC PyInit_custom_json(void) {
    PyObject *sysPath = PySys_GetObject("path");
    PyList_Append(sysPath, PyUnicode_FromString("."));
    return PyModule_Create(&custom_json_module);
}
