from typing import TypedDict, Annotated
from operator import add
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.schema import Document


class ClauseComplianceResult(BaseModel):
    clause_title: str = Field(
        ..., description="The title of the clause being evaluated."
    )
    clause_text: str = Field(
        ..., description="The original clause text being evaluated."
    )
    policy_source: str = Field(
        ...,
        description="The source or identifier of the internal policy used for comparison.",
    )
    reason: str = Field(
        ..., description="Explanation of the compliance decision. keep this short"
    )
    compliant: bool = Field(
        ..., description="Whether the clause is compliant with internal policy."
    )
    suggested_revision: Optional[str] = Field(
        None, description="Suggested revision if the clause is not compliant."
    )


class Clause(BaseModel):
    text: Optional[str] = Field(default=None, description="The raw clause text")
    clause_type: Optional[str] = Field(default=None, description="The type of clause")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata ")


class ExtractedClauses(BaseModel):
    clauses: List[Clause]


class AgentState(TypedDict):
    contract: str
    extracted_clauses: ExtractedClauses
    answer: Annotated[List[ClauseComplianceResult], add]


def retrieved_docs_reducer(a: List[Document], b: List[Document]) -> List[Document]:
    return a + b


class query(BaseModel):
    query: str = Field(
        description="A generated query for retrival from vectorstore according to the clause type and clause text"
    )


class SubState(TypedDict):
    clause: dict
    query: str
    retrived_docs: Annotated[List[Document], retrieved_docs_reducer]
    relevant_docs: Annotated[List[Document], retrieved_docs_reducer]
    answer: Annotated[List[ClauseComplianceResult], add]
