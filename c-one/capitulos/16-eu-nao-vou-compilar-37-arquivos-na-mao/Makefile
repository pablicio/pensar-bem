CC      = gcc
CFLAGS  = -Wall -Wextra -std=c17 -O2 -MMD -MP
CFLAGS += -Werror=maybe-uninitialized

SRC = $(wildcard src/*.c)
OBJ = $(SRC:src/%.c=build/%.o)

gateway: $(OBJ)
	$(CC) $^ -o $@

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c $< -o $@

build:
	mkdir -p build

simulador: CFLAGS += -DSIMULADOR -O0 -g
simulador: clean gateway

clean:
	rm -rf build gateway

.PHONY: clean simulador

-include $(OBJ:.o=.d)
