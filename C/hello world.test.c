#include <assert.h>

int main() {
    int* p;

    // Test case 1: create an array of size 5 with initial value 0
    p = create_array(5, 0);
    for (int i = 0; i < 5; i++) {
        assert(p[i] == 0);
    }
    free(p);

    // Test case 2: create an array of size 3 with initial value 1
    p = create_array(3, 1);
    for (int i = 0; i < 3; i++) {
        assert(p[i] == 1);
    }
    free(p);

    // Test case 3: create an array of size 1 with initial value -1
    p = create_array(1, -1);
    assert(p[0] == -1);
    free(p);

    // Test case 4: create an array of size 0 with initial value 0
    p = create_array(0, 0);
    assert(p == NULL);

    return 0;
}