import pandas as pd
import os
from dotenv import load_dotenv
from difflib import get_close_matches

load_dotenv()

# Detect optional Google Gemini support
genai_available = False
genai_err = None
try:
    import google.generativeai as genai
    genai_available = True
except Exception as e:
    genai_available = False
    genai_err = str(e)


def map_user_terms_to_columns(question, df):
    question_lower = question.lower()
    columns = list(df.columns)
    column_map = {}

    for col in columns:
        col_lower = col.lower()

        # Direct substring match
        if col_lower in question_lower:
            column_map[col] = col
            continue

        # Check if any word in column appears in question
        col_words = col_lower.replace("_", " ").split()
        for word in col_words:
            if word in question_lower:
                column_map[col] = col
                break

        # Fuzzy match (80%+ similarity)
        if col not in column_map:
            matches = get_close_matches(col_lower, [question_lower], cutoff=0.8)
            if matches:
                column_map[col] = col

    return list(column_map.values())


def explain_result_human(result):
    """Return a human-friendly explanation for `result`.

    If Gemini is available, use it; otherwise provide a concise fallback.
    """
    if genai_available:
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel("gemini-2.5-flash")
            if isinstance(result, pd.DataFrame):
                result_str = result.head(10).to_dict()
            else:
                result_str = str(result)

            prompt = f"""
Explain the following data/result in simple language and give actionable advice if relevant:

{result_str}

Keep the answer short, structured, and highlight key points.
"""
            return model.generate_content(prompt).text
        except Exception:
            pass

    # Fallback (no AI): brief summary
    if isinstance(result, pd.DataFrame):
        return (
            f"Returned DataFrame with {len(result)} rows and columns {list(result.columns)}. "
            f"Sample (up to 3 rows): {result.head(3).to_dict()}"
        )
    return str(result)


def ask_pandas_agent(question):
    """Generate a pandas query (via Gemini) and execute it against the dataset.

    This function is defensive:
    - loads `data/merged_predictions.csv` lazily
    - returns helpful error messages when AI or data is unavailable
    """
    # Load dataset lazily
    try:
        df = pd.read_csv("data/merged_predictions.csv")
    except Exception as e:
        return {
            "query": None,
            "result": None,
            "explanation": None,
            "error": f"Could not load data/merged_predictions.csv: {e}"
        }

    matched_cols = map_user_terms_to_columns(question, df)

    system_prompt = f"""
You are an AI that converts natural language questions into valid pandas code.
Use ONLY this dataframe named `df`.

df columns: {list(df.columns)}

Relevant columns detected from the user question: {matched_cols}

Rules:
- Return ONLY python code (no backticks)
- Assign the final output to a variable named 'result'
- 'result' MUST be a DataFrame or convertible to DataFrame
- Do NOT modify df
- Do NOT use imports, os, eval, or unsafe operations
"""

    if not genai_available:
        return {
            "query": None,
            "result": None,
            "explanation": None,
            "error": (
                "AI model unavailable. Install and configure google-generativeai and set GEMINI_API_KEY. "
                f"Import error: {genai_err}"
            )
        }

    # Request Gemini to generate pandas code
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(question + "\n" + system_prompt)
        pandas_code = response.text.strip()
    except Exception as e:
        return {
            "query": None,
            "result": None,
            "explanation": None,
            "error": f"AI generation failed: {e}"
        }

    # Execute generated code safely (best-effort)
    local_vars = {"df": df}
    result = None
    error = None

    try:
        result = eval(pandas_code, {"df": df}, {})
        if not isinstance(result, pd.DataFrame):
            try:
                result = pd.DataFrame(result)
            except Exception:
                pass
    except Exception:
        try:
            exec(pandas_code, {}, local_vars)
            result = local_vars.get("result", None)
        except Exception as e:
            error = str(e)

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
import pandas as pd
import os
from dotenv import load_dotenv
from difflib import get_close_matches

load_dotenv()

genai_available = False
genai_err = None
try:
    import google.generativeai as genai
    genai_available = True
except Exception as e:
    genai_available = False
    genai_err = str(e)

df = pd.read_csv("data/merged_predictions.csv")



from difflib import get_close_matches

def map_user_terms_to_columns(question, df):
    question_lower = question.lower()
    columns = list(df.columns)
    column_map = {}

    for col in columns:
        col_lower = col.lower()

        # Direct substring match
        if col_lower in question_lower:
            column_map[col] = col
            continue

        # Check if any word in column appears in question
        col_words = col_lower.replace("_", " ").split()
        for word in col_words:
            if word in question_lower:
                column_map[col] = col
                break

        # Fuzzy match (80%+ similarity)
        if col not in column_map:
            matches = get_close_matches(col_lower, [question_lower], cutoff=0.8)
            if matches:
                column_map[col] = col

    return list(column_map.values())








def explain_result_human(result):
    """Convert pandas result to simple advice for the user"""
    if isinstance(result, pd.DataFrame):
        result_str = result.head(10).to_dict()  # limit to top 10 rows
    else:
        result_str = str(result)

    prompt = f"""
Explain the following data/result in simple language and give actionable advice if relevant:

{result_str}

Only provide actionable insights, avoid technical code explanations. and if possible at the bottom you can do advanced research in Rwanda analyze it's trade landmark and find different opportunities both locally and globally that can support the user 

and make sure in a creative way your answer is well structured so that the user can easily follow them and get insights from them

but also remember to summarize and highlight titles , since users follow well summarized content remember to summarize and highlight important key points.
"""
    explanation = MODEL.generate_content(prompt).text
    return explanation


def ask_pandas_agent(question):
    """AI → generate pandas code → execute → return result + human explanation"""

    
    matched_cols = map_user_terms_to_columns(question, df)

    system_prompt = f"""
    You are an AI that converts natural language questions into valid pandas code.
    Use ONLY this dataframe named `df`.

    df columns: {list(df.columns)}

    Relevant columns detected from the user question: {matched_cols}

    Mapping rules:
    - you must be analytical in matching column names , for example
    A user can ask i work in agriculture ,so find columns in {list(df.columns)} that are relevant to agriculture , like livestock and food stuffs , 
    or a user asks i work in minerals so you must check in the provided columns  {list(df.columns)} and first the relevant columns

    so you must first check what are the relevant columns in  {list(df.columns)}  can use to generate to generate relevant codes depending on df dataframe, and to arrive at you final result 
    first check relevant if you used relevant columns in mapping.

    Rules:
    - Return ONLY python code (no backticks)
    - Assign the final output to a variable named 'result'
    - 'result' MUST be a DataFrame or convertible to DataFrame
    - Do NOT modify df
    - Do NOT use imports, os, eval, or unsafe operations
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
                try:
                    df = pd.read_csv("data/merged_predictions.csv")
                except Exception as e:
                    return {
                        "query": None,
                        "result": None,
                        "explanation": None,
                        "error": f"Could not load data/merged_predictions.csv: {e}"
                    }
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

