Volusia.parcel_schools
Nearest School Name and distance

---To know the school luc select luc, luc_desc, count(*) from volusia.parcel group by luc, luc_desc order by luc::integer

--- The school in the county have luc of 8300 select * from volusia.parcel where luc='8300' select count(*) from volusia.parcel where luc='8300'

--- School in parcel table select parid, geom from volusia.parcel where luc='8300';

--- Add the geometry column to the parcel table SELECT AddGeometryColumn ('volusia','parcel','geom',2236,'MULTIPOLYGON',2);

update volusia.parcel a set geom = p.geom from volusia.gis_parcels p where a.parid=p.altkey;

--- Make geometry into volusia.gis_schools
select parid, geom into volusia.gis_schools from volusia.parcel where luc='8300';

--- create Volusia.parcel_schools table and add the data from owner and parcel tables drop table if exists Volusia.parcel_schools ; select p.parid, p.luc,p.luc_desc,o.own1 as school_name into volusia.parcel_schools from volusia.owner o join volusia.parcel p on o.parid=p.parid where p.luc='8300';

---Add sch_typ column to the volusia.parcel_schools alter table volusia.parcel_schools add column sch_type char(20);

update volusia.parcel_schools set sch_type='Elementary' where school_name ilike '%elem%';

update volusia.parcel_schools set sch_type='Middle' where school_name ilike '%mid%';

update volusia.parcel_schools set sch_type='High' where school_name ilike '%High%';

select sch_type, count(*) from volusia.parcel_schools group by sch_type;

---Add school names into gis_schools alter table volusia.gis_schools add column s_name text;

update volusia.gis_schools g set s_name = s.school_name from volusia.parcel_schools s where g.parid=s.parid;

---The closest school to a random parcel and school name select p.parid, p.geom, s.school_name, ST_Distance(p.geom, (select p2.geom from volusia.parcel p2 where p2.parid=4841709))/5280 as school_dist
from volusia.parcel p join volusia.parcel_schools s on p.parid=s.parid where p.luc='8300' order by p.geom <-> (select p2.geom from volusia.parcel p2 where p2.parid=4841709) limit 1;

---Add scdistance column to the parcel table alter table volusia.parcel add column scdistance double precision;

---create index create index idx_parcel_luc on volusia.parcel (luc); create index idx_parcel on volusia.parcel (parid);

CREATE INDEX parcel_geom_idx ON volusia.parcel USING GIST (geom);

vacuum analyze volusia.parcel;

--Showing the school data in QGIS as a layer.
![image](https://user-images.githubusercontent.com/65051383/117502202-29967180-af4d-11eb-8fe3-d70966f037d8.png)



--- this asample of school table

![image](https://user-images.githubusercontent.com/65051383/117502253-3d41d800-af4d-11eb-9f4c-68a6b3d8aa60.png)


--this is sample of school distance

![image](https://user-images.githubusercontent.com/65051383/117502294-4cc12100-af4d-11eb-9edb-963ddad7a103.png)


The zipped file has two files the first one is parcel_schools.txt to download the file and create the parcel_schools table

the seconed one is scdistance (school distance)

load parcel_schools table (download zip file in repository, extract to c:\temp\cs540)

COPY volusia.parcel_schools from 'C:\temp\cs540\parcel_schools.txt' WITH (FORMAT 'csv', DELIMITER E'\t', NULL '', HEADER);

load scdistance (download zip file in repository, extract to c:\temp\cs540)

copy (select parid, scdistance from volusia.parcel where geom is not null ) to 'c:\temp\cs540\scdistance.txt' with (format 'csv',DELIMITER E'\t', NULL '',HEADER);

To konw more about Nearest School Name and to find the distance see the PDF
