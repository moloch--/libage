package main

/*
#include<stdlib.h>
*/
import "C"
import (
	"bytes"
	"fmt"
	"io"
	"strings"
	"unsafe"

	"filippo.io/age"
	"filippo.io/age/agessh"
	"filippo.io/age/armor"
)

var (
	resultPtr *C.char
)

//export FreeResult
func FreeResult() {
	C.free(unsafe.Pointer(resultPtr))
}

//export Encrypt
func Encrypt(cPublicKey *C.char, cPlaintext *C.char) *C.char {
	publicKey := C.GoString(cPublicKey)
	recipient, err := parseRecipient(publicKey)
	if err != nil {
		resultPtr = C.CString("")
	}
	plaintext := C.GoString(cPlaintext)
	ciphertext := bytes.NewBuffer([]byte{})
	err = encrypt([]age.Recipient{recipient}, bytes.NewReader([]byte(plaintext)), ciphertext, true)
	if err != nil {
		resultPtr = C.CString("")
	} else {
		resultPtr = C.CString(ciphertext.String())
	}
	return resultPtr
}

func parseRecipient(arg string) (age.Recipient, error) {
	switch {
	case strings.HasPrefix(arg, "age1"):
		return age.ParseX25519Recipient(arg)
	case strings.HasPrefix(arg, "ssh-"):
		return agessh.ParseRecipient(arg)
	}
	return nil, fmt.Errorf("unknown recipient type: %q", arg)
}

func encrypt(recipients []age.Recipient, in io.Reader, out io.Writer, withArmor bool) error {
	if withArmor {
		a := armor.NewWriter(out)
		defer func() {
			a.Close()
		}()
		out = a
	}
	w, err := age.Encrypt(out, recipients...)
	if err != nil {
		return err
	}
	if _, err := io.Copy(w, in); err != nil {
		return err
	}
	if err := w.Close(); err != nil {
		return err
	}
	return nil
}

func main() {}
