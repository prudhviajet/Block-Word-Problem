# Block-Word-Problem
![image](https://user-images.githubusercontent.com/84682126/153914736-0b2f34ca-4815-4113-afb7-9151698f8c41.png)
<p>There is a table on which blocks can be placed, some may or may not be stacked on other blocks. We have an arm with which we can pick up or put down only one block at a time. our aim to change the configuration of the blocks from initial state to goal state.</p>
<p>Goal Stack Planning works backwards from the goal state to the initial state. We start at the goal start and try fulfilling the preconditions required to achieve the initial state. These preconditions may have their own preconditions. We make use of a stack to hold these goals that need to be fulfilled as well the actions that we need to perform.</p>
<p><b>Predicates:</b></p>
<p>Predicates are statements which help us convey the information about a configuration in blocks world.</p>
<p>List of predicates are:</p>
<ol>
  <li>on(A,B) -> Block A is on B</li>
  <li>on_table(A) -> A is on table</li>
  <li>clr(A) -> Nothing is on top of A</li>
  <li>carry(A) -> Arm is carrying A</li>
  <li>empty_arm -> Arm is carrying nothing</li>
</ol>
<p><b>Operations:</b></p>
<p>The arm can perform some movements to change the placement of blocks, these are called operations.</p>
<p>List of operations are:</p>
<ol>
  <li>stack(A,B) -> Stacking A on B</li>
  <li>un_stack(A,B) -> Picking up A which is on top of B</li>
  <li>pick_up(A) -> Picking up A which is on top of the table</li>
  <li>put_down(A) -> Put down A on the table</li>
</ol>
<p>all the four operations have certain precondition which needed to be satisfied to perform.</p>
<p>The effect of these operations is represented using two lists add(A) and delete(D). delete list contains predicates which will cease to be true once the operation is performed. add list contains predicates which will become true once the operation is performed.</p>
![image](https://user-images.githubusercontent.com/84682126/153916075-b8c04b81-fb9e-4dfa-85c7-f57b55221c59.png)
<p><b>Algorithm:</b></p>
<pre>
Push the Goal state in to the Stack
Push the individual Predicates of the Goal State into the Stack
Loop till the Stack is empty
          Pop an element E from the stack
          IF E is a Predicate
                    IF E is True then
                              Do Nothing
                    ELSE
                              Push the relevant action into the Stack
                              Push the individual predicates of the Precondition of the action into the Stack
          Else IF E is an Action
                    Apply the action to the current State.
                    Add the action ‘a’ to the plan
</pre>
<p><b>Explanation:</b></p>
<p>The Goal Stack Planning Algorithms works backwards from the goal state to the initial state. It starts by pushing the unsatisfied goals into the stack. Then it pushes the individual subgoals into the stack and its pops an element out of the stack. Based on the kind of element we are popping out from the stack a decision is to be made. If it is a Predicate, then compares it with the description of the current world state, if it is satisfied or is already present in our current situation then it’s true. If the Predicate is not true then we have to select and push relevant action satisfying the predicate to the Stack. After pushing the relevant action into the stack its precondition should be pushed into the stack. In order to apply an operation its precondition has to be satisfied. For that, the preconditions are pushed into the stack once after an action is pushed.</p>
