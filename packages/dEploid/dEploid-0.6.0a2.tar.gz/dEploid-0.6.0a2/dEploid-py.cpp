#include <Python.h>
#include "structmember.h" // fix something array have incomplete type
#include <string>  /* string */
#include <exception>
#include <stdexcept>

#include "lib/src/vcfReader.hpp"
#include "lib/src/mcmc.hpp"
#include "lib/src/dEploidIO.hpp"

#define MODULE_DOC \
"Low level interface for dEploid"


//typedef struct {
    //PyObject_HEAD
    //tree_sequence_t *tree_sequence;
//} TreeSequence;

static void
handle_library_error(int err)
{
    //if (msp_is_kas_error(err)) {
        //PyErr_SetString(MsprimeFileFormatError, msp_strerror(err));
    //} else {
        //switch (err) {
            //case MSP_ERR_FILE_VERSION_TOO_NEW:
                //PyErr_SetString(MsprimeVersionTooNewError, msp_strerror(err));
                //break;
            //case MSP_ERR_FILE_VERSION_TOO_OLD:
                //PyErr_SetString(MsprimeVersionTooOldError, msp_strerror(err));
                //break;
            //case MSP_ERR_FILE_FORMAT:
                //PyErr_SetString(MsprimeFileFormatError, msp_strerror(err));
                //break;
            //case MSP_ERR_OUT_OF_BOUNDS:
                //PyErr_SetString(PyExc_IndexError, msp_strerror(err));
                //break;
            //default:
                //PyErr_SetString(MsprimeLibraryError, msp_strerror(err));
        //}
    //}
    //PyErr_SetString(MsprimeFileFormatError, msp_strerror(err));
}



static PyObject *
dEploid_add(PyObject *self, PyObject *args)
{
    PyObject *ret = NULL;
    double x, y, result;

    if (!PyArg_ParseTuple(args, "dd", &x, &y)) {
        goto out;
    }
    result = x + y;
    ret = Py_BuildValue("d", result);
out:
    return ret;
}

static PyObject *
extractCoverageFromVcf(PyObject *args)
{
    PyObject *ret = NULL;
    //size_t num_tracked_samples;
    int err;
    err = 0;
    //if (SparseTree_get_node_argument(self, args, &node) != 0) {
        //goto out;
    //}
    //err = sparse_tree_get_num_tracked_samples(self->sparse_tree, (node_id_t) node,
            //&num_tracked_samples);

    //if (err != 0) {
        //handle_library_error(err);
        //goto out;
    //}
    ////ret = Py_BuildValue("I", (unsigned int) num_tracked_samples);
//out:
    if ( err != 0 ){
        handle_library_error(err);
    }

    return ret;
}



PyObject* matrixToListList_Double(const vector < vector<double> > &data) {
    PyObject* listListObj = PyList_New( data.size() );
    if (!listListObj) throw std::logic_error("Unable to allocate memory for Python list");

    for (size_t i = 0; i < data.size(); i++) {
        PyObject* listObj = PyList_New(data[i].size());
        for (size_t ii = 0; ii < data[i].size(); ii++) {
            PyObject *num = PyFloat_FromDouble( (double) data[i][ii]);
            if (!num) {
                Py_DECREF(listObj);
                throw std::logic_error("Unable to allocate memory for Python list");
            }
            PyList_SET_ITEM(listObj, ii, num);
        }
        PyList_SET_ITEM(listListObj, i, listObj);
    }
    return listListObj;
}


PyObject* vectorToList_Double(const vector<double> &data) {
    PyObject* listObj = PyList_New( data.size() );
    if (!listObj) throw std::logic_error("Unable to allocate memory for Python list");
    for (unsigned int i = 0; i < data.size(); i++) {
        PyObject *num = PyFloat_FromDouble( (double) data[i]);
        if (!num) {
            Py_DECREF(listObj);
            throw std::logic_error("Unable to allocate memory for Python list");
        }
        PyList_SET_ITEM(listObj, i, num);
    }
    return listObj;
}


PyObject* vectorToList_Str(const vector<string> &data) {
    PyObject* listObj = PyList_New( data.size() );
    if (!listObj) throw std::logic_error("Unable to allocate memory for Python list");
    for (unsigned int i = 0; i < data.size(); i++) {
        PyObject *s = Py_BuildValue("s", data[i].c_str());
        PyList_SET_ITEM(listObj, i, s);
    }
    return listObj;
}


/*===================================================================
 * VcfStruct
 *===================================================================
 */

typedef struct {
    PyObject_HEAD
    bool locked;
    VcfReader *vcfreader;
} VcfStruct;


static int
VcfStruct_check_state(VcfStruct *self)
{
    int ret = 0;
    if (self->vcfreader == NULL) {
        PyErr_SetString(PyExc_SystemError, "VcfStruct not initialised");
        ret = -1;
    }
    return ret;
}

