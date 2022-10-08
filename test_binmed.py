import statistics as st
import numpy as np

from binmedian import output_binmed

### This needs to be worked on and refactored but quick sanity
### checks here to make sure it works...

test_list = [
    [np.random.randint(0, 100) for _ in range(101)],
    [1, 3, 5],
    [1, 3, 5, 7],  ##even n
    [1, 2, 3, 4, 5, 6],  ##even n
    [1, 2, 3, 4, 5, 6, 9],
    [2.25, 2.5, 2.5, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75],  ##even n
    [2.25, 2.5, 2.5, 2.75, 2.75, 2.75, 3.0, 3.0, 3.25, 3.5, 3.75],
    [220, 220, 240, 260, 260, 260, 260, 280, 280, 300, 320, 340],  ##even n
    [1, 2, 3, 4],  ##even n
    [12, 12, 4],
    [12, 2, 4],
]

for i in test_list:
    print(
        f"The answer given {output_binmed(i)}, this is {output_binmed(i)==st.median(i)}, should be {st.median(i)}"
    )
    assert output_binmed(i) == st.median(i)
