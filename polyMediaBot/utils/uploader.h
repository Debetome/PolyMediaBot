#ifndef UPLOADER_H
#define UPLOADER_H

#define BUFFER 2048

#include <curl/curl.h>

typedef struct {
  FILE *fp;
  int *chat_id;
  char *endpoint;
  char *token;
  char *answer;
  CURL *curl;
  CURLcode response;
} upload_t;

upload_t *new_upload(char *token, int chat_id, char *answer, FILE *fp);
int upload_file(upload_t *self);
void clean_upload(upload_t *self);

#endif
