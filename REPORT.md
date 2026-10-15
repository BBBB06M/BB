# GraphMind AI — Brief Report (Draft, 1 page)

**Topic:** Functions & Graphs, Grade 9  
**Technology:** Python, Streamlit, Plotly, Google Gemini API  
**Student:** [Your name]

## Learning objective

The application helps learners analyse a quadratic function f(x)=ax²+bx+c by identifying the vertex and explaining whether its graph opens up or down. A common learning objective is adapted to three levels while the learner uses one interactive interface.

## AI prompts and integration

Google Gemini receives a system prompt describing a Grade 9 mathematics tutor using clear A2–B1 English. It is required to return a structured task with coefficients a, b, c; short context; two progressive hints; and a learning tip. Prompts require level-specific complexity and forbid revealing the numerical vertex in the hints. A second prompt requests a short supportive explanation based on answers independently graded by Python. Gemini's key is stored privately in Streamlit Secrets.

## Differentiation

**Foundation:** f(x)=±x²+c, direct scaffolding and simple visual translation. **Standard:** nonzero x term and the formula x=-b/(2a). **Advanced:** h(t)=at²+bt+c with a real-life ball-flight model, where the vertex describes maximum height and time. Each level presents a new context, gradual hints, interactive graph, answer entry and feedback.

## Reliability and testing

Gemini supplies problem language and parameters, but Python validates the coefficient ranges, calculates the exact vertex using fractions and grades student responses. The application also offers a labelled rule-based Demo mode when the API is unavailable; Demo mode is not claimed to be AI. Before submission the deployed Gemini connection and all three levels must be tested with a real key, and outputs should be reviewed by the student.

**Website:** https://graphmind-ai-bbbb06m.streamlit.app  
**Code:** https://github.com/BBBB06M/BB
