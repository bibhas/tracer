#define DOCTEST_CONFIG_IMPLEMENT
#include "doctest.h"

int program();

int main(int argc, char** argv) {
    doctest::Context context; // initialize

    // defaults
    context.addFilter("test-case-exclude", "*math*"); // exclude test cases with "math" in the name
    context.setOption("abort-after", 5); // stop test execution after 5 failed assertions
    context.setOption("sort", "name");   // sort the test cases by their name

    context.applyCommandLine(argc, argv);

    // overrides
    context.setOption("no-breaks", true); // don't break in the debugger when assertions fail

    int res = context.run(); // run queries, or run tests unless --no-run is specified

    if(context.shouldExit()) // important - query flags (and --exit) rely on the user doing this
        return res;          // propagate the result of the tests

    int client_stuff_return_code = program();
    // your program - if the testing framework is integrated in your production code

    return res + client_stuff_return_code; // the result from doctest is propagated here as well
}

#include <string>

TEST_CASE("[string] testing std::string") {
    std::string a("omg");
    CHECK(a == "omg");
}

TEST_CASE("[math] basic stuff") {
    CHECK(6 > 5);
    CHECK(6 > 7);
}

int program() {
    printf("Program code.\n");
    return EXIT_SUCCESS;
}
