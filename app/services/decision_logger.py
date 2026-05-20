from app.models.decision_log import SupervisorDecisionLog


def log_decision(
    db,
    request_id,
    policy_result,
    ranking_score,
    esg_score,
    approved
):

    log = SupervisorDecisionLog(
        request_id=request_id,
        policy_result=policy_result,
        ranking_score=ranking_score,
        esg_score=esg_score,
        approved=approved
    )

    db.add(log)
    db.commit()
