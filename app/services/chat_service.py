"""Chat service for the investment advisor."""

import json
import re

from langchain_groq import ChatGroq

from app.config import settings
from app.graph import investment_graph

from app.services.mongodb_service import (
    create_chat_conversation,
    get_chat_conversation,
    save_chat_message,
    update_chat_title,
    save_portfolio,
)


llm = ChatGroq(
    model=settings.groq_model,
    temperature=0
)

intent_llm = ChatGroq(
    model=settings.groq_model,
    temperature=0
)


VALID_RISK_PROFILES = {
    "low",
    "moderate",
    "high"
}


def _extract_json(content: str) -> dict:
    """Extract JSON from an LLM response."""

    content = content.strip()

    # Remove markdown code fences.
    if content.startswith("```"):
        content = re.sub(
            r"^```(?:json)?\s*",
            "",
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r"\s*```$",
            "",
            content
        )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try extracting the first JSON object.
    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Unable to parse JSON from LLM response.")


def _normalise_risk_profile(value):
    """Normalize common risk profile descriptions."""

    if value is None:
        return None

    value = str(value).strip().lower()

    mappings = {
        "conservative": "low",
        "safe": "low",
        "low risk": "low",

        "balanced": "moderate",
        "medium": "moderate",
        "moderate risk": "moderate",
        "medium risk": "moderate",

        "aggressive": "high",
        "high risk": "high",
    }

    value = mappings.get(value, value)

    if value in VALID_RISK_PROFILES:
        return value

    return None


def _validate_changes(changes: dict) -> dict:
    """Validate and normalize portfolio changes."""

    result = {
        "investment_amount": None,
        "duration_years": None,
        "risk_profile": None,
        "investment_goal": None
    }

    amount = changes.get("investment_amount")

    if amount is not None:
        try:
            amount = float(amount)

            if amount >= 1000:
                result["investment_amount"] = amount
        except (TypeError, ValueError):
            pass

    duration = changes.get("duration_years")

    if duration is not None:
        try:
            duration = int(duration)

            if duration >= 1:
                result["duration_years"] = duration
        except (TypeError, ValueError):
            pass

    risk = _normalise_risk_profile(
        changes.get("risk_profile")
    )

    if risk:
        result["risk_profile"] = risk

    goal = changes.get("investment_goal")

    if goal:
        goal = str(goal).strip()

        if goal:
            result["investment_goal"] = goal

    return result


def detect_chat_intent(message: str) -> dict:
    """
    Determine whether a chat message is informational or requests
    a portfolio modification.
    """

    prompt = f"""
You are an intent classifier for an investment advisor.

Analyze the user's message.

User message:
{message}

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "intent": "informational",
    "changes": {{
        "investment_amount": null,
        "duration_years": null,
        "risk_profile": null,
        "investment_goal": null
    }}
}}

Rules:

1. Use "informational" when the user is asking a question,
   asking for an explanation, asking why something was recommended,
   asking about an asset, or requesting general investment information.

2. Use "modify_portfolio" when the user wants to change their
   current investment plan.

3. Extract an exact investment amount when requested.
   Example:
   "Increase my investment to 1 lakh"
   -> investment_amount: 100000

4. Extract the investment duration.
   Example:
   "Change my horizon to 10 years"
   -> duration_years: 10

5. Map risk descriptions:
   conservative -> low
   safe -> low
   balanced -> moderate
   medium -> moderate
   aggressive -> high

6. Only populate fields that the user actually wants to change.

7. Do not infer changes that the user did not request.

8. If the user asks a question about the existing portfolio,
   classify it as informational.

Return JSON only.
"""

    try:
        response = intent_llm.invoke(prompt)

        parsed = _extract_json(
            response.content
        )

        intent = parsed.get(
            "intent",
            "informational"
        )

        if intent not in {
            "informational",
            "modify_portfolio"
        }:
            intent = "informational"

        changes = _validate_changes(
            parsed.get("changes", {})
        )

        return {
            "intent": intent,
            "changes": changes
        }

    except Exception as exc:
        print(
            f"Chat intent detection failed: {exc}"
        )

        return {
            "intent": "informational",
            "changes": {
                "investment_amount": None,
                "duration_years": None,
                "risk_profile": None,
                "investment_goal": None
            }
        }


def _build_history_text(previous_messages):
    """Build recent conversation history for the LLM."""

    history_text = ""

    for item in previous_messages[-10:]:
        role = item.get("role", "user")
        content = item.get("content", "")

        history_text += (
            f"{role.upper()}: {content}\n"
        )

    return history_text


def _build_portfolio_text(portfolio):
    """Build readable portfolio context."""

    if not portfolio:
        return "No portfolio has been generated yet."

    return "\n".join(
        f"- {asset}: ₹{amount:,.2f}"
        for asset, amount in portfolio.items()
    )


def _run_updated_portfolio_workflow(
    investment_goal: str,
    investment_amount: float,
    duration_years: int,
    risk_profile: str | None = None
):
    """
    Run the existing LangGraph investment workflow using the
    updated investment inputs.
    """

    initial_state = {
        "user_goal": investment_goal,
        "investment_amount": investment_amount,
        "duration_years": duration_years,

        # Empty means risk profiler should calculate it.
        # A valid value means the user explicitly requested
        # that risk profile and risk_profiler will preserve it.
        "risk_profile": risk_profile or "",

        "research_data": {},
        "portfolio": {},
        "recommendations": [],
        "critique": "",
        "approved": False,
        "history": []
    }

    print("\n========== CHAT PORTFOLIO UPDATE ==========")
    print(f"Goal: {investment_goal}")
    print(f"Amount: ₹{investment_amount}")
    print(f"Duration: {duration_years} years")
    print(f"Risk: {risk_profile}")
    print("===========================================\n")

    result = investment_graph.invoke(
        initial_state
    )

    return result


