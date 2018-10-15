==== CS510 HW1 ====
    Author: Tom Rein
    Email: tr557@drexel.edu

==== Description ====
    This program implements various search algorithms to solve a sliding block puzzle

==== Directory Contents ====
    * search.py
        - source code for search algorithms

    * SBP-level0.txt
        - level used for random walks
        - the main function in search.py loads this file from the current directory

    * SBP-level1.txt
        - level used for testing search algoritms
        - the main function in search.py loads this file from the current directory

    * hw1.sh
        - a simple bash script that runs the program
        - It simply calls "python search.py"

    * output-hw1.txt
        - redirected output from "search.py" generated on tux

==== Usage Instructions ====

    1) To execute the program, simply type "./hw1.sh"

        This will simply run "python search.py"
        My main function loads both sliding block puzzles included in the directory

        Execute permissions should be granted on the bash script, but additional ways to invoke the program are as follows:
            - "bash hw1.sh"
            - "python search.py"
