BEGIN;
CREATE TABLE `clientes` (
    `codigo` varchar(20) NOT NULL PRIMARY KEY,
    `nombres` varchar(100) NOT NULL,
    `apellidos` varchar(100) NOT NULL,
    `direccion` varchar(300) NOT NULL,
    `ciudad` varchar(50) NOT NULL,
    `telefono` varchar(50) NOT NULL,
    `tipo` varchar(1) NOT NULL,
    `cliente_desde` date NOT NULL
)
;
COMMIT;
BEGIN;
CREATE TABLE `usuarios` (
    `username` varchar(50) NOT NULL PRIMARY KEY,
    `password` varchar(200) NOT NULL,
    `nivel` integer NOT NULL,
    `is_staff` bool NOT NULL,
    `last_factura` integer NOT NULL
)
;
COMMIT;
BEGIN;
CREATE TABLE `productos` (
    `codigo` varchar(20) NOT NULL PRIMARY KEY,
    `precio` numeric(20, 2) NOT NULL,
    `nombre` varchar(200) NOT NULL
)
;
CREATE TABLE `bodegas` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `nombre` varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE `contenido_de_bodegas` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `bodega_id` integer NOT NULL,
    `prod_id` varchar(20) NOT NULL,
    `cant` integer NOT NULL,
    UNIQUE (`bodega_id`, `prod_id`)
)
;
ALTER TABLE `contenido_de_bodegas` ADD CONSTRAINT `bodega_id_refs_id_aa960968` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);
ALTER TABLE `contenido_de_bodegas` ADD CONSTRAINT `prod_id_refs_codigo_eae75b66` FOREIGN KEY (`prod_id`) REFERENCES `productos` (`codigo`);
CREATE TABLE `ingresos` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fecha` date NOT NULL,
    `usuario_id` integer NOT NULL,
    `bodega_id` integer NOT NULL
)
;
ALTER TABLE `ingresos` ADD CONSTRAINT `bodega_id_refs_id_70d08783` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);
ALTER TABLE `ingresos` ADD CONSTRAINT `usuario_id_refs_id_f0cb4f78` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `ingreso_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ingreso_cod_id` integer NOT NULL,
    `num` integer NOT NULL,
    `producto_id` varchar(20) NOT NULL,
    `cantidad` integer NOT NULL,
    UNIQUE (`ingreso_cod_id`, `num`)
)
;
ALTER TABLE `ingreso_items` ADD CONSTRAINT `producto_id_refs_codigo_b03c5a7c` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`codigo`);
ALTER TABLE `ingreso_items` ADD CONSTRAINT `ingreso_cod_id_refs_id_867edf02` FOREIGN KEY (`ingreso_cod_id`) REFERENCES `ingresos` (`id`);
COMMIT;
BEGIN;
CREATE TABLE `notas_de_venta` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `vendedor_id` varchar(50) NOT NULL,
    `cliente_id` varchar(20) NOT NULL,
    `fecha` date NOT NULL,
    `bodega_id` integer NOT NULL,
    `precio_modificado` bool NOT NULL
)
;
ALTER TABLE `notas_de_venta` ADD CONSTRAINT `vendedor_id_refs_username_402d8104` FOREIGN KEY (`vendedor_id`) REFERENCES `usuarios` (`username`);
ALTER TABLE `notas_de_venta` ADD CONSTRAINT `cliente_id_refs_codigo_4e2fa716` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`codigo`);
ALTER TABLE `notas_de_venta` ADD CONSTRAINT `bodega_id_refs_id_4b3dc221` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);
CREATE TABLE `items_de_venta` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `venta_cod_id` integer NOT NULL,
    `num` integer NOT NULL,
    `producto_id` varchar(20) NOT NULL,
    `cantidad` integer NOT NULL,
    `nuevo_precio` numeric(20, 2),
    UNIQUE (`venta_cod_id`, `num`)
)
;
ALTER TABLE `items_de_venta` ADD CONSTRAINT `producto_id_refs_codigo_40ee3da` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`codigo`);
ALTER TABLE `items_de_venta` ADD CONSTRAINT `venta_cod_id_refs_id_6ebe96fe` FOREIGN KEY (`venta_cod_id`) REFERENCES `notas_de_venta` (`id`);
CREATE TABLE `ordenes_de_despacho` (
    `codigo` bigint NOT NULL PRIMARY KEY,
    `vendedor_id` varchar(50) NOT NULL,
    `cliente_id` varchar(20) NOT NULL,
    `fecha` date NOT NULL,
    `total` numeric(20, 2) NOT NULL,
    `bodega_id` integer NOT NULL,
    `pago` varchar(1) NOT NULL,
    `precio_modificado` bool NOT NULL
)
;
ALTER TABLE `ordenes_de_despacho` ADD CONSTRAINT `vendedor_id_refs_username_8bc60329` FOREIGN KEY (`vendedor_id`) REFERENCES `usuarios` (`username`);
ALTER TABLE `ordenes_de_despacho` ADD CONSTRAINT `cliente_id_refs_codigo_25e446f5` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`codigo`);
ALTER TABLE `ordenes_de_despacho` ADD CONSTRAINT `bodega_id_refs_id_519f595a` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);
CREATE TABLE `items_de_despacho` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `desp_cod_id` bigint NOT NULL,
    `num` integer NOT NULL,
    `producto_id` varchar(20) NOT NULL,
    `cantidad` integer NOT NULL,
    `precio` numeric(20, 2) NOT NULL,
    `precio_modificado` bool NOT NULL,
    UNIQUE (`desp_cod_id`, `num`)
)
;
ALTER TABLE `items_de_despacho` ADD CONSTRAINT `desp_cod_id_refs_codigo_c7fa0011` FOREIGN KEY (`desp_cod_id`) REFERENCES `ordenes_de_despacho` (`codigo`);
ALTER TABLE `items_de_despacho` ADD CONSTRAINT `producto_id_refs_codigo_9cb3a496` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`codigo`);
COMMIT;


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
