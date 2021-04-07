GO ?= go

.PHONY: libage
libage:
	CGO_ENABLED=1 GOOS=linux $(GO) build -buildmode=c-shared -o src/age/libage.so

