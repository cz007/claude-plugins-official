# Business Rules — pricing

At extraction: 2 extracted rule cards (2 P0); later steps may add or correct rules below. Independent review is not established by this renderer; consult RULE_VALIDATION.json. Confidence is not business approval. 0 candidate rules were refuted and left out.

| ID | Name | Category | Priority | Source | Confidence |
|---|---|---|---|---|---|
| RULE-001 | Tiered price | Calculation | P0 | `pricing.py:5-8` | High |
| RULE-002 | Reject invalid quantity | Validation | P0 | `pricing.py:3-4` | High |

## Calculation

### RULE-001: Tiered price
**Category:** Calculation
**Priority:** P0
**Source:** `pricing.py:5-8`
**Plain English:** Quantities up to 10 cost 100 each; larger quantities cost 90 each.
**Specification:**
  Given a non-negative integer quantity
  When  a quote is requested
  Then  total equals quantity times 100 if quantity <= 10, otherwise times 90
**Parameters:** threshold=10; rates=100,90
**Edge cases handled:** 0; 10; 11
**Confidence:** High

## Validation

### RULE-002: Reject invalid quantity
**Category:** Validation
**Priority:** P0
**Source:** `pricing.py:3-4`
**Plain English:** Negative, boolean and non-integer quantities return an error.
**Specification:**
  Given a quantity input
  When  it is negative, boolean or not an integer
  Then  return error invalid quantity
**Edge cases handled:** -1; true; string
**Confidence:** High

## Rules requiring SME confirmation

No low-confidence cards were supplied. Business-owner confirmation and independent review remain separate requirements.
