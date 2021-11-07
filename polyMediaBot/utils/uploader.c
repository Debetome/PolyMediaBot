#include <curl/curl.h>
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "uploader.h"

static char* BASE_URL = "https://api.telegram.com/";

static void set_endpoint(upload_t *self) {
  if (self->token == NULL) {
    fprintf(stderr, "Token unavailable!\n");
    return;
  }
  printf("[*] Token checked!");

  if (self->chat_id == NULL) {
    fprintf(stderr, "chat id not provided!\n");
    return;
  }
  printf("[*] Chat id checked!\n");

  size_t total_size = (sizeof(char) * strlen(self->token))
                    + (sizeof(char) * strlen(self->chat_id))
                    + (sizeof(char) * strlen(self->answer))
                    + (sizeof(char) * 50);

  self->endpoint = (char*)malloc(sizeof(char) * strlen(BASE_URL) + total_size);
  printf("[*] Endpoint ptr created!\n");

  strncpy(self->endpoint, BASE_URL, strlen(BASE_URL) * sizeof(char));
  printf("[*] Base url parsed!\n");
  strncat(self->endpoint, self->token, strlen(self->token) * sizeof(char));
  printf("[*] Token parsed!\n");
  strncat(self->endpoint, "/sendVideo", sizeof(char) * 11);
  printf("[*] Endpoint parsed!\n");
  strncat(self->endpoint, "?chat_id=", sizeof(char) * 10);
  printf("[*] Chat id parsed!\n");
  strncat(self->endpoint, self->chat_id, strlen(self->chat_id) * sizeof(char));
  printf("[*] Endpoint parameters parsed!\n");

  if (self->answer != NULL) {
    strncat(self->endpoint, "&answer=", sizeof(char) * 10);
    strncat(self->endpoint, self->answer, strlen(self->answer) * sizeof(char));
  }
  printf("[*] Answer was parsed!\n");

  strncat(self->endpoint, "&video=", sizeof(char) * 9);
  strncat(self->endpoint, self->fp, sizeof(self->fp));
  printf("[*] Video was parsed!\n");
  printf("[*] Endpoint parsed!\n");
}

static void set_token(upload_t *self, char *token) {
  self->token = (char*)malloc(strlen(token) * sizeof(char) 
                             + sizeof(char) * 4);

  strncpy(self->token, "bot", sizeof(char) * 4);
  strncat(self->token, token, sizeof(char) * strlen(token));
  printf("[*] Token parsed!\n");
}

upload_t *new_upload(char *token, char *chat_id, char *answer, FILE *fp) {
  upload_t *self = (upload_t*)malloc(sizeof(upload_t));
  self->curl = curl_easy_init();
  self->chat_id = chat_id;
  self->answer = answer;
  self->fp = fp;

  set_token(self, token);
  printf("%s\n", self->token);
  set_endpoint(self);

  curl_easy_setopt(self->curl, CURLOPT_URL, self->endpoint);
  curl_easy_setopt(self->curl, CURLOPT_CUSTOMREQUEST, "GET");
  curl_easy_setopt(self->curl, CURLOPT_FAILONERROR, 1L);

  printf("[*] Object created!\n");
  return self;
}


int upload_file(upload_t *self) {
  self->response = curl_easy_perform(self->curl);
  if (self->response != CURLE_OK) {
    fprintf(stderr, "Error: %s\n",
        curl_easy_strerror(self->response));
    return 0;
  }
  printf("[*] File uploaded!\n");
  return 1;
}

void clean_upload(upload_t *self) {
  fclose(self->fp);
  free(self->endpoint);
  free(self->token);
  curl_easy_cleanup(self->curl);
  free(self);
  printf("[*] Object cleaned!\n");
}

static PyObject *_upload_file(PyObject *self, PyObject *args) {
  upload_t *upload;
  FILE *fp;
  char *filename;

  char *chat_id;
  char *token;
  char *answer;

  if (!PyArg_ParseTuple(args, "ssss", &token, &chat_id, &answer, &filename)) {
    return Py_False;
  }

  fp = fopen(filename, "rb");
  if (!fp) {
    fprintf(stderr, "Unable to open file '%s'\n", filename);
    return Py_False;
  }

  printf("[*] Options parsed!\n");

  upload = new_upload(token, chat_id, answer, fp);
  if (!upload_file(upload))
    return Py_False;
  clean_upload(upload);

  return Py_True;
}

static struct PyMethodDef methods[] = {
  {"upload_file", (PyCFunction)_upload_file, METH_VARARGS},
  {NULL, NULL}
};

static struct  PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "upload",
  NULL,
  -1,
  methods
};

PyMODINIT_FUNC PyInit_upload(void) {
  return PyModule_Create(&module);
}
