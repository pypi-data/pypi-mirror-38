### ML-Crypto
This library is `pycrypto` / `pycryptodome` wrapper that standardises the MissingLink.ai-s encryption and allows easy extentions to support additional encryption schemes.
 
 ## Overview
 * This library contains a set of `Cipher`s.  Each `Cipher` has 
   * `encrpyt` and `decrypt` functions that *MUST* return/accept byte array and 
   * `encrpyt_string` / `decrypt_string` that work with string objects that will be a `base64` representation of the encrypted byte output of the underlying `[en|de]crypt functions`
   * If your cipher returns structured data (such as `IV` and other data), you SHOULD use `namedtuples` and extend them with `MsgPackNamedTuple` mixin. This will allow you to easly dump the named tuple into optimised byterarray, in order to be flexable with the object, currently we are converting the named tuple into `dict` in order to be able to add fields in the feature 
   * You SHOULD provide key generation function as part of the cipher that will generate key (the function may perform external calls in case of cloud kms and etc.) 
 ## Current Ciphers
   * Symmetric - `AES-CTR` encryption with `256` bits (32 bytes) key length
   * Asymmetric - `PKCS1_OAEP` encryption with `SHA512` hashAlgo
   * Envelope - Envelope encryption where the body is encrypted with the `Symmetric` cipher. the `DEK` (data encryption key) is encrypted using non-specific cipher provided during init

  ## PyCryptoDome vs PyCrypto vs None
  * When installing, no cryptography package is provided by default. Use `ml-crypto[pycryptodome]` or `ml-crypto[pycrypto]` to ensure one is installed or use the default if you know you have one installed
  * As `pycrypto` is dead, prefer using `pycryptodome` and expect some issues (The main one is encrypted ssh private keys) not to work
