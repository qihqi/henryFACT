create table productos (
    nombre varchar(200) not null,
    precio decimal(20, 2) not null,
    codigo varchar(20) primary key,
    cantidad int not null
);

create table usuarios (
    username varchar(50) primary key,
    password varchar(200) not null,
    is_admin boolean not null,
    last_factura bigint not null
);

create table clientes (
    codigo varchar(20) primary key,
    nombres varchar(100) not null,
    apellidos varchar(100) not null,
    direccion varchar(300) not null,
    ciudad varchar(50) not null,
    tipo varchar(1) not null,
    cliente_desde date not null
);

create table notas_de_venta (
    codigo bigint primary key auto_increment,
    vendedor varchar(50) not null,
    cliente varchar(20) not null,
    tiempo date not null
);

alter table notas_de_venta add 
    foreign key (vendedor) references usuario(username);
alter table notas_de_venta add 
    foreign key (cliente) references clientes(codigo);

create table items_de_venta (
    codigo_venta bigint not null,
    item_no int not null,
    cantidad int not null,
    codigo_prod varchar(50) not null,
    primary key (codigo_venta, item_no) 
);
    
alter table items_de_venta add 
    foreign key (codigo_venta) references notas_de_venta(codigo);
alter table items_de_venta add 
    foreign key (item_no) references productos(codigo);

create table factura (
    codigo bigint primary key,
    cajero varchar(50) not null,
    cliente varchar(20) not null,
    tiempo date not null,
    forma_pago varchar(1) not null,
    total decimal(20, 2) not null
);
alter table factura add 
    foreign key (cajero) references usuario(username);
alter table factura add 
    foreign key (cliente) references clientes(codigo);

create table items_de_factura (
    codigo_factura bigint not null,
    item_no int not null,
    cantidad int not null,
    codigo_prod varchar(50) not null,
    precio decimal(50, 2) not null,
    primary key (codigo_factura, item_no)
);
alter table items_de_factura add 
    foreign key (codigo_factura) references factura(codigo);
alter table items_de_factura add 
    foreign key (item_no) references productos(codigo)
/*
    foreign key (cajero) references usuario(username),
    foreign key (cliente) references clientes(codigo)
    foreign key (codigo_factura) references factura(codigo),
    foreign key (item_no) references productos(codigo)
    constraint fk_ventas foreign key (codigo_venta) references notas_de_venta(codigo),
    constraint fk_vent_prod foreign key (item_no) references productos(codigo)
    */
