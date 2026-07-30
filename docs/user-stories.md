# User Stories

25 user stories tracked as [GitHub Issues](https://github.com/Waterbottles792/PreMerge/issues)
(#3–#27) on the [PreMerge User Stories](https://github.com/Waterbottles792/PreMerge/projects)
board, one MoSCoW label each. See [MoSCoW.md](MoSCoW.md) for the underlying
requirement each story implements.

| # | Story | Priority |
|---|---|---|
| 3 | As Priya, I want to compare two branches for merge conflict risk so I know before merging whether my work overlaps with someone else's. | must-have |
| 4 | As Arjun, I want every branch pair analyzed automatically so I get a full risk picture without specifying pairs by hand. | must-have |
| 5 | As Priya, I want file-level overlap detection so I can see which files both branches touched. | must-have |
| 6 | As Arjun, I want line-level overlap detection so I can tell real conflicts from files that were merely both edited. | must-have |
| 7 | As Arjun, I want one combined risk score per branch pair so I can rank and sequence merges. | must-have |
| 8 | As Dr. Rao, I want historical file coupling calculated so hidden conflicts across related files are caught. | must-have |
| 9 | As Dr. Rao, I want coupling derived from real git commit history so the signal reflects how the team actually works. | must-have |
| 10 | As Dr. Rao, I want logically dependent files identified so conflicts hidden behind indirection still surface. | must-have |
| 11 | As Dr. Rao, I want coupling expressed as a Jaccard similarity score so the strength of the relationship is quantified, not just flagged. | must-have |
| 12 | As Meera, I want coupling results cached so repeat CI runs are fast. | should-have |
| 13 | As Priya, I want the risk report displayed in the terminal so I can read results without leaving my workflow. | must-have |
| 14 | As Arjun, I want plain-English explanations per risk pair so I can quote them directly in review. | should-have |
| 15 | As Meera, I want results exported as JSON so other tools and the GitHub Action can consume them. | should-have |
| 16 | As Arjun, I want branch pairs ranked by risk so I can sequence merges to minimize conflict pain. | must-have |
| 17 | As Arjun, I want high-risk conflicts visually highlighted so I don't have to hunt for the ones that matter. | should-have |
| 18 | As Dr. Rao, I want to configure the scoring weights so I can tune the model to our data. | should-have |
| 19 | As Dr. Rao, I want configuration loaded from a JSON file so weight changes don't require editing source code. | should-have |
| 20 | As Meera, I want to point PreMerge at a repository path so I can analyze repos other than the current directory. | should-have |
| 21 | As Meera, I want PreMerge to run as a GitHub Action so conflict risk is checked automatically on every PR. | must-have |
| 22 | As Arjun, I want the risk report posted as a PR comment so I see it where I make merge decisions. | must-have |
| 23 | As Arjun, I want the PR comment updated in place on new pushes so I don't get spammed with duplicate comments. | must-have |
| 24 | As Meera, I want analysis performance improved on large repos so PreMerge stays usable as history grows. | could-have |
| 25 | As Arjun, I want to compare every branch against `main` in one command so I get the merge-queue view. | should-have |
| 26 | As Priya, I want built-in CLI help so I can discover commands and options without reading external docs. | must-have |
| 27 | As Arjun, I want a comprehensive conflict report combining all signals so I have one place to review risk instead of piecing it together. | must-have |

**Summary:** 16 must-have, 8 should-have, 1 could-have.
