set NURSES ordered;
set SHIFTS ordered;
set DAYS ordered;

# Identify the last week
param last_week := card(DAYS) div 7;
set LAST_WEEK_DAYS := {d in DAYS: (ord(d) - 1) div 7 + 1 = last_week};

param N > 0 integer;
param J > 0 integer;
param K > 0 integer;

param demand {DAYS, SHIFTS};
param vacation {DAYS, NURSES};
param pref_comp {NURSES, NURSES};
param unpref_comp {NURSES, NURSES};
param workhours {NURSES};
param pref_shifts {NURSES, DAYS, SHIFTS};
param unpref_shifts {NURSES, DAYS, SHIFTS};
param last_shift {NURSES};

var x {NURSES, SHIFTS, DAYS} binary;
var z {NURSES, NURSES, SHIFTS, DAYS} binary;
var w1 {NURSES, DAYS} binary;
var w2 {NURSES, DAYS} binary;
var w3 {NURSES, DAYS} binary;

maximize happiness: (sum{i1 in NURSES, i2 in NURSES, j in SHIFTS, k in DAYS} (pref_comp[i1, i2] - unpref_comp[i1, i2])*z[i1, i2, j, k]) + (sum{i in NURSES, j in SHIFTS, k in DAYS} (pref_shifts[i, k, j] - unpref_shifts[i, k, j])*x[i, j, k]);

subject to enforce_vacation{i in NURSES, j in SHIFTS, k in DAYS}: vacation[k, i]*x[i, j, k] <= 0;
subject to employer_demand{j in SHIFTS, k in DAYS}: sum{i in NURSES} (1 - vacation[k, i])*x[i, j, k] >= demand[k, j];
subject to max_one_shift_a_day{i in NURSES, k in DAYS}: sum{j in SHIFTS} (1 - vacation[k, i])*x[i, j, k] <= 1;
subject to never_morning_after_night{i in NURSES, k in DAYS: ord(k) < K}: (1 - vacation[k, i])*x[i, member(J, SHIFTS), k] + (1 - vacation[next(k), i])*x[i, member(1, SHIFTS), next(k)] <= 1;
subject to max_working_hours{i in NURSES}: sum{j in SHIFTS, k in DAYS} x[i, j, k] <= workhours[i]*J/24;
subject to max_six_nights_a_week{i in NURSES, k in DAYS: ord(k) mod 7 = 1}: sum{l in ord(k)..(ord(k)+6)} x[i, member(J, SHIFTS), member(l, DAYS)] <= 6; 
subject to justice{i in NURSES}: -2 <= (sum{j in SHIFTS, k in DAYS: ord(k) mod 7 = 0 or ord(k) mod 7 = 6} x[i, j, k]) - (1/N)*(sum{tilde_i in NURSES, j in SHIFTS, k in DAYS: ord(k) mod 7 = 0 or ord(k) mod 7 = 6} x[tilde_i, j, k]) <= 2;
subject to z_conditions1{i1 in NURSES, i2 in NURSES, j in SHIFTS, k in DAYS}: z[i1, i2, j, k] <= x[i1, j, k];
subject to z_conditions2{i1 in NURSES, i2 in NURSES, j in SHIFTS, k in DAYS}: z[i1, i2, j, k] <= x[i2, j, k];
subject to z_conditions3{i1 in NURSES, i2 in NURSES, j in SHIFTS, k in DAYS}: z[i1, i2, j, k] >= x[i1, j, k] + x[i2, j, k] - 1;
subject to check_last_shift{i in NURSES}: last_shift[i] + x[i, 's1', 'd1'] <= 1;
subject to w1_condition1{i in NURSES, k in DAYS}: w1[i, k] >= 0;
subject to w1_condition2{i in NURSES, j in SHIFTS, k in DAYS}: w1[i, k] <= 1 - x[i, j, k];
subject to w1_condition3{i in NURSES, k in DAYS}: w1[i, k] >= (1 - x[i, 's1', k]) + (1 - x[i, 's2', k]) + (1 - x[i, 's3', k]) - 2;
subject to w2_condition1{i in NURSES, k in DAYS}: w2[i, k] >= 0;
subject to w2_condition2{i in NURSES, j in SHIFTS, k in DAYS: ord(j) > 1}: w2[i, k] <= 1 - x[i, j, k];
subject to w2_condition22{i in NURSES, k in DAYS: ord(k) < K}: w2[i, k] <= 1 - x[i, 's1', next(k)];
subject to w2_condition3{i in NURSES, k in DAYS: ord(k) < K}: w2[i, k] >= (1 - x[i, 's2', k]) + (1 - x[i, 's3', k]) + (1 - x[i, 's1', next(k)]) - 2;
subject to w3_condition1{i in NURSES, k in DAYS}: w3[i, k] >= 0;
subject to w3_condition2{i in NURSES, j in SHIFTS, k in DAYS: ord(j) < J and ord(k) < K}: w3[i, k] <= 1 - x[i, j, next(k)];
subject to w3_condition22{i in NURSES, k in DAYS}: w3[i, k] <= 1 - x[i, 's3', k];
subject to w3_condition3{i in NURSES, k in DAYS: ord(k) < K}: w3[i, k] >= (1 - x[i, 's3', k]) + (1 - x[i, 's1', next(k)]) + (1 - x[i, 's2', next(k)]) - 2;
subject to weekly_24h_vacation_except_last{i in NURSES, k in DAYS: ord(k) mod 7 = 1 and not (k in LAST_WEEK_DAYS)}:
        sum{l in ord(k)..(ord(k)+6)} (w1[i, member(l, DAYS)] + w2[i, member(l, DAYS)] + w3[i, member(l, DAYS)]) >= 1;
subject to weekly_24h_vacation_last{i in NURSES, k in DAYS: ord(k) mod 7 = 1 and (k in LAST_WEEK_DAYS)}:
        sum{l in ord(k)..(ord(k)+5)} (w1[i, member(l, DAYS)] + w2[i, member(l, DAYS)] + w3[i, member(l, DAYS)]) + w1[i, last(DAYS)] >= 1;
