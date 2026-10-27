"""Supplemental teaching calculations; amounts are millions of constant 2026 US dollars."""
import json
from pathlib import Path
r=.08;n=25;capital=2075;om=45;savings=200
annuity=(1-(1+r)**(-n))/r
central_eth=200*.70+1000*.35
supplier=central_eth*.35*.20*.55
regional=supplier+30+300*.35
no_ind_eth=200*.70
no_ind_supplier=no_ind_eth*.35*.20*.55
out={"annuity_factor":annuity,"annual_equivalent_cost":capital/annuity+om,"npv":(savings-om)*annuity-capital,"bcr":savings*annuity/(capital+om*annuity),"combined_capital_before_exclusions":2075+1000+300,"central_eth_gdp":central_eth,"central_other_gdp":regional,"central_combined_gdp":central_eth+regional,"private_industry_share":455/(central_eth+regional),"no_private_industry_eth":no_ind_eth,"no_private_industry_supplier":no_ind_supplier,"no_private_industry_other":no_ind_supplier+30,"no_private_industry_combined":no_ind_eth+no_ind_supplier+30,"zero_response_additional_gdp":0,"regional_diversion_stress":supplier-30,"same_consignment_extra_cost_dollars":-200+130+90,"delay_budget_dollars":200-130,"delay_threshold_days":(200-130)/35}
assert abs(out["npv"]+420.409693377)<.001
assert abs(out["no_private_industry_combined"]-175.39)<1e-9
p=Path(__file__).resolve().parent/"results/supplemental.json";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding="utf8");print(json.dumps(out,indent=2))
