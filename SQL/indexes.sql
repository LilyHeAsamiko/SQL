CREATE INDEX "search_course_id_by_student_id" ON "enrollments"("student_id");
select number,title,department,semester from cources where id == (select "course_id" indexed by search_course_id_by_student_id where student_id > 24999);
CREATE INDEX "search_requirements_id_by_course_id" ON "satisfies"("course_id");
select name from requirements where id in (select requirement_id from satisfies indexed by search_requirements_id_by_course_id where course_id > 1);