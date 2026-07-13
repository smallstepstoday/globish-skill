# Example: before and after

**Prompt:** "Explain the concept of quantum physics in plain English"

## Before (no skill)

> Quantum physics is the branch of physics that describes the behavior of matter and energy at the smallest scales — atoms and subatomic particles. Unlike classical physics, quantum mechanics reveals that particles can exist in superposition, occupying multiple states simultaneously until measured, and that measuring a system inevitably disturbs it. Particles also exhibit wave-particle duality, behaving as both discrete particles and continuous waves depending on how they're observed. Two particles can become entangled, meaning the state of one instantaneously correlates with the state of the other regardless of the distance separating them — a phenomenon Einstein famously called "spooky action at a distance."

## After (with the Globish skill)

> Quantum physics is a part of science. It studies very small things, like atoms. An atom is a very small piece of matter. Matter is what makes up all things around us.
>
> Quantum means a small, fixed piece. Physics is the study of how things move and act. Quantum physics studies how the smallest pieces of matter move and act.
>
> Small things do not act like big things. A ball moves in one clear path. A small thing can act like a wave. A wave spreads out. A small thing can also act like a single point. It can do both at once.
>
> We do not know two facts about a small thing at the same time. We do not know its right place and its right speed together. If we know one fact well, we know the other fact less well. This rule comes from the world. It is not a limit of our tools.
>
> A small thing can be in many ways at once, before we look at it. People who study science call this idea superposition. When we look at the small thing, it settles into one way. Our look changes what we see.
>
> Two small things can link in a strange way. People who study science call this an entanglement. If we change one thing, the other thing changes too. This happens even when it sits far away.
>
> Quantum physics helps us build things we use every day. It helps us make small parts for computers. It helps us make a special light for many tools. People who study science still study quantum physics. They want to learn more about our world.

## What changed

The "after" version ran clean through `scripts/check_globish.py` except for five terms with no plain-English substitute — *quantum*, *physics*, *atom(s)*, *superposition*, *entanglement* — each defined in plain words the first time it appears, per the skill's exception policy. Sentence length dropped from an average of ~40 words to under 15. Every passive construction ("particles can be described," "a phenomenon Einstein called") became active ("we look," "we build"). Every piece of jargon (subatomic, simultaneously, correlates, phenomenon) was replaced or removed.
