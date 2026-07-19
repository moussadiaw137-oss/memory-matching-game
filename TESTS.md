# Test Cases — Memory Matching Game

## Vanilla cases

| # | Test | Steps | Expected result |
|---|------|-------|------------------|
| V1 | Play a full 2-pair game | Choose 2 pairs, find both matches correctly | Board resolves, "You found all 2 pairs in X attempts!" is shown |
| V2 | A match is found | Pick two positions with the same value | "Match!" message, both cards stay revealed, score +1 |
| V3 | No match | Pick two positions with different values | "No match" message, both cards hidden again on next display |
| V4 | Play again | Finish a game, answer "y" | A new game starts (new board asked) |
| V5 | Stop after one game | Finish a game, answer "n" | "Thanks for playing!" is printed, program ends |

## Edge cases

| # | Test | Steps | Expected result |
|---|------|-------|------------------|
| E1 | Non-numeric number of pairs | Enter "abc" when asked how many pairs | Error message, re-asks the question |
| E2 | Number of pairs out of range | Enter "1" or "20" | Error message, re-asks (valid range: 2–8) |
| E3 | Non-numeric position | Enter "a" when picking a card | "Invalid input: please type a number.", re-asks |
| E4 | Position out of range | Enter "99" on a small board | "Invalid position...", re-asks |
| E5 | Same position picked twice in one turn | Pick position 3, then position 3 again | Rejected, re-asks for a different position |
| E6 | Re-picking an already-matched card | After a pair is matched, try to pick one of those positions again | Rejected — this was a real bug found during testing (the first version let matched cards be re-picked, which could silently re-score a pair); fixed by tracking `matched` separately from temporarily-shown cards |
| E7 | Negative number | Enter "-1" as a position | Rejected as out of range |

## How E6 was tested (regression test)
A scripted run with a forced board `['A','A','B','B']` and inputs
`["2","0","abc","1","0","2","2","3","n"]` confirmed:
- the "abc" typo is rejected (E3)
- the first pair matches correctly (V2)
- re-picking position 0 right after it was matched is rejected (E6)
- picking position 2 twice in the same turn is rejected (E5)
- the second pair still matches and the game ends correctly (V1)
