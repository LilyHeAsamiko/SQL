CREATE INDEX "search_expire_time_by_id" ON "messages"("id");
select expires_timestamp from messages indexed by "search_expire_time_by_id" where id = 151;