import pytest
from pydantic import ValidationError

from agentic.agents.states import create_dynamic_classifier_state


def test_create_dynamic_classifier_state():
    account_id = "cultpass"
    DynamicClassifier = create_dynamic_classifier_state(account_id)

    correct_instance = DynamicClassifier(
        is_ticket_classified_score=85.5,
        needs_info_about_previous_user_tickets=True,
        needs_info_about_reservations=False,
        tags=["billing", "access"],
    )

    with pytest.raises(ValidationError):
        DynamicClassifier(
            is_ticket_classified_score="not-a-number", # Should fail float validation
            needs_info_about_previous_user_tickets=True,
            needs_info_about_reservations=False,
            tags="not-a-list" # Should fail list validation
        )

    with pytest.raises(ValidationError):
        DynamicClassifier(
            is_ticket_classified_score="not-a-number", # Should fail float validation
            needs_info_about_previous_user_tickets=True,
            needs_info_about_reservations=False,
            tags=["nonexistent-tag"] # Should fail Literal validation
        )

    with pytest.raises(ValidationError):
        DynamicClassifier(
            is_ticket_classified_score="not-a-number", # Should fail float validation
            needs_info_about_previous_user_tickets=0.7,  # Should fail bool validation
            needs_info_about_reservations=0.5,  # Should fail bool validation
            tags="not-a-list" # Should fail list validation
        )
