MACHINE := $(shell $(CC) -dumpmachine)
WINDOWS := $(strip $(foreach W,-w64- -windows-,$(findstring $W,$(MACHINE))))
BINEXT := $(if $(WINDOWS),.exe,)
SOEXT := $(if $(WINDOWS),.dll,.so)

CFLAGS := $(CFLAGS) -Wall -Wextra -Werror -Wpedantic -Wconversion -Wc++-compat
LDLIBS := -lm

.PHONY: build
build: bin/rsa$(SOEXT)

bin/rsa$(SOEXT): backend/rsa.c backend/rsa.h
	mkdir -p $(@D)
	$(CC) $(CFLAGS) -fPIE -shared -o $@ $(filter %.c,$^) $(LDLIBS)

bin/teste$(BINEXT): backend/teste.c backend/rsa.c backend/rsa.h
	mkdir -p $(@D)
	$(CC) $(CFLAGS) -o $@ $(filter %.c,$^) $(LDLIBS)
