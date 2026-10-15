"""GraphMind AI - differentiated interactive lessons on quadratic graphs.

Run: streamlit run app.py
Required secret: OPENAI_API_KEY in .streamlit/secrets.toml or environment.
"""
import os

import plotly.graph_objects as go
import streamlit as st

from ai_engine import DEFAULT_MODEL, client_for, feedback_for_answer, generate_exercise
from demo_engine import generate_demo_exercise, demo_feedback
from math_engine import check_answer, fraction_label, terms, verified_steps


st.set_page_config(
    page_title="GraphMind AI | Functions & Graphs",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root { --primary: #325ae7; }
.stApp { background: #f7f9fe; }
.block-container { max-width: 1250px; padding-top: 1.55rem; padding-bottom: 4rem; }
h1, h2, h3, p { letter-spacing: -0.012em; }
.hero {
  padding: 30px 34px; border-radius: 22px;
  background: linear-gradient(115deg, #14254e 5%, #263ba5 70%, #5069e6 100%);
  color: white; box-shadow: 0 16px 34px rgba(27,45,126,.11); margin-bottom: 25px;
}
.hero .eyebrow { color: #c3d5ff; font-size: 0.82rem; letter-spacing: 0.11em; font-weight: 700; }
.hero .main-title { font-size: 2.32rem; line-height: 1.17; font-weight: 800; margin: 10px 0 8px; }
.hero .subtitle { color: #e0e8ff; font-size: 1.02rem; max-width: 760px; }
.level-chip { display:inline-block; background: #e8ecff; color:#293eb8; border-radius:10px;
   padding:5px 11px; font-weight:700; font-size:0.85rem; margin:0 0 10px; }
.small-muted { color: #62718b; font-size: 0.9rem; }
.concept-card { padding: 19px 22px; border: 1px solid #e4e9f4; border-radius: 16px;
  background: #fff; margin-top: 10px; }
[data-testid="stSidebar"] {background: #fff; border-right: 1px solid #e4e9f4; }
div[data-testid="stMetric"] {border: 1px solid #e5eaf4; background: white; padding: 14px;
  border-radius: 13px; }
div[data-testid="stVerticalBlockBorderWrapper"] {border-color:#e3eaf6;}
@media (max-width: 700px) {
 .hero { padding: 22px; }
 .hero .main-title { font-size: 1.75rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


def get_secret(name: str, default: str = "") -> str:
    """Don't crash when there is no local secrets.toml file yet."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        # Streamlit may raise a custom error when no secrets file exists yet.
        value = ""
    return str(value or os.environ.get(name, default) or default)


def clear_activity() -> None:
    st.session_state.exercise = None
    st.session_state.hint_count = 0
    st.session_state.marking = None
    st.session_state.ai_feedback = ""
    st.session_state.show_solution = False


def figure_for(q, advanced: bool, reveal_vertex: bool):
    xv = float(q.vertex_x)
    if advanced:
        min_x, max_x = 0.0, max(6.0, 2.2 * xv + 1.0)
        x_label, y_label = "Time (seconds)", "Height (metres)"
    else:
        min_x, max_x = min(-5.0, xv - 4.3), max(5.0, xv + 4.3)
        x_label, y_label = "x", "f(x)"
    points = [min_x + (max_x - min_x) * i / 199 for i in range(200)]
    values = [float(q.evaluate(x)) for x in points]
    fig = go.Figure()
    fig.add_hline(y=0, line_color="#bac4d7", line_width=1)
    fig.add_vline(x=0, line_color="#bac4d7", line_width=1)
    fig.add_trace(go.Scatter(
        x=points, y=values, mode="lines", name="Parabola",
        line=dict(color="#435de2", width=4),
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>",
    ))
    if reveal_vertex:
        fig.add_trace(go.Scatter(
            x=[xv], y=[float(q.vertex_y)], mode="markers+text", name="Vertex",
            text=[f"({fraction_label(q.vertex_x)}, {fraction_label(q.vertex_y)})"],
            textposition="top center", marker=dict(size=13, color="#ea6855"),
        ))
        fig.add_vline(x=xv, line_dash="dot", line_color="#e2a79a")
    fig.update_layout(
        template="plotly_white", height=430, autosize=True,
        margin=dict(l=18, r=18, t=24, b=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fff",
        font=dict(family="Arial, sans-serif", color="#37466e"),
        showlegend=False, dragmode="pan",
        xaxis=dict(title=x_label, zeroline=False, gridcolor="#e9edf6"),
        yaxis=dict(title=y_label, zeroline=False, gridcolor="#e9edf6"),
    )
    return fig


for name, initial in (
    ("exercise", None), ("selected_level", "Foundation"), ("hint_count", 0),
    ("marking", None), ("ai_feedback", ""), ("show_solution", False),
    ("question_id", 0),
):
    if name not in st.session_state:
        st.session_state[name] = initial

api_key = get_secret("OPENAI_API_KEY")
# Placeholders are not valid API credentials.
if api_key and (not api_key.startswith("sk-") or "осында" in api_key or "your-" in api_key):
    api_key = ""
model = get_secret("OPENAI_MODEL", DEFAULT_MODEL)

with st.sidebar:
    st.markdown("### 📈 GraphMind AI")
    st.caption("Personalized mathematics practice")
    st.divider()
    st.markdown("**Course**")
    st.write("Grade 9 · Functions & Graphs")
    st.markdown("**Core learning goal**")
    st.write("Find the vertex and opening direction of a quadratic function.")
    st.divider()
    st.markdown("**How to learn**")
    st.write("① Pick a level")
    st.write("② Generate an AI exercise")
    st.write("③ Study the graph and solve")
    st.write("④ Use hints, check, and reflect")
    st.divider()
    if api_key:
        st.success("OpenAI connection configured")
    else:
        st.success("Demo mode active — no API key required")
        st.caption("Practice exercises are generated by Python rules, not AI. You can add OpenAI later.")
    if api_key:
        st.caption("Model: " + model)
        st.caption("AI requests may incur API charges.")

st.markdown(
    """
<div class="hero">
  <div class="eyebrow">INTERACTIVE • ADAPTIVE • VISUAL</div>
  <div class="main-title">Understand functions.<br>See the mathematics.</div>
  <div class="subtitle">Your AI graph tutor creates a new challenge at your level,
      gives helpful clues, and explains verified solutions step by step.</div>
</div>
""",
    unsafe_allow_html=True,
)

st.subheader("01 · Choose your learning level")
level = st.radio(
    "Difficulty", ["Foundation", "Standard", "Advanced"],
    key="selected_level", horizontal=True, label_visibility="collapsed",
)
if st.session_state.exercise and st.session_state.exercise.level != level:
    clear_activity()

level_description = {
    "Foundation": "Explore a shifted parabola. Simple coefficients and guided visual thinking.",
    "Standard": "Use the vertex formula with grade-level coefficients and a graph.",
    "Advanced": "Investigate a real-world height function. Explain its maximum and when it happens.",
}
st.caption(level_description[level])

left_button, right_button = st.columns([1, 2], vertical_alignment="center")
with left_button:
    generate = st.button("✨ Generate new problem", type="primary", use_container_width=True)
with right_button:
    if not api_key:
        st.info("🧮 Demo mode: new level-based practice problems, graph, hints and verified answers — no key needed.")
    else:
        st.caption("Every new problem is generated by OpenAI and checked against mathematical constraints.")

if generate:
    previous = None
    current = st.session_state.exercise
    if current and current.level == level:
        previous = (current.quadratic.a, current.quadratic.b, current.quadratic.c)
    try:
        with st.spinner("Creating a level-appropriate problem…"):
            new_exercise = generate_exercise(client_for(api_key), model, level, previous) if api_key else generate_demo_exercise(level, previous)
        clear_activity()
        st.session_state.exercise = new_exercise
        st.session_state.question_id += 1
    except Exception:
        st.error("We could not generate a problem. Please try again.")

exercise = st.session_state.exercise
if exercise is None:
    with st.container(border=True):
        st.markdown("### Your learning space is ready")
        st.write("Choose a difficulty and press **Generate new AI problem**. The system will create a task, two hints and a learning tip. The graph and final answer are computed by Python.")
        st.markdown("#### The one central task")
        st.latex(r"f(x)=ax^2+bx+c\qquad x_v=\frac{-b}{2a}")
        st.caption("The same skill is taught differently at the three difficulty levels.")
else:
    q = exercise.quadratic
    advanced = level == "Advanced"
    var = "t" if advanced else "x"
    st.divider()
    st.subheader("02 · Investigate your problem")
    mode_label = "AI-GENERATED" if api_key else "DEMO PRACTICE"
    st.markdown(f"<span class='level-chip'>{level.upper()} · {mode_label}</span>", unsafe_allow_html=True)
    st.markdown(f"### {exercise.title}")
    st.write(exercise.context)
    st.latex(("h(t)" if advanced else "f(x)") + "=" + terms(q.a, q.b, q.c, symbol=var))

    col_graph, col_work = st.columns([1.24, 1], gap="large")
    with col_graph:
        with st.container(border=True):
            st.markdown("#### Interactive function graph")
            st.plotly_chart(figure_for(q, advanced, st.session_state.show_solution), use_container_width=True, config={"displaylogo": False, "scrollZoom": False})
            st.caption("Explore the curve by hovering and panning. The vertex marker appears after Show solution.")
    with col_work:
        with st.container(border=True):
            st.markdown("#### 🧠 Your solution")
            st.write("Find the vertex **(x, y)** and tell which way the parabola opens.")
            st.caption("Enter decimal answers if needed (e.g. 1.5). Accuracy ±0.05 is accepted.")
            with st.form(f"answer_form_{st.session_state.question_id}"):
                x_answer = st.number_input("Vertex x-coordinate" if not advanced else "Time of maximum (seconds)", min_value=-100.0, max_value=100.0, value=0.0, step=0.5, format="%.2f")
                y_answer = st.number_input("Vertex y-coordinate" if not advanced else "Maximum height (metres)", min_value=-100.0, max_value=100.0, value=0.0, step=0.5, format="%.2f")
                direction_answer = st.radio("Parabola opens", ["Upward", "Downward"], horizontal=True)
                submit = st.form_submit_button("Check my answer", type="primary", use_container_width=True)
            if submit:
                marking = check_answer(q, x_answer, y_answer, direction_answer)
                st.session_state.marking = marking
                st.session_state.ai_feedback = ""
                if marking.all_correct:
                    st.success("3/3 correct! Excellent graph reasoning.")
                else:
                    st.warning(f"You got {marking.correct_count}/3 correct. Try a hint and improve your answer.")
                try:
                    with st.spinner("AI is preparing personalized feedback…"):
                        st.session_state.ai_feedback = feedback_for_answer(client_for(api_key), model, exercise, marking) if api_key else demo_feedback(marking, level)
                except Exception:
                    st.session_state.ai_feedback = "The automatic check works, but AI feedback is temporarily unavailable."
            if st.session_state.marking is not None:
                result = st.session_state.marking
                icons = lambda flag: "✅" if flag else "🔄"
                st.markdown(f"{icons(result.x_correct)} Vertex x  ·  {icons(result.y_correct)} Vertex y  ·  {icons(result.direction_correct)} Direction")
                if st.session_state.ai_feedback:
                    st.info(("**AI feedback:** " if api_key else "**Practice feedback:** ") + st.session_state.ai_feedback)

    st.subheader("03 · Learn with support")
    hint_area, solution_area = st.columns(2, gap="large")
    with hint_area:
        with st.container(border=True):
            st.markdown("#### 💡 Helpful hints")
            st.write("Start with a small clue, then ask for a more direct method.")
            if st.button("Reveal next hint", disabled=st.session_state.hint_count >= 2, use_container_width=True):
                st.session_state.hint_count += 1
            for i in range(st.session_state.hint_count):
                st.info(f"**Hint {i + 1}:** {exercise.hints[i]}")
            if st.session_state.hint_count == 2:
                st.caption("You have used both hints. You can now show the full solution.")
            st.markdown("**Learning tip**")
            st.write(exercise.learning_tip)
    with solution_area:
        with st.container(border=True):
            st.markdown("#### ✅ Verified solution")
            st.write("The numbers below are computed using exact arithmetic — never copied from an AI guess.")
            if st.button("Show step-by-step solution", use_container_width=True):
                st.session_state.show_solution = True
            if st.session_state.show_solution:
                for index, step in enumerate(verified_steps(q, advanced), start=1):
                    st.markdown(f"**Step {index}.** {step}")
            else:
                st.caption("Try on your own before revealing the solution.")

st.divider()
with st.expander("For teachers · How differentiation works"):
    st.markdown(
        """
| Foundation | Standard | Advanced |
|---|---|---|
| Simple graph `±x²+c` | General quadratic `ax²+bx+c` | Projectile height `h(t)=at²+bt+c` |
| Simple language, direct visual hints | Vertex formula and independent calculation | Multi-step interpretation in time/metres |
| Identify shifts and direction | Find vertex and symmetry | Explain a real-world maximum |

**AI role:** the OpenAI API creates *new coefficients*, a contextual task, two personalized hints,
and an explanation tip at the chosen level. After an attempt, it also gives level-specific feedback.

**Mathematical reliability:** Python independently checks the chosen coefficient constraints,
plots the quadratic, computes the exact vertex with fractions, and grades answers. AI-generated
text must not be treated as an authoritative calculation.
"""
    )
st.caption("GraphMind AI · Educational Technology & AI · Demo mode uses Python rules; authentic AI requires OpenAI API access.")
