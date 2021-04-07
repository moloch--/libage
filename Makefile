GO ?= go

.PHONY: linux
linux:
	CGO_ENABLED=1 GOOS=linux $(GO) build -buildmode=c-shared -o src/age/libage.so

.PHONY: macos
macos:
	CGO_ENABLED=1 GOOS=darwin $(GO) build -buildmode=c-shared -o src/age/libage.dylib

