SRCS=xdim.c
OBJS=xdim.o
BINS=xdim

CFLAGS+=-Wall -Wextra -Werror -O2
LDFLAGS+=-lXxf86vm

all: $(BINS)

xdim: xdim.o
	$(CC) $(LDFLAGS) $< -o $@

clean:
	rm -f $(BINS) $(OBJS)