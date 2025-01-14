INSERT INTO rating_dimensions (id, name, description, created_at)
VALUES 
    (1, 'difficulty', 'How challenging the course content is to understand', NOW()),
    (2, 'workload', 'The amount of effort and time required for assignments and preparation', NOW()),
    (3, 'grading', 'Whether grading criteria are fair and transparent', NOW()),
    (4, 'lecture_quality', 'How engaging and clear the lectures are', NOW());
