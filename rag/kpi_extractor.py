import os
from types import SimpleNamespace

from dotenv import load_dotenv
from pydantic import BaseModel , Field , ConfigDict
from typing import Annotated


PrintedValue = Annotated[ str | None,
    Field(description="Number exactly as printed" )  ]

PrintedUnit = Annotated[ str | None,
    Field( description="Unit exactly as printed") ]

Page_Number = Annotated[ str | None,
    Field( description="Page No where the value appears")]

class KPI(BaseModel):
    value : PrintedValue
    unit : PrintedUnit
    page : Page_Number

class ESGMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    #alias: what the field is called in the JSON.
    #ConfigDict: rules for the whole model. populate_by_name=True means accept the Python name too, not only the alias.

    scope1_emissions: Annotated[KPI, Field(alias="Scope 1 Emissions")]
    scope2_emissions: Annotated[KPI, Field(alias="Scope 2 Emissions")]
    total_energy: Annotated[KPI, Field(alias="Total Energy Consumed")]
    renewable_energy: Annotated[KPI, Field(alias="Energy from Renewable Sources")]
    water_consumption: Annotated[KPI, Field(alias="Water Consumption")]
    permanent_employees_total: Annotated[KPI, Field(alias="Permanent Employees Total")]
    permanent_employees_female: Annotated[KPI, Field(alias="Permanent Employees Female")]

class Retriever:
