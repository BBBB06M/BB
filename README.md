# GraphMind AI — Functions & Graphs

An interactive **Grade 9 AI Math Differentiator** built using **Python + Streamlit + OpenAI API**.

## What the app does

Every learner studies **one core mathematical task**: analyze a quadratic graph and find its vertex and opening direction. OpenAI dynamically creates a problem appropriate to one of three difficulty levels:

| Level | Differentiation | Support |
|---|---|---|
| **Foundation** | `f(x) = ±x² + c` | Simple graph translations; direct, gradual hints |
| **Standard** | `f(x) = ax² + bx + c` | The vertex formula and grade-level independent solving |
| **Advanced** | `h(t) = at² + bt + c` | Real-world ball-height model: maximum height and time |

Students can generate a fresh task, explore an interactive Plotly graph, request two **AI-generated level-specific hints**, enter three answers, obtain automatic marking and AI feedback, and reveal a **verified step-by-step solution**.

**Important design decision:** The AI generates activities and guidance; Python checks coefficient bounds, computes the exact mathematical answer with `Fraction`, creates the graph, and grades students. This reduces the risk of unreliable model-produced mathematics.

## Repository contents

```text
GraphMind_AI/
  app.py                     # Streamlit UI and interactive graph
  ai_engine.py               # OpenAI generation + feedback
  math_engine.py             # Verified numerical logic
  requirements.txt           # Install dependencies
  .streamlit/config.toml     # Visual theme
  .streamlit/secrets.example.toml # Example ONLY, not a real key
  .gitignore                 # Protect private files
  tests/                     # Offline automated tests
  DEPLOY_KZ.md               # Detailed Kazakh deployment instructions
  REPORT.md                  # One-page report in English
```

## Run locally

1. Install **Python 3.11+**.
2. Download this repository and open a terminal in its folder.
3. Create an optional virtual environment: `python -m venv .venv` and activate it.
4. Install: `python -m pip install -r requirements.txt`.
5. Create a file called `.streamlit/secrets.toml` (**do not commit**):

   ```toml
   OPENAI_API_KEY = "your-private-key"
   OPENAI_MODEL = "gpt-5-mini"
   ```

6. Launch: `python -m streamlit run app.py`.
7. Open the local address Streamlit displays, usually `http://localhost:8501`.

## Publish to Streamlit Community Cloud

1. Upload **all project files except `.streamlit/secrets.toml`** to a **public GitHub repository**.
2. Go to <https://share.streamlit.io>, sign in with GitHub, then choose **Create app**.
3. Set repository/branch and entrypoint file `app.py`.
4. In **Advanced settings → Secrets**, paste your **real** key using the TOML layout above; the private secret is stored with Streamlit, not in GitHub.
5. Click **Deploy** and copy the resulting public `https://....streamlit.app` URL.
6. Check all three levels live, then submit the live URL, your GitHub link, and the report.

The hosting service can change its menus. For current setup, see <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy>.

## Automated tests

Install development test dependency `python -m pip install pytest` then run `python -m pytest -q`.
Tests do **not** need an API key and use fake responses instead of contacting OpenAI. Verify live API behavior yourself after adding a valid key.

## Privacy, safety and costs

- The **OpenAI API is billed separately** from ChatGPT subscriptions. You need valid API access/billing; requests are not guaranteed to be free.
- API keys must only live in local private secrets or Streamlit Cloud secrets; **never in GitHub**.
- A publicly accessible app using your server-side key may consume your account's API quota. Set an appropriate spend/usage limit in the OpenAI dashboard and monitor usage.
- Do not send pupils' names or personal data to the AI; this prototype sends only the exercise level, coefficients and correctness flags.
- The AI is a teaching tool: evaluate generated hints and mathematics with teacher review before classroom use.

## Academic originality

The assignment specifies original design, prompts and report. Before submission, review the code, try all levels, customize the explanations/layout as your own work, check mathematical correctness, and be ready to explain how you developed and verified the app. Do not misrepresent unaudited generated material as independently authored.

## References

- OpenAI Python Responses API: <https://developers.openai.com/api/reference/python>
- OpenAI Structured Outputs: <https://developers.openai.com/api/docs/guides/structured-outputs>
- Streamlit deployment: <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy>
- Streamlit secrets: <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management>
