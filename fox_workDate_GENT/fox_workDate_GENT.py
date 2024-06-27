from datetime import date, timedelta

def list_of_workDate(start_str,end_str,rest_ls):
    start_date=date(int(start_str[0:4]),int(start_str[4:6]),int(start_str[6:8]))
    end_date=date(int(end_str[0:4]),int(end_str[4:6]),int(end_str[6:8]))
    delta = end_date-start_date
    workDate_without_holidays=[]
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        if day.weekday()<5 and str(day).replace("-","") not in rest_ls:
            workDate_without_holidays.append(str(day).replace("-",""))
    return workDate_without_holidays

def list_of_restDate():
    ls=[]
    with open('行事曆.txt','r') as f:
        ls=f.read().split('\n')
    return ls

if __name__ == "__main__":
    start = "20231225"
    end = "20250115"

    restDate_ls=list_of_restDate()
    print(restDate_ls)
    print("==========")
    workDate_ls=list_of_workDate(start,end,restDate_ls)
    print(workDate_ls)

