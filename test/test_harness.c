/*
A fairly simple utility that takes instructions as binary on stdin and then
prints out ghidra disassembly for it on stdout.
*/
#include <iostream>
#include <cassert>

#include "loadimage.hh"
#include "sleigh.hh"

// This is a tiny LoadImage class which feeds the executable bytes to the
// translator
class MyLoadImage : public LoadImage {
    uintb baseaddr;
    int4 length;
    uint1* data;

public:
    MyLoadImage(uint1* ptr, int4 sz)
        : LoadImage("nofile")
    {
        baseaddr = 0;
        data = ptr;
        length = sz;
    }
    uintb getLastAddress() { return baseaddr + length; }
    uintb getBaseAddress() { return baseaddr; }
    virtual void loadFill(uint1* ptr, int4 size, const Address& addr);
    virtual string getArchType(void) const { return "myload"; }
    virtual void adjustVma(long adjust) {}
};

// This is the only important method for the LoadImage. It returns bytes from
// the static array depending on the address range requested
void MyLoadImage::loadFill(uint1* ptr, int4 size, const Address& addr)
{
    uintb start = addr.getOffset();
    uintb max = baseaddr + (length - 1);
    for (int4 i = 0; i < size; ++i) { // For every byte requestes
        uintb curoff = start + i; // Calculate offset of byte
        if ((curoff < baseaddr) || (curoff > max)) { // If byte does not fall in window
            ptr[i] = 0; // return 0
            continue;
        }
        uintb diff = curoff - baseaddr;
        ptr[i] = data[(int4)diff]; // Otherwise return data from our window
    }
}

class AssemblyRaw : public AssemblyEmit {
public:
    virtual void dump(const Address& addr, const string& mnem, const string& body)
    {
        cout << ": " << mnem << ' ' << body << endl;
    }
};

static void dumpAssembly(MyLoadImage loader, Translate& trans)
{
    AssemblyRaw emit;

    Address addr(trans.getDefaultCodeSpace(), loader.getBaseAddress());
    Address lastaddr(trans.getDefaultCodeSpace(), loader.getLastAddress());

    while (addr < lastaddr) {
        uint1 buf[64];

        int4 length = trans.instructionLength(addr);
        assert(length < sizeof(buf));

        loader.loadFill(buf, length, addr);

        addr.printRaw(cout);
        cout << "[" << setfill('0') << setw(2) << hex << (int)buf[0] << "]";

        addr = addr + trans.printAssembly(emit, addr);
    }
}

int main(int argc, char** argv)
{
    char buf[4096];
    cin.read(buf, sizeof(buf));

    if (cin) {
        std::cerr << "File passed on stdin too big" << std::endl;
        return 2;
    }
    int len = cin.gcount();

    // Set up the loadimage
    MyLoadImage loader((uint1*)buf, len);

    // Set up the context object
    ContextInternal context;

    // Set up the assembler/pcode-translator
    string sleighFileName = "data/languages/fr.sla";
    Sleigh trans(&loader, &context);

    // Read sleigh file into DOM
    DocumentStorage docStorage;
    Element* sleighRoot = docStorage.openDocument(sleighFileName)->getRoot();
    docStorage.registerTag(sleighRoot);
    trans.initialize(docStorage);

    dumpAssembly(loader, trans);
    return 0;
}
