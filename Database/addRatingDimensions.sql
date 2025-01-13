INSERT INTO rating_dimensions (id, name, description, created_at)
VALUES 
    (1, 'difficulty', 'How challenging the course content is to understand', NOW()),
    (2, 'workload', 'The amount of effort and time required for assignments and preparation', NOW()),
    (3, 'grading_fairness', 'Whether grading criteria are fair and transparent', NOW()),
    (4, 'lecture_quality', 'How engaging and clear the lectures are', NOW()),
    (5, 'practicality', 'The real-world applicability of the course content', NOW()),
    (6, 'instructor_support', 'How approachable and helpful the instructor is', NOW()),
    (7, 'resources', 'The quality and usefulness of provided materials, such as slides or textbooks', NOW()),
    (8, 'exam_difficulty', 'How hard the exams and assessments are', NOW()),
    (9, 'flexibility', 'How manageable the schedule and course requirements are', NOW());
