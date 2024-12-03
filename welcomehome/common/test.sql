INSERT INTO person(userName,password,fname,lname,email) VALUES ('${userName}','${password}','${fname}','${lname}','${email}');

UPDATE person SET userName='${userName}', password='${password}', fname='${fname}', lname='${lname}', email='${email}' WHERE userName='${userName}';