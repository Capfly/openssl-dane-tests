from OpenSSL import SSL
from socket import socket
from binascii import unhexlify
from cryptography.hazmat.bindings.openssl.binding import Binding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

host = ("stangew.de", 443)

ecodes = {
    0: "X509_V_OK",
    20: "X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY",
    65: "X509_V_ERR_DANE_NO_MATCH"
}


def mycb(cnx, x509, errno, errd, ret):
    cert = x509.to_cryptography()
    print("x509.subject", cert.subject)
    print("x509.serialnr", cert.serial_number)
    print("x509.error", errno, ret, "(%s)" % ecodes[errno])  # error 65 in windows (DANE)
    print()
    return ret


# ## BINDINGS ## #
binding = Binding()
binding.init_static_locks()
_ffi = binding.ffi
_lib = binding.lib
print("openssl version", hex(_lib.OPENSSL_VERSION_NUMBER))

# ## SSL CONTEXT ## #
nctx = SSL.Context(SSL.TLSv1_2_METHOD)
# nctx.load_verify_locations("C:/Users/Wolfi/Desktop/certs/ca-certificates.crt")  # windows-specific
nctx.load_verify_locations("/etc/ssl/certs/ca-certificates.crt")
# nctx.set_verify_depth(5)
nctx.set_verify(SSL.VERIFY_NONE, mycb)  # set callback for debugging
print("ctx_dane_enable", _lib.SSL_CTX_dane_enable(nctx._context))

# ## CONNECTION ## #
sock = socket()
sock.connect(host)
s = SSL.Connection(nctx, sock)
s.set_connect_state()
# _lib.SSL_set_tlsext_host_name(s._ssl, host[0].encode()) # not needed if dane_enable has set the base domain
print("dane_enable", _lib.SSL_dane_enable(s._ssl, host[0].encode()))  # BEFORE HANDSHAKE

# ## TLSA DATA BEFORE HANDSHAKE ## #
usagep = _ffi.new("uint8_t *", 3)
selp = _ffi.new("uint8_t *", 0)
mtp = _ffi.new("uint8_t *", 1)
datap = _ffi.new("unsigned char**",
                 _ffi.new("unsigned char[]",
                          unhexlify("0808104a9462452fffdc5f5f4a7d0d72fb6954951d8ebbbba34358f56904735e")))
szp = _ffi.new("size_t *", 32)
print("tlsa_add", _lib.SSL_dane_tlsa_add(s._ssl, usagep[0], selp[0], mtp[0], datap[0], szp[0]))

# ## HANDSHAKE AND CLOSE ## #
s.do_handshake()
s.shutdown()
sock.close()

#print("get0_dane_tlsa", _lib.SSL_get0_dane_tlsa(s._ssl, usagep, selp, mtp, _ffi.NULL, _ffi.NULL))