static void
VcfStruct_dealloc(VcfStruct* self)
{
    if (self->vcfreader != NULL) {
        //delete self->vcfreader;
        PyMem_Free(self->vcfreader);
        self->vcfreader = NULL;
    }
    Py_XDECREF(self->vcfreader);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static int
VcfStruct_init(VcfStruct *self, PyObject *args)
{
    int ret = -1;
    int err;

    int ok;
    char *s;
    ok = PyArg_ParseTuple(args, "s", &s);
    if (ok == 0){ // 0 is false/fail, 1 is success
        PyErr_SetString(PyExc_SystemError, "Bad name");
        return ret;
    }
    std::string filename(s);

    try {
        self->vcfreader = new VcfReader(filename);
        self->vcfreader->finalize();
    } catch (const exception &e) {
        PyErr_SetString(PyExc_SystemError, e.what());
        ret = -1;
        return ret;
    }
    ret = 0;
    return ret;
}


static PyObject *
VcfStruct_get_vcfheader(VcfStruct *self)
{
    PyObject *ret = NULL;
    if (VcfStruct_check_state(self) != 0) {
        goto out;
    }
    ret = vectorToList_Str(self->vcfreader->headerLines);
out:
    return ret;
}


static PyObject *
VcfStruct_get_vqslod(VcfStruct *self)
{
    PyObject *ret = NULL;
    if (VcfStruct_check_state(self) != 0) {
        goto out;
    }
    ret = vectorToList_Double(self->vcfreader->vqslod);
out:
    return ret;
}


static PyObject *
VcfStruct_get_refcount(VcfStruct *self)
{
    PyObject *ret = NULL;
    if (VcfStruct_check_state(self) != 0) {
        goto out;
    }
    ret = vectorToList_Double(self->vcfreader->refCount);
out:
    return ret;
}


static PyObject *
VcfStruct_get_altcount(VcfStruct *self)
{
    PyObject *ret = NULL;
    if (VcfStruct_check_state(self) != 0) {
        goto out;
    }
    ret = vectorToList_Double(self->vcfreader->altCount);
out:
    return ret;
}


static PyMemberDef VcfStruct_members[] = {
    {NULL}  /* Sentinel */
};


static PyMethodDef VcfStruct_methods[] = {
    {"get_vcfheader", (PyCFunction) VcfStruct_get_vcfheader, METH_NOARGS,
            "Returns the VCF header as plain text." },
    {"get_refCount", (PyCFunction) VcfStruct_get_refcount, METH_NOARGS,
            "Returns VCF reference allele count." },
    {"get_altCount", (PyCFunction) VcfStruct_get_altcount, METH_NOARGS,
            "Returns VCF alternative allele count." },
    {"get_vqslod", (PyCFunction) VcfStruct_get_vqslod, METH_NOARGS,
            "Returns VCF SNP VQSLOD scores." },
    {NULL}  /* Sentinel */
};


static PyTypeObject Vcf = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_dEploid.Vcf",             /* tp_name */
    sizeof(VcfStruct),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)VcfStruct_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,        /* tp_flags */
    "VcfStruct objects",           /* tp_doc */
    0,                     /* tp_traverse */
    0,                     /* tp_clear */
    0,                     /* tp_richcompare */
    0,                     /* tp_weaklistoffset */
    0,                    /* tp_iter */
    0, /* tp_iternext */
    VcfStruct_methods,             /* tp_methods */
    VcfStruct_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)VcfStruct_init,      /* tp_init */
    //0,                         /* tp_alloc */
    //Noddy_new,                 /* tp_new */
};



/*
 * mcmcChain
 * This will be equivalent to the main function in dEploid
 */


typedef struct {
    PyObject_HEAD
    bool locked;
    McmcSample * mcmcSample; // = new McmcSample();
} McmcSampleStruct;


static int
mcmcChain_check_state(McmcSampleStruct *self)
{
    int ret = 0;
    if (self->mcmcSample == NULL) {
        PyErr_SetString(PyExc_SystemError, "McmcSampleStruct not initialised");
        ret = -1;
    }
    return ret;
}


static void
mcmcChain_dealloc(McmcSampleStruct* self)
{
    if (self->mcmcSample != NULL) {
        //delete self->vcfreader;
        PyMem_Free(self->mcmcSample);
        self->mcmcSample = NULL;
    }
    Py_XDECREF(self->mcmcSample);
    Py_TYPE(self)->tp_free((PyObject*)self);
}


static int
mcmcChain_init(McmcSampleStruct* self, PyObject *args)
{
    int ret = -1;
    int err;

    int ok;
    char *s;
    ok = PyArg_ParseTuple(args, "s", &s);
    std::string cmd(s);
    if (cmd.size() > 0){
        try {
            DEploidIO dEploidIO(cmd);
            self->mcmcSample = new McmcSample();
            MersenneTwister rg(dEploidIO.randomSeed());

            McmcMachinery mcmcMachinery(&dEploidIO.plaf_,
                                        &dEploidIO.refCount_,
                                        &dEploidIO.altCount_,
                                        dEploidIO.panel,
                                        &dEploidIO,
                                        self->mcmcSample,
                                        &rg,
                                        false);  // use IBD
            mcmcMachinery.runMcmcChain(true,     // show progress
                                       false);   // use IBD
        } catch (const exception &e) {
            PyErr_SetString(PyExc_SystemError, e.what());
            ret = -1;
            return ret;
        }
    }
    ret = 0;
    return ret;
}


