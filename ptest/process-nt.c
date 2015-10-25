#include <Python.h>

#include <Windows.h>

#include <stdio.h>

static PyObject *RuntimeError;

static PyObject *TimeoutExpired;

static PyObject *
process_run(PyObject *self, PyObject *args)
{
    char *cmd;
    const char *cwd;
    const char *input;
    const char *output;
    unsigned int timeout;
    SECURITY_ATTRIBUTES attr;
    HANDLE input_handle, output_handle;
    PROCESS_INFORMATION proc_info;
    STARTUPINFO start_info;
    BOOL success;
    unsigned int start_time, end_time;
    PyObject *time;
    unsigned int wait_status;
    unsigned int status;

    if (!PyArg_ParseTuple(args, "ssssI", &cmd, &cwd, &input, &output, &timeout))
        return NULL;

    attr.nLength = sizeof(SECURITY_ATTRIBUTES);
    attr.bInheritHandle = TRUE;
    attr.lpSecurityDescriptor = NULL;

    input_handle = CreateFile(
        "nul",
        GENERIC_READ,
        FILE_SHARE_READ,
        &attr,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_READONLY,
        NULL
    );
    if (input_handle == INVALID_HANDLE_VALUE)
        return PyErr_SetFromWindowsErr(GetLastError());

    output_handle = CreateFile(
        "nul",
        GENERIC_WRITE,
        FILE_SHARE_WRITE,
        &attr,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );
    if (output_handle == INVALID_HANDLE_VALUE)
    {
        CloseHandle(input_handle);
        return PyErr_SetFromWindowsErr(GetLastError());
    }

    ZeroMemory(&proc_info, sizeof(PROCESS_INFORMATION));

    ZeroMemory(&start_info, sizeof(STARTUPINFO));
    start_info.cb = sizeof(STARTUPINFO);
    start_info.wShowWindow = SW_HIDE;
    start_info.hStdInput = input_handle;
    start_info.hStdOutput = output_handle;
    start_info.hStdError = output_handle;
    start_info.dwFlags |= STARTF_USESHOWWINDOW;
    start_info.dwFlags |= STARTF_USESTDHANDLES;

    success = CreateProcess(NULL,
        cmd,
        NULL,
        NULL,
        TRUE,
        0,
        NULL,
        cwd,
        &start_info,
        &proc_info
    );
    if (!success)
        return PyErr_SetFromWindowsErr(GetLastError());

    start_time = GetTickCount();

    wait_status = WaitForSingleObject(proc_info.hProcess, timeout);

    end_time = GetTickCount();
    time = PyFloat_FromDouble((end_time - start_time) / 1000.0);

    CloseHandle(input_handle);
    CloseHandle(output_handle);

    if (WaitForSingleObject(proc_info.hProcess, timeout) == WAIT_TIMEOUT)
    {
        if (!TerminateProcess(proc_info.hProcess, 0))
        {
            PyErr_SetFromWindowsErr(GetLastError());
            goto error;
        }
        WaitForSingleObject(proc_info.hProcess, INFINITE);
        PyErr_SetObject(TimeoutExpired, time);
        goto error;
    }


    if (!GetExitCodeProcess(proc_info.hProcess, &status))
    {
        PyErr_SetFromWindowsErr(GetLastError());
        goto error;
    }

    if (status > 0)
    {
        PyErr_SetObject(RuntimeError, PyTuple_Pack(2, time, PyLong_FromLong(status)));
        return NULL;
    }

    CloseHandle(proc_info.hProcess);
    CloseHandle(proc_info.hThread);

    return time;

error:
    CloseHandle(proc_info.hProcess);
    CloseHandle(proc_info.hThread);
    return NULL;
}

static PyMethodDef ProcessMethods[] =
{
    {"run", process_run, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef processmodule =
{
    PyModuleDef_HEAD_INIT,
    "process",
    NULL,
    -1,
    ProcessMethods
};

PyMODINIT_FUNC
PyInit_process(void)
{
    PyObject *m;

    m = PyModule_Create(&processmodule);
    if (m == NULL)
        return NULL;

    RuntimeError = PyErr_NewException("process.ProcessRuntimeError", NULL, NULL);
    Py_INCREF(RuntimeError);
    PyModule_AddObject(m, "ProcessRuntimeError", RuntimeError);

    TimeoutExpired = PyErr_NewException("process.ProcessTimeoutExpired", NULL, NULL);
    Py_INCREF(TimeoutExpired);
    PyModule_AddObject(m, "ProcessTimeoutExpired", TimeoutExpired);

    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX | SEM_NOALIGNMENTFAULTEXCEPT | SEM_NOOPENFILEERRORBOX);

    return m;
}