




INSERT INTO `users` (`username`,`password_hash`, `email`, `role`, `firstName`, `lastName`, `dob`, `location`) VALUES
    ('admin1', 'f96ccfe70a319f69019876d2be895235e7ee5d2b5f21dd51c6aa189b275acddf', 'admin1@example.com', 'admin', "Jack", "Adam", "2000-05-07", "Lincoln"),
    ('moderator1', 'b5ce5123ce0ccf4542807db003fec1c15bdfe4673d36ee1d78cc87cd6907cf51', 'moderator1@example.com', 'moderator', "Jesse", "Smith", "1987-06-14", "Lincoln"),
    ('moderator2', '3e5bfcdba74fa42f55d5c855ade31bc46ff2106d02faa62700e30f7fac6b7e62', 'moderator2@example.com', 'moderator', "Jack", "Watson", "1996-02-26", "Lincoln"),
    ('member1', 'd4a02dad3813e40a57db961445eae89e1ecc87cd5dc024b2c640221be92c8281', 'member1@example.com', 'member', "Sam", "Jackson", "1972-01-13", "CHCH"),
    ('member2', 'cf3782b6c0154365fab797b3916d1c3c4053f4e82a62c8c41152d0ec07f077ed', 'member2@example.com', 'member', "Tim", "Hank", "1979-12-15","NZ"),
    ('user3', 'hashed_password3', 'user3@example.com', 'member', 'Alice', 'Johnson', '1990-03-03', 'Location3'),
    ('user4', 'hashed_password4', 'user4@example.com', 'member', 'Bob', 'Williams', '1975-04-04', 'Location4'),
    ('user5', 'hashed_password5', 'user5@example.com', 'member', 'Charlie', 'Brown', '1982-05-05', 'Location5'),
    ('user6', 'hashed_password6', 'user6@example.com', 'member', 'David', 'Miller', '1992-06-06', 'Location6'),
    ('user7', 'hashed_password7', 'user7@example.com', 'member', 'Eve', 'Davis', '1987-07-07', 'Location7'),
    ('user8', 'hashed_password8', 'user8@example.com', 'member', 'Frank', 'Garcia', '1995-08-08', 'Location8'),
    ('user9', 'hashed_password9', 'user9@example.com', 'member', 'Grace', 'Martinez', '1991-09-09', 'Location9'),
    ('user10', 'hashed_password10', 'user10@example.com', 'member', 'Hank', 'Rodriguez', '1983-10-10', 'Location10');



INSERT INTO messages (title, content, created_at, user_id) VALUES
    ('Leaf Problems', 'My neighbor’s tree drops leaves all over my yard. Any advice?', '2024-07-01 08:23:45', 7),
    ('Root Damage', 'Roots from my neighbor’s tree are damaging my driveway. What can I do?', '2024-07-01 09:11:30', 8),
    ('Blocked Views', 'My neighbor’s hedge is blocking my view. Can I ask them to trim it?', '2024-07-01 10:05:15', 6),
    ('Tree Diseases', 'How can I tell if my tree is diseased and needs to be removed?', '2024-07-01 11:42:50', 6),
    ('Tree Preservation', 'I want to preserve an old tree in my backyard. Any tips?', '2024-07-01 12:33:05', 9),
    ('Tree Trimming', 'How often should I trim my hedges?', '2024-07-01 13:27:20', 6),
    ('Tree Types', 'What are the best types of trees to plant in a small garden?', '2024-07-01 14:14:55', 7),
    ('Falling Branches', 'A branch from my neighbor’s tree fell and damaged my car. Who is responsible?', '2024-07-01 15:18:40', 8),
    ('Tree Laws', 'Are there any local laws regarding tree maintenance?', '2024-07-01 16:22:10', 9),
    ('Hedge Maintenance', 'How do I maintain a hedge to keep it healthy and looking good?', '2024-07-01 17:05:25', 10),
    ('Tree Removal', 'When is it necessary to remove a tree?', '2024-07-02 08:15:30', 7),
    ('Tree Growth', 'My tree isn’t growing as fast as it should. Any ideas why?', '2024-07-02 09:47:55', 8),
    ('Planting Trees', 'What is the best time of year to plant a new tree?', '2024-07-02 10:53:10', 10),
    ('Watering Trees', 'How often should I water my trees?', '2024-07-02 11:38:25', 12),
    ('Tree Fertilizer', 'What kind of fertilizer is best for trees?', '2024-07-02 12:29:40', 11),
    ('Pruning Trees', 'Is there a specific time of year I should prune my trees?', '2024-07-02 13:21:15', 8),
    ('Tree Identification', 'How can I identify the type of tree in my yard?', '2024-07-02 14:05:30', 7),
    ('Tree Safety', 'My tree looks like it might fall over. What should I do?', '2024-07-02 15:45:50', 8),
    ('Tree Roots', 'Are tree roots dangerous to my house foundation?', '2024-07-02 16:33:10', 9),
    ('Tree Lighting', 'Can I use decorative lights on my tree without damaging it?', '2024-07-02 17:22:35', 10),
    ('Tree Mulching', 'How should I mulch around my tree for best results?', '2024-07-03 08:05:50', 11);


INSERT INTO replies (content, user_id, message_id, created_at) VALUES
    ('You might want to talk to your neighbor about it. Sometimes a simple conversation can solve the issue.', 5, 1, '2024-07-01 08:30:20'),
    ('Consider installing a leaf guard or barrier to prevent leaves from entering your yard.', 3, 1, '2024-07-01 08:45:10'),
    ('You might need to consult a professional to assess the damage and possible solutions.', 4, 2, '2024-07-01 09:25:55'),
    ('If the roots are on your property, you might be able to trim them, but check local laws first.', 6, 2, '2024-07-01 09:40:40'),
    ('Politely ask your neighbor if they would be willing to trim the hedge. If they refuse, check local regulations.', 5, 3, '2024-07-01 10:20:30'),
    ('You might have legal recourse if the hedge violates local ordinances.', 7, 3, '2024-07-01 10:35:15'),
    ('Look for signs like discolored leaves, abnormal growth, or insect infestation.', 9, 4, '2024-07-01 11:50:45'),
    ('A certified arborist can diagnose tree diseases and suggest treatment options.', 6, 4, '2024-07-01 12:05:20'),
    ('Avoid heavy pruning, provide adequate water, and use mulch to preserve tree health.', 8, 5, '2024-07-01 12:45:30'),
    ('Consult with a tree preservation expert to ensure the best care for your old tree.', 10, 5, '2024-07-01 13:00:00');




