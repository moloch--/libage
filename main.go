package main

/*
#include<stdlib.h>
*/
import "C"
import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strings"
	"unsafe"

	"filippo.io/age"
	"filippo.io/age/agessh"
	"filippo.io/age/armor"
	"golang.org/x/crypto/ssh"
)

var (
	resultPtr *C.char
)

type LazyScryptIdentity struct {
	Passphrase func() (string, error)
}

//export FreeResult
func FreeResult() {
	if resultPtr != nil {
		C.free(unsafe.Pointer(resultPtr))
		resultPtr = nil
	}
}

//export Encrypt
func Encrypt(cPublicKey *C.char, cPlaintext *C.char) *C.char {
	publicKey := C.GoString(cPublicKey)
	recipient, err := parseRecipient(publicKey)
	if err != nil {
		resultPtr = C.CString("")
	}
	if recipient != nil {
		plaintext := C.GoString(cPlaintext)
		ciphertext := bytes.NewBuffer([]byte{})
		err = encrypt([]age.Recipient{recipient}, bytes.NewReader([]byte(plaintext)), ciphertext, true)
		if err != nil {
			resultPtr = C.CString("")
		} else {
			resultPtr = C.CString(ciphertext.String())
		}
	}
	return resultPtr
}

//export Decrypt
func Decrypt(cPrivateKey *C.char, cCiphertext *C.char) *C.char {
	privateKey := C.GoString(cPrivateKey)
	ciphertext := C.GoString(cCiphertext)

	buf := bytes.NewBuffer([]byte{})
	err := decrypt([]string{privateKey}, bytes.NewReader([]byte(ciphertext)), buf)
	if err != nil {
		resultPtr = C.CString("")
	} else {
		resultPtr = C.CString(buf.String())
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

func decrypt(keys []string, in io.Reader, out io.Writer) error {
	identities := []age.Identity{}

	for _, name := range keys {
		ids, err := parseIdentitiesFile(name)
		if err != nil {
			return err
		}
		identities = append(identities, ids...)
	}

	rr := bufio.NewReader(in)
	if start, _ := rr.Peek(len(armor.Header)); string(start) == armor.Header {
		in = armor.NewReader(rr)
	} else {
		in = rr
	}

	r, err := age.Decrypt(in, identities...)
	if err != nil {
		return err
	}
	if _, err := io.Copy(out, r); err != nil {
		return err
	}
	return nil
}

func parseIdentitiesFile(name string) ([]age.Identity, error) {
	var f *os.File

	var err error
	f, err = os.Open(name)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %v", err)
	}
	defer f.Close()

	b := bufio.NewReader(f)
	const pemHeader = "-----BEGIN"
	if peeked, _ := b.Peek(len(pemHeader)); string(peeked) == pemHeader {
		const privateKeySizeLimit = 1 << 14 // 16 KiB
		contents, err := ioutil.ReadAll(io.LimitReader(b, privateKeySizeLimit))
		if err != nil {
			return nil, fmt.Errorf("failed to read %q: %v", name, err)
		}
		if len(contents) == privateKeySizeLimit {
			return nil, fmt.Errorf("failed to read %q: file too long", name)
		}
		return parseSSHIdentity(name, contents)
	}

	ids, err := age.ParseIdentities(b)
	if err != nil {
		return nil, fmt.Errorf("failed to read %q: %v", name, err)
	}
	return ids, nil
}

func parseSSHIdentity(name string, pemBytes []byte) ([]age.Identity, error) {
	id, err := agessh.ParseIdentity(pemBytes)
	if sshErr, ok := err.(*ssh.PassphraseMissingError); ok {
		pubKey := sshErr.PublicKey
		if pubKey == nil {
			pubKey, err = readPubFile(name)
			if err != nil {
				return nil, err
			}
		}
		passphrasePrompt := func() ([]byte, error) {
			return []byte{}, nil
		}
		i, err := agessh.NewEncryptedSSHIdentity(pubKey, pemBytes, passphrasePrompt)
		if err != nil {
			return nil, err
		}
		return []age.Identity{i}, nil
	}
	if err != nil {
		return nil, fmt.Errorf("malformed SSH identity in %q: %v", name, err)
	}

	return []age.Identity{id}, nil
}

func readPubFile(name string) (ssh.PublicKey, error) {
	if name == "-" {
		return nil, fmt.Errorf(`failed to obtain public key for "-" SSH key
Use a file for which the corresponding ".pub" file exists, or convert the private key to a modern format with "ssh-keygen -p -m RFC4716"`)
	}
	f, err := os.Open(name + ".pub")
	if err != nil {
		return nil, fmt.Errorf(`failed to obtain public key for %q SSH key: %v
Ensure %q exists, or convert the private key %q to a modern format with "ssh-keygen -p -m RFC4716"`, name, err, name+".pub", name)
	}
	defer f.Close()
	contents, err := ioutil.ReadAll(f)
	if err != nil {
		return nil, fmt.Errorf("failed to read %q: %v", name+".pub", err)
	}
	pubKey, _, _, _, err := ssh.ParseAuthorizedKey(contents)
	if err != nil {
		return nil, fmt.Errorf("failed to parse %q: %v", name+".pub", err)
	}
	return pubKey, nil
}

func main() {}
