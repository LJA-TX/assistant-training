# Plain-English Project Summary

This page is a plain-language guide for casual readers. It is not a governance or authority document. For the official current status, read [current_status.md](current_status.md).

## 1. What this project is

This project studies how AI models can learn to use outside tools more reliably.

A "tool" can mean something simple like a calculator, a search function, a calendar, or another software system that can do a specific job better than guessing in plain text.

The long-term goal is not just to make one model look good once. The larger goal is to build a reusable way to train and evaluate future models so their tool use can be measured, compared, and understood more honestly.

This public repository is a curated package, not a complete working archive. It shares the method, the evidence, and the main lessons, but not every internal step ever taken.

## 2. Why tool use matters

AI systems are more useful when they can do more than produce fluent text. If a model can pick the right tool, use it correctly, and avoid using a tool when it should not, it can be more helpful and less likely to make things up.

That sounds straightforward, but it is not. A model can appear strong in a controlled test and still make poor decisions in more realistic settings. Reliable tool use is not just about whether a model can format an answer correctly. It is also about judgment, restraint, and consistency.

## 3. What the first generation of work learned

"Gen-1" simply means the first major round of evidence-gathering work in this project.

Gen-1 showed that the project could produce strong tool-use behavior under some conditions. It also showed that those gains could come with important tradeoffs.

For example, a model might become better at making the right kind of tool request while also becoming worse at knowing when not to call a tool, or worse at other parts of safe and disciplined behavior.

Gen-1 also produced something valuable beyond scores: a bounded public package with baseline results, method documents, governance records, and historical evidence that explains how the project reached its current state.

## 4. Why scores alone are not enough

One of the clearest lessons from Gen-1 is that a strong score does not automatically mean a model will behave well in real use.

A model can do well in a narrow test but still behave differently when the situation changes. That means the project cannot stop at "the output looked right."

It also has to ask:

- What conditions produced that result?
- Would the same pattern hold in a different setting?
- Did the gain come with costs somewhere else?
- Is the result telling us something durable, or something narrow and fragile?

This is why the project treats comparison and interpretation as seriously as the raw scores themselves.

## 5. Why evidence capture matters

The project also learned that results are hard to trust if the surrounding evidence is missing.

It is not enough to save a final score or a final output. The project also needs to preserve the inputs, settings, and context that shaped that output, so later readers can understand what they are actually looking at.

In plain English, the goal is to avoid a situation where people can say "this looked impressive" but cannot reliably explain what produced it.

This does not mean the repository tries to store everything forever. It means the evidence that matters for interpretation has to be captured when the work happens, not guessed later from memory.

## 6. What Gen-2 means in plain English

"Gen-2" means the next evidence program that would build on what Gen-1 learned.

Gen-2 exists because the project now knows more about what strong tool-use behavior can look like, but it still does not fully understand why that behavior appears, how stable it is, or which tradeoffs come with it.

In plain terms, Gen-2 is about making strong tool-use behavior more understandable, more inspectable, more traceable, and more honestly bounded by the evidence.

Right now, Gen-2 exists in the repository as published framing and charter material. Those documents explain the intended direction, but they do not by themselves mean that new experiments or execution work are underway.

That means asking questions like:

- What seems to be driving the best tool-use behavior?
- Which good results are robust, and which depend on narrow conditions?
- What tradeoffs appear alongside stronger tool use?
- What evidence has to be captured from the start so later conclusions are trustworthy?

Some especially strong historical examples remain important reference points, but they are reference points only. They are not being treated as exact targets that must be recreated.

## 7. What this project is not

This project is not claiming that tool use is solved.

It is not claiming that any model in this repository is ready for deployment.

It is not only a search for one impressive result.

It is not a complete archive of every internal working note or every intermediate artifact.

It is not an announcement that new experiment execution is already underway in this public repository.

It is not an attempt to blur the line between evidence, explanation, and authorization.

## 8. Where to go next

If you want the official current status, read [current_status.md](current_status.md).

If you want the main entry point to the curated package, read [start_here.md](start_here.md).

If you want a summary of concrete outcomes, read [project_outcomes_to_date.md](project_outcomes_to_date.md).

If you want the current official Gen-2 framing, read [status/GEN2_PROGRAM_CHARTER.md](status/GEN2_PROGRAM_CHARTER.md).
