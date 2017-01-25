here's the format:

terms
* simple structure --- leaf | node [term]
* things we want to be able to do with terms
    - evaluate (given some interpretation of every symbol)
    - apply substitutions (given new terms and the symbols to be matching)
    - extract positions, update by positions, etc.
* ideally, immutable. subclass from tuples or something?
* how do the typical itertools compare?
    - filter, clearly
    - reduce is close to evaluate
    - enumerate, except with positions. requires fixed order, kinda hard to do
* trick is often that recursion should not always propagate (i.e., in subs)

substitution
* essentially a dictionary --- symbol -> term
* application is excatly what you'd expect

positions
* want a lexicographic order, which corresponds to the left-most position in a term
    - the above is actually wrong - it's what we'd expect in a left-first preorder traversal
* easy way to make, although they're effectively just a list
    - simple type, just --- root | int :: position

context
* term with a hole, easily made with a position or a predicate
* partially unwrapped term, getting ready to be reassembled
* type is actually second order --- term -> term

extra grammar
* like in all the text, we follow the normal conventions (adapted for ascii)
    - C is for a context
    - t, u, v, etc. are terms
    - p, q, etc. are positions
    - s is a substitution
* this guides the overloaded operators we'll use
    - C[t] puts term t into context C
    - t | p accesses the subterm at position p in t
    - t @ s applies the substitution s to term t
