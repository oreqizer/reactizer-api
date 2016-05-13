drop table if exists todos;
create table entries (
  id integer primary key autoincrement,
  text text not null
);