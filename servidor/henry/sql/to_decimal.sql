alter table contenido_de_bodegas modify column cant decimal(23,3) not null;
alter table items_de_despacho modify column cantidad decimal(23,3) not null;
alter table items_de_venta modify column cantidad decimal(23,3) not null;
alter table ingreso_items modify column cantidad decimal(23,3) not null;
