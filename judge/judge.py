from automata.fa import dfa, nfa
from automata.pda import pda, npda


def run(machine, tests):
    type = machine['type']
    machine = machine[type.lower()]
    initial_state = machine['startState']
    transitions = machine['transitions']
    final_states = machine['acceptStates']

    states = set(transitions.keys()).union(*(state for out in transitions.values() for state in out.values()))

    input_symbols = set().union(*(transition.keys() for transition in transitions.values()))

    model_types = {
        'DFA': dfa.DFA,
        'NFA': nfa.NFA,
        'PDA': npda.NPDA
    }

    kwags = {
        'stack_symbols': set('#@'),
        'initial_stack_symbol': set()
    } if type == 'PDA' else {}


    model = model_types[type](
        states=states,
        input_symbols=input_symbols,
        initial_state=initial_state,
        final_states=set(final_states),
        transitions=transitions,
        **kwags
    )
    return [model.accepts_input(test[0]) for test in tests]

