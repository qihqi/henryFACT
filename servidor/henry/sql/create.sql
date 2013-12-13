alter table productos ENGINE=InnoDB;
alter table bodegas ENGINE=InnoDB;
alter table contenido_de_bodegas ENGINE=InnoDB;
alter table ingresos ENGINE=InnoDB;
alter table clientes ENGINE=InnoDB;
alter table usuarios ENGINE=InnoDB;
alter table ingreso_items ENGINE=InnoDB;
alter table notas_de_venta ENGINE=InnoDB;
alter table ordenes_de_despacho ENGINE=InnoDB;
alter table items_de_despacho ENGINE=InnoDB;
alter table items_de_venta ENGINE=InnoDB;
alter table transformas ENGINE=InnoDB;
alter table ingreso_detalle ENGINE=InnoDB;
alter table bodegas_externas ENGINE=InnoDB;

/*insert the dbuser*/
create user 'henry'@'%' identified by password '*7153FBECE00BBF8BEE80D1D055DEC0F2984B285A';
grant all privileges on henry.* to 'henry'@'%';

/*insert el cliente consumidor final*/
insert into clientes(codigo, apellidos, nombres, cliente_desde) 
    values ('NA', 'Consumidor Final', '', curdate());

insert into bodegas(id, nombre) values (-1, 'Ninguno');
insert into categorias(nombre) values ('FLORES'), ('BISUTERIA');
/*insert config descuentos */
insert into descuentos(param, value) values ('global', 0), ('descuento desde', null);



