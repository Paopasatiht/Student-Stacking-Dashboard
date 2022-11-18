select * 
from Enrollment as e, Stacking as stk, Students as s, Skill_Types as skill
where e.stack_id = stk.stack_id and e.student_id = s.student_id and stk.skill_id = skill.skill_id;

#View foe admin
#4 main views which is All student information, All courses and its skill,
#All lectuerer and their affiliation, Company information

#1. All student information
select s.student_id, s.student_fName, s.student_lName, s.age, s.gender, s.email, s.preference, 
u.uni_id, u.uni_name, u.uni_department, u.uni_program
from Students s, University u
where s.uni_id = u.uni_id;




#2 All courses and its skill
select c.course_id as CourseID, c.course_name as Course, s.skill_id as SkillID, 
t.skill_name as Skill, t.skill_type as Skill_Type, t.skill_score as Skill_Score
from Courses c, Stacking s, Skill_Types t 
where c.course_id = s.course_id and s.skill_id = t.skill_id;

#3 All lectuerer and their affiliation
select l.*, c.course_id, c.course_name,u.uni_department, u.uni_program, u.uni_name
from Lecturer l, Lecturer_Courses lc, University u, Courses c
where l.uni_id = u.uni_id and l.lecturer_id = lc.lecturer_id and lc.course_id = c.course_id;

#4 Company information
select *
from Company;