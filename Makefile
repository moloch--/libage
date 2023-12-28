GO ?= go

.PHONY: linux
linux:
	CGO_ENABLED=1 GOOS=linux $(GO) build -buildmode=c-shared -o src/age/libage.so

.PHONY: linux-arm64
linux-arm64:
	CGO_ENABLED=1 GOOS=linux GOARCH=arm64 CC=aarch64-linux-gnu-gcc $(GO) build -buildmode=c-shared -o src/age/libage-arm64.so

.PHONY: macos
macos:
	CGO_ENABLED=1 GOOS=darwin $(GO) build -buildmode=c-shared -o src/age/libage.dylib

