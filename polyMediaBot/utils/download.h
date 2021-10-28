#ifndef DOWNLOAD_H
#define DOWNLOAD_H

#include "curl/curl.h"

typedef struct {
  const char *url;
  const char *filename;
  FILE *fp;
  CURL *curl;
  CURLcode response;
} download_t;

download_t* new_download(char *url, char *filename, FILE *fp);
void download_file(download_t *download);
void clean_download(download_t *download);

#endif
