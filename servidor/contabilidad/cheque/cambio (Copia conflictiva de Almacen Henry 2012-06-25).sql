CREATE TABLE cheque_cuenta (
    id integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nombre varchar(100) NOT NULL UNIQUE
)
;
alter table cheque_cheque change depositado_en_id  depositado_en_id integer ;