def generate_chat_response(
    user_id: str,
    message: str,
    conversation_id: str | None,
    investment_goal: str | None,
    investment_amount: float | None,
    duration_years: int | None,
    risk_profile: str | None,
    portfolio: dict[str, float] | None,
):
    """
    Generate a chat response.

    Informational messages are answered using the current portfolio
    context.

    Portfolio modification messages trigger the existing LangGraph
    workflow with the updated investment inputs.
    """

    if not conversation_id:
        conversation_id = create_chat_conversation(
            user_id
        )

        if not conversation_id:
            raise RuntimeError(
                "Unable to create chat conversation."
            )

    conversation = get_chat_conversation(
        conversation_id,
        user_id
    )

    if not conversation:
        raise ValueError(
            "Chat conversation not found."
        )

    previous_messages = conversation.get(
        "messages",
        []
    )

    chat_intent = detect_chat_intent(
        message
    )

    print("\n========== CHAT INTENT ==========")
    print(
        f"Intent: {chat_intent['intent']}"
    )
    print(
        f"Changes: {chat_intent['changes']}"
    )
    print("=================================\n")

    changes = chat_intent["changes"]

    # ============================================================
    # PORTFOLIO MODIFICATION
    # ============================================================

    if chat_intent["intent"] == "modify_portfolio":

        # Use the requested value when present.
        # Otherwise preserve the current dashboard value.
        updated_goal = (
            changes["investment_goal"]
            or investment_goal
            or ""
        )

        updated_amount = (
            changes["investment_amount"]
            if changes["investment_amount"] is not None
            else investment_amount
        )

        updated_duration = (
            changes["duration_years"]
            if changes["duration_years"] is not None
            else duration_years
        )

        updated_risk = (
            changes["risk_profile"]
            if changes["risk_profile"] is not None
            else None
        )

        if not updated_goal:
            raise ValueError(
                "Investment goal is required to update the portfolio."
            )

        if updated_amount is None:
            raise ValueError(
                "Investment amount is required to update the portfolio."
            )

        if updated_duration is None:
            raise ValueError(
                "Investment duration is required to update the portfolio."
            )

        # Run the SAME graph used by /invest.
        result = _run_updated_portfolio_workflow(
            investment_goal=updated_goal,
            investment_amount=float(updated_amount),
            duration_years=int(updated_duration),
            risk_profile=updated_risk
        )

        updated_analysis = {
            "risk_profile": result["risk_profile"],
            "portfolio": result["portfolio"],
            "recommendations": result.get(
                "recommendations",
                []
            ),
            "critique": result.get(
                "critique",
                ""
            ),
            "workflow_history": result.get(
                "history",
                []
            ),

            # Include the actual inputs so Angular can
            # update its dashboard state.
            "investment_goal": updated_goal,
            "investment_amount": float(
                updated_amount
            ),
            "duration_years": int(
                updated_duration
            )
        }

        # Persist updated portfolio.
        save_portfolio({
            "goal": updated_goal,
            "amount": float(updated_amount),
            "duration": int(updated_duration),
            "risk_profile": result["risk_profile"],
            "portfolio": result["portfolio"],
            "critique": result.get(
                "critique",
                ""
            )
        })

        assistant_message = (
            "I've updated your investment plan based on your request. "
            f"Your investment amount is now "
            f"₹{float(updated_amount):,.0f} for "
            f"{int(updated_duration)} years, with a "
            f"{result['risk_profile']} risk profile. "
            "I've regenerated the portfolio using the full investment "
            "analysis workflow."
        )

        # Save conversation.
        save_chat_message(
            conversation_id,
            user_id,
            "user",
            message
        )

        save_chat_message(
            conversation_id,
            user_id,
            "assistant",
            assistant_message
        )

        if not previous_messages:
            title = message[:60].strip()

            if len(message) > 60:
                title += "..."

            update_chat_title(
                conversation_id,
                user_id,
                title
            )

        return (
            assistant_message,
            conversation_id,
            chat_intent,
            True,
            updated_analysis
        )

    # ============================================================
    # INFORMATIONAL CHAT
    # ============================================================

    history_text = _build_history_text(
        previous_messages
    )

    portfolio_text = _build_portfolio_text(
        portfolio
    )

    prompt = f"""
        You are an intelligent investment advisor.

        Answer the user's question using the current investment
        context and conversation history.

        You are NOT modifying the portfolio unless the request
        explicitly asks for a portfolio change.

        Current investment goal:
        {investment_goal or "Not provided"}

        Current investment amount:
        {
            f"₹{investment_amount:,.2f}"
            if investment_amount is not None
            else "Not provided"
        }

        Current investment duration:
        {duration_years or "Not provided"} years

        Current risk profile:
        {risk_profile or "Not provided"}

        Current portfolio:
        {portfolio_text}

        Conversation history:
        {history_text}

        User message:
        {message}

        Instructions:

        - Answer naturally and clearly.
        - Explain investment recommendations when asked.
        - Use the current portfolio as context.
        - Do not invent portfolio holdings.
        - Do not claim that a portfolio was changed.
        - If the user asks for general financial information,
        explain it clearly.
        - Keep the answer useful but reasonably concise.
        """

    response = llm.invoke(prompt)

    assistant_message = response.content

    save_chat_message(
        conversation_id,
        user_id,
        "user",
        message
    )

    save_chat_message(
        conversation_id,
        user_id,
        "assistant",
        assistant_message
    )

    if not previous_messages:
        title = message[:60].strip()

        if len(message) > 60:
            title += "..."

        update_chat_title(
            conversation_id,
            user_id,
            title
        )

    return (
        assistant_message,
        conversation_id,
        chat_intent,
        False,
        None
    )