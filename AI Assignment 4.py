def isPredicate(obj):
    predicates = [on, on_table, clr, carry, empty_arm]
    for predicate in predicates:
        if isinstance(obj, predicate):
            return True
    return False

def isOperation(obj):
    operations = [stack, unstack, pick_up, put_down]
    for operation in operations:
        if isinstance(obj, operation):
            return True
    return False

class on():
    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
    def __str__(self):
        return "on({P},{Q})".format(P=self.P, Q=self.Q)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def __hash__(self):
        return hash(str(self))
    def take_action(self, world_state):
        return stack(self.P, self.Q)

class on_table():
    def __init__(self, P):
        self.P = P
    def __str__(self):
        return "on_table({P})".format(P=self.P)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def __hash__(self):
        return hash(str(self))
    def take_action(self, world_state):
        return put_down(self.P)

class clr():
    def __init__(self, P):
        self.P = P
    def __str__(self):
        return "clr({P})".format(P=self.P)
        self.P = P
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def __hash__(self):
        return hash(str(self))
    def take_action(self, world_state):
        for predicate in world_state:
            # If Block is on another block, unstack
            if isinstance(predicate, on) and predicate.Q == self.P:
                return unstack(predicate.P, predicate.Q)
        return None

class carry():
    def __init__(self, P):
        self.P = P
    def __str__(self):
        return "carry({P})".format(P=self.P)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def __hash__(self):
        return hash(str(self))
    def take_action(self, world_state):
        P = self.P
        # If block is on table, pick up
        if on_table(P) in world_state:
            return pick_up(P)
        # If block is on another block, unstack
        else:
            for predicate in world_state:
                if isinstance(predicate, on) and predicate.P == P:
                    return unstack(P, predicate.Q)

class empty_arm():
    def __init__(self):
        pass
    def __str__(self):
        return "empty_arm"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def __hash__(self):
        return hash(str(self))
    def take_action(self, world_state=[]):
        for predicate in world_state:
            if isinstance(predicate, carry):
                return put_down(predicate.P)
        return None

def arm_status(world_state):
    for predicate in world_state:
        if isinstance(predicate, carry):
            return predicate
    return empty_arm()

class stack():
    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
    def __str__(self):
        return "stack({P},{Q})".format(P=self.P, Q=self.Q)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def pre_condition(self):
        return [clr(self.Q), carry(self.P)]
    def delete(self):
        return [clr(self.Q), carry(self.P)]
    def add(self):
        return [empty_arm(), on(self.P, self.Q)]

class unstack():
    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
    def __str__(self):
        return "unstack({P},{Q})".format(P=self.P, Q=self.Q)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def pre_condition(self):
        return [empty_arm(), on(self.P, self.Q), clr(self.P)]
    def delete(self):
        return [empty_arm(), on(self.P, self.Q)]
    def add(self):
        return [clr(self.Q), carry(self.P)]

class pick_up():
    def __init__(self, P):
        self.P = P
    def __str__(self):
        return "pick_up({P})".format(P=self.P)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def pre_condition(self):
        return [clr(self.P), on_table(self.P), empty_arm()]
    def delete(self):
        return [empty_arm(), on_table(self.P)]
    def add(self):
        return [carry(self.P)]

class put_down():
    def __init__(self, P):
        self.P = P
    def __str__(self):
        return "put_down({P})".format(P=self.P)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, alter):
        return self.__dict__ == alter.__dict__ and self.__class__ == alter.__class__
    def pre_condition(self):
        return [carry(self.P)]
    def delete(self):
        return [carry(self.P)]
    def add(self):
        return [empty_arm(), on_table(self.P)]

class GoalStackPlanner:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    def get_steps(self):
        # Store Steps
        steps = []
        # Stack
        stack = []
        # World State
        world_state = self.initial_state.copy()
        # Push the goal_state onto the stack
        stack.append(self.goal_state.copy())
        # Loop until the stack is empty
        while len(stack) != 0:
            # Top of the stack
            stack_top = stack[-1]
            # If Stack Top is Compound Goal, push its unsatisfied goals onto stack
            if type(stack_top) is list:
                compound_goal = stack.pop()
                for goal in compound_goal:
                    if goal not in world_state:
                        stack.append(goal)
            # If Stack Top is an action
            elif isOperation(stack_top):
                operation = stack[-1]
                all_preconditions_satisfied = True
                # If any precondition is unsatisfied and push it onto program stack
                for predicate in operation.delete():
                    if predicate not in world_state:
                        all_preconditions_satisfied = False
                        stack.append(predicate)
                # If all preconditions are satisfied, pop operation from stack and execute it
                if all_preconditions_satisfied:
                    stack.pop()
                    steps.append(operation)
                    for predicate in operation.delete():
                        world_state.remove(predicate)
                    for predicate in operation.add():
                        world_state.append(predicate)
            # If Stack Top is a single satisfied goal
            elif stack_top in world_state:
                stack.pop()
            # If Stack Top is a single unsatisfied goal
            else:
                unsatisfied_goal = stack.pop()
                # Replace Unsatisfied Goal with an action that can complete it
                action = unsatisfied_goal.take_action(world_state)
                stack.append(action)
                # Push the Precondition on the stack
                for predicate in action.pre_condition():
                    if predicate not in world_state:
                        stack.append(predicate)
        return steps
initial_state = [on('Y', 'X'), on_table('X'), on_table('Z'), on_table('W'), clr('Y'), clr('Z'), clr('W'), empty_arm()]
goal_state = [on('X', 'Z'), on_table('Z'), on('W', 'Y'), on_table('Y'), clr('X'), clr('W'), empty_arm()]
goal_stack_planner = GoalStackPlanner(initial_state=initial_state, goal_state=goal_state)
steps = goal_stack_planner.get_steps()
print("The initial state is : \n")
print(initial_state)
print("\n\n")
print("The required goal state is : \n")
print(goal_state)
print("\n\n")
print("The steps are : \n")
print(steps)
print("\n\n")