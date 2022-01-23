#include <stdio.h>
#include <openssl/ssl.h>
// compilen mit gcc filename.c -lssl -o filename

int main() {

 SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
 SSL *ssl = SSL_new(ctx);

 int s0 = SSL_CTX_dane_enable(ctx);
 int s1 = SSL_dane_enable(ssl, "stangew.de");
 uint8_t usage = 3;
 uint8_t select = 0;
 uint8_t mtype = 1;
 unsigned char* data = "0808104a9462452fffdc5f5f4a7d0d72fb6954951d8ebbbba34358f56904735e";

SSL_connect(ssl);

 int s2 = SSL_dane_tlsa_add(ssl, usage, select, mtype, data, 32); // -1, erst muss eine Verbindung her: SSL_connect(ssl)

 printf("%d %d %d\n", s0, s1, s2);

 return 0;
}
