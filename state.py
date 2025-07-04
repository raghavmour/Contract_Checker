from typing import TypedDict, Annotated
from operator import add
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.schema import Document


class ClauseComplianceResult(BaseModel):
    # clause_title: str = Field(
    #     ..., description="The title of the clause being evaluated."
    # )
    clause_text: str = Field(
        ..., description="The original clause text being evaluated."
    )
    policy_source: str = Field(
        ...,
        description="The source or identifier of the internal policy used for comparison.",
    )
    reason: str = Field(
        ...,
        description="Explanation of the compliance decision. keep this short and to the point",
    )
    compliant: bool = Field(
        ..., description="Whether the clause is compliant with internal policy."
    )
    clauses_internal: List[str] = Field(
        ...,
        description="List of clauses from the internal policies, each with its source formatted as: 'clause text — `source`'.",
    )
    # suggested_revision: Optional[str] = Field(
    #     None,
    #     description="Suggested revision if the clause is not compliant. keep this short and to the point",
    # )


class Clause(BaseModel):
    text: Optional[str] = Field(default=None, description="The raw clause text")
    clause_type: Optional[str] = Field(default=None, description="The type of clause")
    # metadata: Optional[dict] = Field(default=None, description="Optional metadata ")


class ExtractedClauses(BaseModel):
    clauses: List[Clause]


# class ExtractedClauses(BaseModel):
#     indemnification: Optional[List[Clause]] = Field(
#         default=None,
#         description="Requires one party to compensate the other for losses or damages arising from certain events, such as breach of contract, negligence, or third-party claims.",
#     )
#     warranties_and_representations: Optional[List[Clause]] = Field(
#         default=None,
#         description="Describes the vendor’s guarantees regarding the quality of goods or services, compliance with laws, and any other promises made during the negotiation of the agreement.",
#     )
#     dispute_resolution: Optional[List[Clause]] = Field(
#         default=None,
#         description="Outlines the process for resolving disputes, including whether arbitration, mediation, or litigation will be used, and the location where disputes will be resolved.",
#     )
#     governing_law_and_jurisdiction: Optional[List[Clause]] = Field(
#         default=None,
#         description="Defines the legal jurisdiction and law that will govern the agreement in case of legal disputes.",
#     )
#     subcontracting_and_assignment: Optional[List[Clause]] = Field(
#         default=None,
#         description="Defines whether the vendor can delegate its responsibilities to others or assign the agreement to another party.",
#     )
#     intellectual_property: Optional[List[Clause]] = Field(
#         default=None,
#         description="Specifies the ownership and use of intellectual property rights, including rights to any creations or inventions resulting from the agreement.",
#     )
#     limitation_of_liability: Optional[List[Clause]] = Field(
#         default=None,
#         description="Sets a cap on the amount of damages one party can claim from the other, often limiting liability to the amount paid under the contract.",
#     )
#     insurance: Optional[List[Clause]] = Field(
#         default=None,
#         description="Specifies the type of insurance the vendor is required to maintain during the term of the contract (e.g., general liability, professional indemnity).",
#     )
from typing import List
from pydantic import BaseModel, Field


# class ExtractedClauses(BaseModel):
#     indemnification: List[Clause] = Field(
#         default_factory=list,
#         description="Requires one party to compensate the other for losses or damages arising from certain events, such as breach of contract, negligence, or third-party claims.",
#     )
#     warranties_and_representations: List[Clause] = Field(
#         default_factory=list,
#         description="Describes the vendor’s guarantees regarding the quality of goods or services, compliance with laws, and any other promises made during the negotiation of the agreement.",
#     )
#     dispute_resolution: List[Clause] = Field(
#         default_factory=list,
#         description="Outlines the process for resolving disputes, including whether arbitration, mediation, or litigation will be used, and the location where disputes will be resolved.",
#     )
#     governing_law_and_jurisdiction: List[Clause] = Field(
#         default_factory=list,
#         description="Defines the legal jurisdiction and law that will govern the agreement in case of legal disputes.",
#     )
#     subcontracting_and_assignment: List[Clause] = Field(
#         default_factory=list,
#         description="Defines whether the vendor can delegate its responsibilities to others or assign the agreement to another party.",
#     )
#     intellectual_property: List[Clause] = Field(
#         default_factory=list,
#         description="Specifies the ownership and use of intellectual property rights, including rights to any creations or inventions resulting from the agreement.",
#     )
#     limitation_of_liability: List[Clause] = Field(
#         default_factory=list,
#         description="Sets a cap on the amount of damages one party can claim from the other, often limiting liability to the amount paid under the contract.",
#     )
#     insurance: List[Clause] = Field(
#         default_factory=list,
#         description="Specifies the type of insurance the vendor is required to maintain during the term of the contract (e.g., general liability, professional indemnity).",
#     )


class AgentState(TypedDict):
    contract: Annotated[List[str], add]
    extracted_clauses: Annotated[List[Clause], add]
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
