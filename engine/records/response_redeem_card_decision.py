from pydantic import BaseModel, ValidationInfo, field_validator


class ResponseRedeemCardDecision(BaseModel):
    redeem_decision: str

    @field_validator("redeem_decision")
    @classmethod
    def _check_redeem_decision(cls, v: str, info: ValidationInfo):

        if v not in ["yes", "no"]:
            raise ValueError(f"Invalid decision {v}.")
        
        return v