static PyObject *
mcmcChain_get_proportions(McmcSampleStruct* self)
{
    PyObject *ret = NULL;
    if (mcmcChain_check_state(self) != 0) {
        goto out;
    }
    ret = matrixToListList_Double(self->mcmcSample->proportion);
out:
    return ret;
}


static PyObject *
mcmcChain_get_hap(McmcSampleStruct* self)
{
    PyObject *ret = NULL;
    if (mcmcChain_check_state(self) != 0) {
        goto out;
    }
    ret = matrixToListList_Double(self->mcmcSample->hap);
out:
    return ret;
}


static PyObject *
mcmcChain_get_llk(McmcSampleStruct* self)
{
    PyObject *ret = NULL;
    if (mcmcChain_check_state(self) != 0) {
        goto out;
    }
    ret = vectorToList_Double(self->mcmcSample->sumLLKs);
out:
    return ret;
}


static PyMemberDef mcmcChain_members[] = {
    {NULL}  /* Sentinel */
};


static PyMethodDef mcmcChain_methods[] = {
    {"get_proportions", (PyCFunction) mcmcChain_get_proportions, METH_NOARGS,
            "Returns proportion mcmc samples." },
    {"get_hap", (PyCFunction) mcmcChain_get_hap, METH_NOARGS,
            "Returns haplotypes of last iteration of mcmc samples." },
    {"get_llk", (PyCFunction) mcmcChain_get_llk, METH_NOARGS,
            "Returns likelihood chain of mcmc samples." },
    {NULL}  /* Sentinel */
};


static PyTypeObject mcmcChain = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_dEploid.mcmcChain",             /* tp_name */
    sizeof(McmcSampleStruct),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)mcmcChain_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,        /* tp_flags */
    "McmcSampleStruct objects",           /* tp_doc */
    0,                     /* tp_traverse */
    0,                     /* tp_clear */
    0,                     /* tp_richcompare */
    0,                     /* tp_weaklistoffset */
    0,                    /* tp_iter */
    0, /* tp_iternext */
    mcmcChain_methods,             /* tp_methods */
    mcmcChain_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)mcmcChain_init,      /* tp_init */
    //0,                         /* tp_alloc */
    //Noddy_new,                 /* tp_new */
};


/*
 * dEploid_methods initialization
 */

static PyObject *
dEploid_getProgramVertionStr(PyObject *self)
{
    return Py_BuildValue("s", VERSION);
}


static PyObject *
dEploid_getLibraryVertionStr(PyObject *self)
{
    return Py_BuildValue("s", DEPLOIDVERSION);
}


static PyObject *
dEploid_getLassoLibraryVertionStr(PyObject *self)
{
    return Py_BuildValue("s", LASSOVERSION);
}


static PyObject *
dEploid_getCompileTimeStr(PyObject *self)
{
    return Py_BuildValue("s", COMPILEDATE);
}


static PyMethodDef dEploid_methods[] = {
    {"add", (PyCFunction) dEploid_add, METH_VARARGS,
         "Print a lovely skit to standard output."},
    {"getLibraryVertionStr", (PyCFunction) dEploid_getLibraryVertionStr,
            METH_NOARGS, "Returns the version of the dEploid git version." },
    {"getLassoLibraryVertionStr", (PyCFunction) dEploid_getLassoLibraryVertionStr,
            METH_NOARGS, "Returns the version of the lasso git version." },
    {"getProgramVertionStr", (PyCFunction) dEploid_getProgramVertionStr,
            METH_NOARGS, "Returns the version of the dEploid C++ library." },
    {"getCompileTimeStr", (PyCFunction) dEploid_getCompileTimeStr,
            METH_NOARGS, "Returns the compilation time." },
    {NULL}        /* Sentinel */
};




#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef dEploidmodule = {
    PyModuleDef_HEAD_INIT,
    "_dEploid",
    MODULE_DOC,
    -1,
    dEploid_methods,
    NULL, NULL, NULL, NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit__dEploid(void)

#else
#define INITERROR return

void
init__dEploid(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&dEploidmodule);
#else
    PyObject *module = Py_InitModule3("_dEploid", dEploid_methods, MODULE_DOC);
#endif

    /* Vcf type */
    Vcf.tp_new = PyType_GenericNew;
    if (PyType_Ready(&Vcf) < 0) {
        INITERROR;
    }
    Py_INCREF(&Vcf);
    PyModule_AddObject(module, "Vcf", (PyObject *) &Vcf);


    /* mcmcChain type */
    mcmcChain.tp_new = PyType_GenericNew;
    if (PyType_Ready(&mcmcChain) < 0) {
        INITERROR;
    }
    Py_INCREF(&mcmcChain);
    PyModule_AddObject(module, "mcmcChain", (PyObject *) &mcmcChain);

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
