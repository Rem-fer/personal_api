from fastapi import FastAPI
import sql_queries as sq
from account_data import get_balance_w_labels
from llm import generate_weekly_focus
from pydantic import BaseModel

app = FastAPI()

#----------OVERVIEW----------#

##Key metrics
@app.get("/spending")
def get_spend(time_period: str, acc_type: str):
    return sq.get_spending(time_period, acc_type)

@app.get("/deep_work")
def get_dw(time_period: str):
    return sq.get_dw_minutes(time_period)

@app.get("/meditation")
def get_days_meditated(time_period: str):
    return sq.get_days_meditated(time_period)

@app.get("/approaches")
def get_approaches(time_period: str):
    return sq.get_approaches(time_period)

@app.get("/focus")
def get_week_focus(year: int, week_num: int):
    return sq.get_week_focus(year, week_num)

# Submit metrics for review
# Need pydantic model for request that have body parameters. Others don't need it because params are in query
class SaveMetricsForReview(BaseModel):
    week: int
    year: int
    dw: int
    med: int
    approaches: int
    spending: float

@app.post("/metrics")
def save_metrics_for_review(request: SaveMetricsForReview ):
    sq.save_metrics_for_review(request.week, request.year, request.dw, request.med, request.approaches, request.spending)
    return {"message": "Metrics saved successfully"}

#--------------FINANCES-------------#

@app.get("/banking/balances")
def get_balances_with_labels():
    return get_balance_w_labels()

@app.get("/banking/need_review")
def need_review():
    return sq.need_review()
#-----------TRACKING----------#
@app.get("/meditation/streak")
def get_med_streak():
    return sq.current_med_streak()

@app.get("/meditation/dates")
def get_meditation_dates():
    return sq.get_meditation_dates()

@app.get("/deep_work/minutes")
def get_dw_minutes(time_period: str):
    return sq.get_dw_minutes(time_period)

@app.get("/deep_work/per_day")
def get_dw_per_day():
    return sq.get_dw_per_day()

#--------REVIEW FORM----------#

@app.get("/review/metrics")
def get_weekly_review_metrics(week: int, year: int):
    result = sq.get_weekly_review_metrics(week, year)
    if not result:
        return None
    dw, med, approaches, spending = result
    return {
        "dw": dw,
        "med": med,
        "approaches": approaches,
        "spending": spending
    }

@app.get("/review/review-exists")
def review_exists(week: int, year: int):
    return sq.review_exists(week, year)

@app.get("/review/submitted")
def review_text_submitted(week: int, year: int):
    return sq.review_text_submitted(week, year)

# Generate weekly focus
class GenerateWeeklyFocus(BaseModel):
    plus: str
    minus: str
    next_: str

@app.post("/generate-focus")
def generate_focus_route(request: GenerateWeeklyFocus):
    return generate_weekly_focus(request.plus, request.minus, request.next_)
#Save weekly focus

class SaveWeeklyReviewText(BaseModel):
    week: int
    year: int
    plus: str
    minus: str
    next_: str
    next_focus: str

@app.post("/review/save-text")
def save_weekly_review_text(request: SaveWeeklyReviewText):
    sq.save_weekly_review_text(
        request.week,
        request.year,
        request.plus,
        request.minus,
        request.next_,
        request.next_focus
    )
    return {"message": "Review text saved successfully"}