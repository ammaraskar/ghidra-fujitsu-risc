CXX = g++
CFLAGS = -g -Wall
GHIDRA_DECOMP_PATH = ghidra/Ghidra/Features/Decompiler/src/decompile/cpp

ALL := data/languages/fr.sla test/bin/test_harness $(GHIDRA_DECOMP_PATH)/sleigh_dbg $(GHIDRA_DECOMP_PATH)/libsla_dbg.a

all: $(ALL)

data/languages/fr.sla: data/languages/fr.slaspec $(GHIDRA_DECOMP_PATH)/sleigh_dbg
	$(GHIDRA_DECOMP_PATH)/sleigh_dbg data/languages/fr.slaspec

test/bin/test_harness: test/test_harness.c $(GHIDRA_DECOMP_PATH)/libsla_dbg.a
	# -Wno-sign-compare because ghidra's address.hh has warnings.
	$(CXX) -I$(GHIDRA_DECOMP_PATH) $(CFLAGS) -Wno-sign-compare -o $@ $^

$(GHIDRA_DECOMP_PATH)/sleigh_dbg:
	cd $(GHIDRA_DECOMP_PATH) && $(MAKE) sleigh_dbg

$(GHIDRA_DECOMP_PATH)/libsla_dbg.a:
	cd $(GHIDRA_DECOMP_PATH) && $(MAKE) libsla_dbg.a


test: test/bin/test_harness data/languages/fr.sla
	python3 -m unittest

.PHONY: clean test
clean:
	rm -f $(ALL)
