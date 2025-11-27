import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
MODEL = genai.GenerativeModel("gemini-2.5-flash")

# Load dataset
df = pd.read_csv("data/merged_predictions.csv")

def explain_result_human(result):
    """Convert pandas result to simple advice for the user"""
    if isinstance(result, pd.DataFrame):
        result_str = result.head(10).to_dict()  # limit to top 10 rows
    else:
        result_str = str(result)

    prompt = f"""
Explain the following data/result in simple language so that the user can understand it, and give actionable advice if relevant:

{result_str}

Only provide actionable insights, avoid technical code explanations.
"""
    explanation = MODEL.generate_content(prompt).text
    return explanation


def ask_pandas_agent(question):
    """AI → generate pandas code → execute → return result + human explanation"""

    # 1. Prepare system prompt for AI
    system_prompt = f"""
You are an AI that converts natural language questions into valid pandas code.
Use ONLY this dataframe named `df`.

df columns: {list(df.columns)}

Rules:
- Return ONLY python code (no backticks)
- Code must produce a dataframe or scalar
- Do NOT use eval(), exec(), os, or imports
- Do NOT modify the dataframe
- The code can be single-line or multiple lines
- Assign the final output to a variable named 'result'
"""

    # 2. Ask AI to generate pandas code
    response = MODEL.generate_content(question + "\n" + system_prompt)
    pandas_code = response.text.strip()

    # 3. Try to execute code safely
    local_vars = {"df": df}
    result = None
    error = None

    # Try eval first (for single-line expressions)
    try:
        result = eval(pandas_code, {"df": df})
    except:
        # Fallback to exec for multi-line code
        try:
            exec(pandas_code, {}, local_vars)
            result = local_vars.get("result", None)
        except Exception as e:
            error = str(e)

    # 4. Explain result
    explanation = None
    if result is not None:
        explanation = explain_result_human(result)

    return {
        "query": pandas_code,
        "result": result,
        "explanation": explanation,
        "error": error
    }


if __name__ == "__main__":
    q = "I'm in minerals, what products should I invest in, and why?"
    out = ask_pandas_agent(q)
    
    print("Generated Query:\n", out.get("query"))
    if out.get("result") is not None:
        print("\nResult (sample):\n", out["result"].head(10) if isinstance(out["result"], pd.DataFrame) else out["result"])
        print("\n--- Human Explanation ---\n", out["explanation"])
    else:
        print("\nError:", out.get("error"))

