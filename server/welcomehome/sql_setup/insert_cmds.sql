insert into role(roleid,rdescription) values ('1','Staff');
insert into role(roleid,rdescription) values ('2','Volunteer');
insert into role(roleid,rdescription) values ('3','Client');
insert into role(roleid,rdescription) values ('4','Donor');

insert into Category(mainCategory,subCategory,catNotes) values
    ('Electronics','Kitchen','Kitchen Electronics'),
    ('Electronics','Others','General Electronics'),
    ('Furniture','Dining','Furniture related to Dining'),
    ('Furniture','Hall','Furniture related to Hall'),
    ('Furniture','Bedroom','Furniture related to Bedroom'),
    ('Furniture','Others','General Furniture'),
    ('Clothing','Menswear','Mens Clothing'),
    ('Clothing','Womenswear','Womens Clothing'),
    ('Books','Academic','Academic Books'),
    ('Books','Novels','Leisure Books'),
    ('Uncategorized','Uncategorized','A Special Category for Items that cannot be categorized');

insert into Location(roomNum,shelfNum,shelf,shelfDescription) values
    (101,1,'1','1st Floor, Room 101, Shelf 1'),
    (101,2,'2','1st Floor, Room 101, Shelf 2'),
    (101,3,'3','1st Floor, Room 101, Shelf 3'),
    (102,1,'1','1st Floor, Room 102, Shelf 1'),
    (102,2,'2','1st Floor, Room 102, Shelf 2'),
    (201,1,'1','2nd Floor, Room 201, Cupboard'),
    (202,1,'1','2nd Floor, Room 202, Left Cupboard'),
    (202,2,'2','2nd Floor, Room 202, Right Cupboard');

