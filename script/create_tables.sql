create table raw_email (id INT, date DATETIME, mime_type TEXT, from_addr TEXT, to_addr TEXT, subject TEXT, body TEXT, path TEXT, label INT, PRIMARY KEY(id));
create table thread (id INT, date DATETIME, from_address TEXT, to_address TEXT, cc_address TEXT, subject TEXT, body TEXT, label INT, PRIMARY_KEY(id));
create table cleaned_email (id INT, date DATETIME, mime_type TEXT, from_addr TEXT, to_addr TEXT, subject TEXT, body TEXT, path TEXT, label INT, PRIMARY KEY(id));

create table brushed_email_full (id INT NOT NULL AUTO_INCREMENT, date DATETIME, mime_type TEXT, from_addr TEXT, to_addr TEXT, subject TEXT, raw_body TEXT, body TEXT, all_lines TEXT, one_line TEXT, path TEXT, label INT, PRIMARY KEY(id));

create table brushed_email_more (id INT NOT NULL AUTO_INCREMENT, date DATETIME, mime_type TEXT, from_addr TEXT, to_addr TEXT, subject TEXT, raw_body TEXT, body TEXT, all_lines TEXT, one_line TEXT, path TEXT, label INT, prediction INT, PRIMARY KEY(id));