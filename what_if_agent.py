import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import google.generativeai as genai
import time
import typing as t

# Load environment variables
load_dotenv()

# Set up the page configuration
st.set_page_config(
    page_title="What If Scenario Analyzer",
    page_icon="❓",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .stTextArea textarea {
        min-height: 150px !important;
    }
    .result-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #4e73df;
    }
</style>
""", unsafe_allow_html=True)

st.title("❓ What If Scenario Analyzer")
st.markdown("""
This AI agent helps you explore 'What If' scenarios by analyzing potential outcomes and implications.
Enter your scenario below and let the AI analyze it from multiple perspectives.
""")

########## Gemini LLM wrapper (direct Gemini API via google.generativeai) ##########

class GeminiLLM:
    """
    Minimal wrapper around google.generativeai to expose a simple synchronous .call(prompt, **kwargs)
    method which returns generated text. This attempts multiple genai call styles to be
    resilient to SDK differences.
    """
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", temperature: float = 0.7, max_output_tokens: int = 512):
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not provided")
        genai.configure(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def _extract_text_from_response(self, resp) -> str:
        """
        Attempt to pull a sensible text string from common Gemini SDK response shapes.
        You may need to adapt this if your installed SDK returns something different.
        """
        if resp is None:
            return ""
        # Try common shapes (best-effort)
        # 1) new-style: resp.output_text or resp.output or resp.candidates
        if hasattr(resp, "output_text"):
            return resp.output_text
        if isinstance(resp, dict):
            # common dict shapes
            # new chat responses: {'candidates': [{'content': [{'type':'output_text','text': '...'}]}], ...}
            if "candidates" in resp:
                cand = resp["candidates"]
                if isinstance(cand, list) and cand:
                    c0 = cand[0]
                    # candidate may have 'content' or 'text'
                    if isinstance(c0, dict):
                        if "content" in c0 and isinstance(c0["content"], list):
                            # find first output_text piece
                            for p in c0["content"]:
                                if isinstance(p, dict) and p.get("type") in ("output_text", "output"):
                                    txt = p.get("text") or p.get("payload") or ""
                                    if txt:
                                        return txt
                        if "text" in c0:
                            return c0["text"]
            # legacy: {'text': '...'}
            if "text" in resp and isinstance(resp["text"], str):
                return resp["text"]
            # new nested: {'output': [{'content': [{'text': '...'}]}]}
            if "output" in resp and isinstance(resp["output"], list) and resp["output"]:
                out0 = resp["output"][0]
                if isinstance(out0, dict) and "content" in out0 and isinstance(out0["content"], list):
                    for p in out0["content"]:
                        if isinstance(p, dict) and ("text" in p):
                            return p["text"]
        # 2) object with .output and .candidates attributes
        if hasattr(resp, "output") and isinstance(resp.output, list) and resp.output:
            first = resp.output[0]
            # try to find text inside
            if isinstance(first, dict) and "content" in first:
                for part in first["content"]:
                    if isinstance(part, dict) and "text" in part:
                        return part["text"]
        # 3) fallback to str()
        return str(resp)

    def call(self, prompt: str, temperature: t.Optional[float] = None, max_output_tokens: t.Optional[int] = None) -> str:
        """
        Generate text for the given prompt synchronously.
        Returns a plain string.
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_output_tokens if max_output_tokens is None else max_output_tokens

        # Try multiple likely SDK call patterns (best-effort compatibility)
        # 1) genai.generate(...)
        try:
            resp = genai.generate(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            text = self._extract_text_from_response(resp)
            if text:
                return text
        except Exception:
            # not all SDKs have genai.generate or it might throw for other reasons
            pass

        # 2) genai.chat.create(...) (chat-style API)
        try:
            resp = genai.chat.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            text = self._extract_text_from_response(resp)
            if text:
                return text
        except Exception:
            pass

        # 3) genai.text.generate(...) (another possible variant)
        try:
            resp = genai.text.generate(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            text = self._extract_text_from_response(resp)
            if text:
                return text
        except Exception:
            pass

        # 4) As a final fallback, raise an error with guidance
        raise RuntimeError(
            "Gemini call failed. The installed `google.generativeai` SDK may have a different API shape. "
            "Check SDK docs for correct call pattern (generate / chat.create / text.generate)."
        )

########## End wrapper ##########

def setup_llm():
    """Set up the Gemini LLM wrapper for CrewAI with optimized settings."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    # Optimized model settings for faster responses
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    return GeminiLLM(
        api_key=google_api_key,
        model=model_name,
        temperature=0.5,  # Lower temperature for more focused responses
        max_output_tokens=1000  # Increased for better response quality
    )

def setup_agents():
    """Set up the CrewAI agents for scenario analysis using Gemini via the wrapper."""
    llm = setup_llm()

    # CrewAI typically expects an llm-like object; many integrations call llm(...) or llm.call(...)
    # If your Crew version expects a different signature, adapt Agent(..., llm=...) accordingly.
    analyst = Agent(
        role='Senior Research Analyst',
        goal='Quickly analyze the given scenario and break it down into key components',
        backstory="""You are an experienced research analyst with expertise in rapid scenario analysis. 
        You excel at quickly identifying and communicating the most critical elements of any situation.""",
        verbose=False,  # Reduced verbosity for faster execution
        llm=llm,
        allow_delegation=False  # Disabled delegation for faster responses
    )

    strategist = Agent(
        role='Strategic Advisor',
        goal='Evaluate the potential outcomes and implications of the scenario',
        backstory="""You are a seasoned strategist who specializes in identifying potential 
        outcomes, risks, and opportunities in various scenarios. You think critically about 
        cause-and-effect relationships and long-term implications.""",
        verbose=True,
        llm=llm
    )

    advisor = Agent(
        role='Decision Advisor',
        goal='Provide actionable insights and recommendations based on the analysis',
        backstory="""You are a trusted advisor who helps decision-makers navigate complex 
        scenarios. You provide clear, practical recommendations based on thorough analysis 
        and strategic thinking.""",
        verbose=True,
        llm=llm
    )

    return analyst, strategist, advisor

def analyze_scenario(scenario_description: str):
    """Analyze the given scenario using CrewAI agents."""
    analyst, strategist, advisor = setup_agents()
    # Build tasks similarly to your original code
    analysis_task = Task(
        description=f"""Analyze the following scenario and break it down into its key components:
{scenario_description}

Provide a structured analysis including:
1. Key elements of the scenario
2. Main actors involved
3. Critical variables at play
4. Timeframe considerations""",
        agent=analyst,
        expected_output="A structured breakdown of the scenario's key components."
    )

    evaluation_task = Task(
        description="""Based on the analysis, evaluate the potential outcomes and implications.
Consider both positive and negative consequences, as well as any unexpected side effects.
Provide a balanced view of what could happen.""",
        agent=strategist,
        expected_output="A comprehensive evaluation of potential outcomes and implications.",
        context=[analysis_task]
    )

    recommendation_task = Task(
        description="""Based on the analysis and evaluation, provide actionable recommendations.
Consider different approaches and their potential effectiveness.
Include both short-term and long-term strategies.""",
        agent=advisor,
        expected_output="Clear, actionable recommendations for the given scenario.",
        context=[evaluation_task]
    )

    # Create and run the crew
    llm = setup_llm()  # pass the wrapper to the crew manager LLM if your Crew uses manager_llm
    crew = Crew(
        agents=[analyst, strategist, advisor],
        tasks=[analysis_task, evaluation_task, recommendation_task],
        verbose=False,  # Disabled verbose output for better performance
        process=Process.sequential,
        manager_llm=llm,
        function_calling_llm=llm
    )


    # Execute the tasks
    # NOTE: depending on your installed CrewAI version, kickoff() might return a complex object.
    # The following assumes kickoff() returns a plain text summary; adapt parsing if it's structured.
    result = crew.kickoff()
    # If result is an object, try to stringify sensibly:
    try:
        # if it's a dict-like object
        if isinstance(result, dict):
            # prefer 'text' or serialized form
            return result.get("text") or str(result)
        return str(result)
    except Exception:
        return str(result)

def main():
    # Sidebar for API key input
    with st.sidebar:
        st.header("Configuration")
        st.info("Using Gemini API key from .env file")
        if st.button("Reload API Key"):
            load_dotenv(override=True)
            st.rerun()

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application uses CrewAI to analyze 'What If' scenarios.
        It leverages multiple AI agents to provide comprehensive analysis
        and strategic insights using Google's Gemini models.
        """)

    if not os.getenv("GOOGLE_API_KEY"):
        st.error("🔑 GOOGLE_API_KEY not found. Please check your .env file and restart the application.")
        return

    with st.form("scenario_form"):
        scenario = st.text_area(
            "Describe your 'What If' scenario:",
            placeholder="E.g., What if renewable energy became 80% of global energy production by 2030?",
            height=150
        )

        submitted = st.form_submit_button("Analyze Scenario")

        if submitted and scenario:
            with st.spinner("🧠 Analyzing your scenario. This may take a minute..."):
                try:
                    result = analyze_scenario(scenario)
                    
                    # Display results in a clean, readable format
                    st.markdown("## Analysis Results")
                    
                    # Convert result to string if it's not already
                    result_str = str(result) if result else "No results returned"
                    
                    # Display the response in a clean container with proper formatting
                    st.markdown(
                        f"""
                        <div style="
                            max-height: 500px;
                            overflow-y: auto;
                            padding: 20px;
                            background-color: #ffffff;
                            border-radius: 8px;
                            border: 1px solid #e0e0e0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                            line-height: 1.6;
                            color: #333333;
                            font-size: 14px;
                        ">
                            {result_str}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.success("Analysis complete!")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please check your API key, model name and installed google.generativeai SDK version.")
        elif submitted and not scenario:
            st.warning("Please enter a scenario to analyze.")

if __name__ == "__main__":
    main()
