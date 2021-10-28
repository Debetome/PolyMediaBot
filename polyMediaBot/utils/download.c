#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

#include "download.h"
#include "curl/curl.h"

download_t* new_download(char *url, char *filename, FILE *fp) {
  download_t *download = (download_t*)malloc(sizeof(download_t));
  download->url = url;
  download->filename = filename;
  download->curl = curl_easy_init();
  download->fp = fp;

  curl_easy_setopt(download->curl, CURLOPT_URL, download->url);
  curl_easy_setopt(download->curl, CURLOPT_WRITEDATA, download->fp);
  curl_easy_setopt(download->curl, CURLOPT_FAILONERROR, 1L);

  printf("[*] %s\n", download->filename);
  return download;
}

void download_file(download_t *download) {
  curl_easy_perform(download->curl);

  if (download->response != CURLE_OK) {
    fprintf(stderr, "Error: %s\n", 
        curl_easy_strerror(download->response));
  }
  printf("[*] download_ted\n");
}

void clean_download(download_t *download) {
  printf("[*] Cleaning!\n");
  curl_easy_cleanup(download->curl);
  fclose(download->fp);
  free(download);
}

static PyObject* _download_file(PyObject *self, PyObject *args) {
  download_t *download;
  FILE *fp;
  char *url;
  char *filename;

  if (!PyArg_ParseTuple(args, "ss", &url, &filename)) {
    return NULL;
  }

  fp = fopen(filename, "wb");
  download = new_download(url, filename, fp);
  download_file(download);
  clean_download(download);

  return PyUnicode_FromString(filename);
}

static struct PyMethodDef methods[] = {
  {"download_file", (PyCFunction)_download_file, METH_VARARGS},
  {NULL, NULL}
};

static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "download",
  NULL,
  -1,
  methods
};

PyMODINIT_FUNC PyInit_download(void) {
  return PyModule_Create(&module);
}
