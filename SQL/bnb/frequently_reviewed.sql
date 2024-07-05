create view frequently_reviewed as select A.id as id,A.property_type as property_type,A.host_name as host_name , count(B.id) as reviews from listings A inner join reviews B on A.id == B.listing_id order by reviews DESC, property_type ASC,host_name ASC limit 100;