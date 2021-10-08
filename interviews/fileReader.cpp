/*

Problem Statement
Given a low-level API which is awkward to use, develop a more convenient API. Specifically, you're given an API which reads 512 bytes from the given file and returns num bytes read, implement a reader class which makes reads of arbitrary lengths, and for which successive read calls return successive segments of a file.

Present the candidates with a pair of signatures, one that they're given to use and one that they'll have to implement. The given function takes an offset, and reads a specific number of bytes into a given buffer. Signatures for the given function:

  size_t read512(string &file_name, uint64_t offset, uint8_t *buff);

The desired function is given a length and a buffer of at least that size, and should read that many bytes from the file into the buffer. Successive calls should read successive sections of the file. Signatures for the function to implement:

  size_t read(string &file_name, uint64_t length, uint8_t *out);

 */
 #define bufferSize = 512
 size_t read(string &file_name, uint64_t length, uint8_t *out) {
     
    //  file_name.open();
     uint64_t bytes_read = 0;
     uint8_t readOut = malloc(bufferSize * sizeof(uint8_t));
     
     if (length <= 0) return 0;
    
    uint64_t cur_bytes_read = 0;
    // uint64_t bytes_left = length;
     while (bytes_read < length) {
         uint64_t bytes_left = length - bytes_read;
        cur_bytes_read = read512(file_name, bytes_read, readOut);
        bytes_read += cur_bytes_read;
        uint64_t bytes_to_out = bytes_left < cur_bytes_read ? bytes_left : cur_bytes_read;
        memcpy(out, readOut, bytes_to_out);
        memcpy(readOut, 0, sizeof(readOut)); // zero out readOut
        // cur_bytes_read = 0;
     }
     
     return bytes_read;
 }
