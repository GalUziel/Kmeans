#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include "getMeans.h"

/*CAPI of the project. the getMeans_capi function receives parameters from python and sends them to a c 
function that assigns each point to its best fitting cluster */

static float** setArrays(PyObject* curr_list, Py_ssize_t k, int d);

/* Helper function that receives a python array and returns a proper c array */
static float** setArrays(PyObject* curr_list, Py_ssize_t k, int d) {
    PyObject *item;
    float** p_array;
    int i, j;

    p_array = (float **) malloc(k * sizeof(float *));
    if (p_array == NULL) {
        PyErr_SetString(PyExc_NameError,"Failed to allocate memory");
        return NULL;
    }

    for (i = 0; i < k; i++) {
        item = PyList_GetItem(curr_list, i);
        Py_INCREF(item);
        PyObject *inner_item;
        float* single = malloc(d * sizeof(float));
        if (single == NULL){
            PyErr_SetString(PyExc_NameError,"Failed to allocate memory");
            return NULL;
        }
        for (j = 0; j < d; j++) {
            inner_item = PyList_GetItem(item, j);
            Py_INCREF(inner_item);
            single[j] = PyFloat_AsDouble(inner_item);
            Py_DECREF(inner_item);
        }
        Py_DECREF(item);
        p_array[i] = single;
    }
    return p_array;
}

static PyObject* getMeans_capi(PyObject* self, PyObject* args) {
    PyObject *curr_list,*observations_list,*result_list;
    int k,n,d,MAX_ITER,i;
    float** p_curr_cent;
    float** p_observations;
    int* result;

    if (!PyArg_ParseTuple(args, "iiiiOO", &k, &n, &d, &MAX_ITER, &curr_list, &observations_list)) {
    	PyErr_SetString(PyExc_NameError,"Wrong arguments given");
        return NULL;
    }
    //set centroids
    p_curr_cent = setArrays(curr_list, PyList_Size(curr_list), d);

    //set observations
    p_observations = setArrays(observations_list, PyList_Size(observations_list), d);

    result = (int*)malloc(n * sizeof(int));
    if (result == NULL) {
    	PyErr_SetString(PyExc_NameError,"Failed to allocate memory");
        return NULL;
    }

    result = getMeans(k,n,d,MAX_ITER,p_curr_cent,p_observations);
    result_list = PyList_New(n);
    for (i = 0; i < n; i++){
         PyList_SetItem(result_list, i, PyFloat_FromDouble(result[i]));
    }

/* This builds the answer ("d" = Convert a C double to a Python floating point number) back into a python object */
    return Py_BuildValue("O", result_list); /*  Py_BuildValue(...) returns a PyObject*  */
    }

static PyMethodDef capiMethods[] = {
    {"getMeans",                   /* the Python method name that will be used */
      (PyCFunction) getMeans_capi, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parameters
accepted for this function */
      PyDoc_STR("Calculating k means")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",
    NULL,
    -1,
    capiMethods
};

PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    return PyModule_Create(&moduledef);
}
