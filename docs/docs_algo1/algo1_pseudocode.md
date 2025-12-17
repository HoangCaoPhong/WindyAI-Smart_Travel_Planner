Algorithm PlanRoute
Input:
    POIs dataset (≥ 1000 records)
    UserPreferences
    StartLocation
    TimeWindow (StartTime, EndTime)
    Budget

Variables:
    CurrentTime = StartTime
    CurrentLoc = StartLocation
    BudgetLeft = Budget
    Visited = {}
    Route = []

Loop:
    If no POI left OR CurrentTime > EndTime:
        break

    Candidates = []

    For each POI not in Visited:
        For each transport mode in {walking, motorbike, taxi}:
            (dist, travelTime, travelCost) = TravelInfo(CurrentLoc, POI)

            ArriveTime = CurrentTime + travelTime
            FinishTime = ArriveTime + POI.VisitDuration

            If ArriveTime < POI.OpenHour OR FinishTime > POI.CloseHour:
                continue

            If FinishTime > EndTime:
                continue

            If BudgetLeft < (POI.EntryFee + travelCost):
                continue

            Score = Evaluate(POI, travelTime, travelCost, UserPreferences)
            Add (POI, transportMode, Score, ArriveTime, FinishTime) to Candidates

    If Candidates empty:
        break

    best = Candidate with minimum Score

    Append best to Route
    Mark POI as Visited

    BudgetLeft -= (EntryFee + TravelCost)
    CurrentTime = best.FinishTime
    CurrentLoc = best.POI.Location

Output:
    Route
