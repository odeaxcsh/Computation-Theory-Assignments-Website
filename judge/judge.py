from automata.fa import dfa, nfa
from automata.pda import pda, npda


def run(machine, tests):
    print(machine)
    type = machine['type']
    machine = machine[type.lower()]
    initial_state = machine['startState']
    transitions = machine['transitions']
    final_states = machine['acceptStates']

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
        states=set(transitions.keys()),
        input_symbols={'A'},
        initial_state=initial_state,
        final_states=set(final_states),
        transitions=transitions,
        **kwags
    )
    return [model.accepts_input(test[0]) for test in tests]

