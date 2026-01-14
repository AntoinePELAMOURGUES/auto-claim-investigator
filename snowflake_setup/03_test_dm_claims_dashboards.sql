SELECT
    responsibility_category,
    COUNT(*) as nombre_dossiers,
    SUM(damage_amount) as cout_total
FROM INSURANCE_DB.CLAIMS.DM_CLAIMS_DASHBOARD
GROUP BY responsibility_category;