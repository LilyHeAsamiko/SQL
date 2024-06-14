.separator "\t"
.import  E:\SQL\meteorites\dataprocessed.csv Meteorites
create table Meteorites_copy as select * from Meteorites;
update Meteorites_copy set "mass"= NULL where "mass" = "";
update Meteorites_copy set "year"= NULL where "year" = "";
update Meteorites_copy set "lat"= NULL where "lat" = "";
update Meteorites_copy set "long"= NULL where "long" = "";
update Meteorites_copy set "mass" = round("mass",2);
update Meteorites_copy set "lat" = round("lat",2);
update Meteorites_copy set "long" = round("long",2);
delete from Meteorites_copy where nametype is "Relict";
create table Meteorites_N as select * from Meteorites order by “year”, “name” asc;
update Meteorites_N set id = (select id from Meteorites);
