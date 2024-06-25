create table temp as select sentence as Sentence, id as ID from sentences;

update temp set "Sentence" == (select substr("sentence" , 98, 4) from sentences where id == 14) where ID == 14;

create view message as select * from temp where ID in [  14  114  618  630  932 2230 2346 3041];