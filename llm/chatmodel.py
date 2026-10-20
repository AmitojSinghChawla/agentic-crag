import os
from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

import re
import json
import openai

def get_client() -> AzureOpenAI:

    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def get_structured_response(
        prompt: str ,
        response_model : type[BaseModel] ,
        model :str | None = None,
) -> BaseModel :

    model = model or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    client = get_client()

    DEFAULT_SYSTEM_PROMPT = """You are an expert in Environmental, Social, and Governance (ESG) analysis and corporate sustainability reporting, familiar with frameworks such as GRI, ISSB/SASB, TCFD, the GHG Protocol, and India's BRSR.

    Guidelines:
    - Base your answers only on the information provided in the user's message or context. Do not invent facts, figures, or sources.
    - If the provided information is insufficient to answer or to fill a field, say so or return null rather than guessing.
    - Be precise with numbers, units, and reporting periods, and keep distinct metrics separate.
    - Distinguish clearly between reported facts, targets or commitments, and your own analysis.
    - Be concise and objective.

    Always respond in the exact structure requested."""


    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format=response_model,
    )

    message = response.choices[0].message
    if message.refusal:
        raise RuntimeError(f"Model refused: {message.refusal}")

    return message.parsed

if __name__ == "__main__":
    from pydantic import Field

    class FinancialSnapshot(BaseModel):
        company_name: str
        fiscal_year: int
        revenue_crore: float = Field(description="Total revenue in INR crore")
        net_profit_crore: float = Field(description="Net profit in INR crore")
        scope1_emissions_tco2e: float | None = Field(
            default=None, description="Scope 1 GHG emissions in tCO2e, if mentioned"
        )
        key_risks: list[str]

    sample_text = """
    Extract the financial and ESG details from this annual report excerpt:

    Tata Steel Ltd reported consolidated revenue of ₹2,29,171 crore for FY2024,
    with net profit of ₹4,807 crore. Scope 1 emissions stood at 52.3 million tCO2e.
    Key risks highlighted include volatile raw material prices, carbon border
    taxes in the EU, and rising interest rates.
    """

    result = get_structured_response(sample_text, FinancialSnapshot)

    print("Type:", type(result).__name__)
    print(result.model_dump_json(indent=2))

    assert isinstance(result, FinancialSnapshot)
    assert result.fiscal_year == 2024
    assert result.revenue_crore > 0
    assert len(result.key_risks) >= 1
    print("\nAll checks passed.")