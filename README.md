# GraphMind AI — Grade 9 Functions & Graphs

Live site: https://graphmind-ai-bbbb06m.streamlit.app

An interactive Streamlit math differentiator with **Google Gemini AI**, optional OpenAI support and **API-free Demo mode**.

The same central skill is practised at three difficulties: identify the vertex of a quadratic function and its opening direction.

- **Foundation:** f(x) = ±x² + c, direct hints and simple transformations.
- **Standard:** f(x) = ax² + bx + c, use x = -b/(2a).
- **Advanced:** h(t) = at² + bt + c, interpret the ball's maximum height and its time.

Learners can generate new problems, interact with a Plotly graph, reveal two progressive hints, submit answers, receive differentiated feedback, and see a Python-verified solution.

## Enable Gemini AI

1. Visit https://aistudio.google.com/apikey and create a Gemini API key. A free tier may be available, subject to model, region, quota and account eligibility.
2. Open the app at https://share.streamlit.io, select your app, then **Settings → Secrets**.
3. Save private TOML values (do NOT put actual secrets in GitHub):

```toml
GEMINI_API_KEY = "paste-your-real-key-here"
GEMINI_MODEL = "gemini-2.5-flash-lite"
```

4. Reboot the app if prompted, and check that its sidebar says **Gemini AI is configured**.
5. Select a level and generate a new AI problem. Verify all three levels, hints and feedback.

**Provider choice:** Gemini takes priority when GEMINI_API_KEY is configured. If there is no Gemini key, OpenAI is used when OPENAI_API_KEY exists. Otherwise the app automatically works in labelled **Demo mode**. Demo uses Python rules, not AI, and does **not** satisfy the assignment's AI integration requirement.

Math answers, graph data and correctness checking are calculated independently in `math_engine.py` using exact fractions. AI writes the task context, coefficients, progressive hints and level-specific feedback. Generated coefficients are checked against curriculum limits before display.

## Local launch

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

For private local setup use `.streamlit/secrets.toml` (gitignored). Never commit keys. Cloud usage limits and billing are controlled by the provider, not by this application. For a publicly available app, be careful with quotas and permissions.

## Project structure

- `app.py`: Streamlit interactive application
- `gemini_engine.py`: Google Gemini API integration
- `ai_engine.py`: optional OpenAI API adapter and shared structured exercise schema
- `demo_engine.py`: offline non-AI fallback
- `math_engine.py`: verified quadratic functions and grading
- `.streamlit/config.toml`: theme settings
- `requirements.txt`: dependencies
- `REPORT.md`: assignment report draft (revise with your own name and verified findings)

This is an educational prototype; review AI-generated questions before classroom use. 
