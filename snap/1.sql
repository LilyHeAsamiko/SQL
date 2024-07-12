CREATE INDEX "search_users_by_last_login" ON "users"("last_login_date");
select username from users indexed by search_users_by_last_login where last_login_date >= 2024-01-01;