# Brief Report — GraphMind AI: A Web-Based AI Math Differentiator

**Course:** Educational Technology & AI  
**Topic:** Functions and Graphs (Grade 9)  
**Stack:** Python, Streamlit, Plotly, OpenAI Responses API (`gpt-5-mini`)  
**Author:** *[Write your own name here]*

## Aim and core task

The aim is to differentiate a single mathematical skill for diverse learners. Every student investigates a quadratic graph of the form **f(x) = ax² + bx + c**, identifies its vertex, and decides if it opens upward or downward. The tool changes the coefficients, context, scaffolding and feedback according to the selected level while retaining the same central learning objective.

## AI integration and prompt design

The application uses OpenAI through the Python backend. The generation prompt instructs the model to provide structured data (coefficients, a short title, task context, two progressive hints and a learning tip) for the selected learner level. Key prompt rules include **"Use simple A2-B1 English"**, **"Do not reveal the numerical vertex in the hints"**, and **"Return coefficients within the required difficulty range"**. When a student submits an answer, a separate prompt requests **1-3 sentences of supportive, level-matched feedback** grounded in the application's independently checked correctness flags. It must not reveal the answer before the student chooses Show solution.

## Three differentiation levels

**Foundation:** `f(x) = ±x² + c`; simple graph transformations, direct guidance and an accessible introduction to turning points. **Standard:** `f(x) = ax² + bx + c`, with a nonzero linear term; learners apply `x = −b/(2a)` and compute the vertex independently. **Advanced:** a quadratic projectile-height model `h(t) = at² + bt + c`; learners interpret the vertex as the maximum height and the corresponding time. All levels contain hints tailored to their demands.

## Interaction, reliability and evaluation

Students select a level, generate a fresh AI task, explore an interactive Plotly graph, enter the vertex coordinates and opening direction, receive instant marks and AI feedback, and reveal a step-by-step solution. To reduce mathematical errors, Python **checks AI-chosen coefficient ranges**, computes exact vertex coordinates using rational arithmetic, grades answers within a stated tolerance, and builds the graph. Automated offline tests cover exact vertices, difficulty bounds, answer checking and generation validation. **A live API/deployment test must be completed with the student's own key before submission.**

**Submission links (complete after deployment):** Website: _____________________  |  GitHub: _____________________
