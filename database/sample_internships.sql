-- Sample Data Insertion Script for InternHub
-- Run this script in your Supabase SQL Editor to populate 4 Companies and 10 Realistic Internships.

-- 1. Create Sample Company Accounts
INSERT INTO users (id, name, email, password_hash, role)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'TechCorp Solutions', 'hr@techcorp.com', 'scrypt:32768:8:1$dummyhash1', 'company'),
    ('22222222-2222-2222-2222-222222222222', 'InnovateAI Labs', 'careers@innovateai.io', 'scrypt:32768:8:1$dummyhash2', 'company'),
    ('33333333-3333-3333-3333-333333333333', 'CloudScale Systems', 'jobs@cloudscale.net', 'scrypt:32768:8:1$dummyhash3', 'company'),
    ('44444444-4444-4444-4444-444444444444', 'CyberShield Security', 'recruiting@cybershield.org', 'scrypt:32768:8:1$dummyhash4', 'company')
ON CONFLICT (email) DO NOTHING;

-- 2. Insert 10 Detailed Internship Postings
INSERT INTO internships (company_id, title, description, requirements, location, stipend)
VALUES 
(
    '11111111-1111-1111-1111-111111111111',
    'Full-Stack Python & Flask Engineer Intern',
    'Assist our core engineering team in developing modular RESTful APIs and modern web applications using Flask, Supabase, and JavaScript.',
    'Proficiency in Python, HTML5, CSS3, JavaScript. Familiarity with relational databases (PostgreSQL/MySQL) and Git.',
    'Remote',
    '$1,800 / month'
),
(
    '22222222-2222-2222-2222-222222222222',
    'AI & Machine Learning Research Intern',
    'Work alongside senior AI scientists to train transformer models, evaluate dataset pipelines, and integrate PyTorch models into production microservices.',
    'Strong background in Python, NumPy, PyTorch or TensorFlow. Understanding of Machine Learning fundamentals and linear algebra.',
    'San Francisco, CA',
    '$2,400 / month'
),
(
    '33333333-3333-3333-3333-333333333333',
    'Cloud DevOps & Infrastructure Intern',
    'Help automate cloud deployments using Docker, Kubernetes, and Terraform on AWS and Render infrastructure pipelines.',
    'Basic knowledge of Linux administration, Bash scripting, Docker containers, and CI/CD concepts.',
    'Austin, TX',
    '$2,000 / month'
),
(
    '44444444-4444-4444-4444-444444444444',
    'Cybersecurity & Network Analyst Intern',
    'Perform security audits, inspect vulnerability reports, analyze network traffic logs, and help implement SOC compliance policies.',
    'Understanding of networking protocols (TCP/IP, HTTP/S), Linux tools, and basic security concepts (OWASP Top 10).',
    'Washington, D.C.',
    '$1,750 / month'
),
(
    '11111111-1111-1111-1111-111111111111',
    'Frontend React & UI Engineer Intern',
    'Collaborate with designers to build sleek, accessible user interfaces, component libraries, and responsive web layouts.',
    'Solid knowledge of JavaScript (ES6+), React, CSS Flexbox/Grid, and responsive UI design principles.',
    'Remote',
    '$1,600 / month'
),
(
    '22222222-2222-2222-2222-222222222222',
    'Data Analytics & Business Intelligence Intern',
    'Transform complex raw datasets into actionable business insights and intuitive visual dashboards using Python and SQL.',
    'Strong SQL skills, Python data analysis tools (Pandas/Matplotlib), and interest in business metrics.',
    'New York, NY',
    '$1,900 / month'
),
(
    '33333333-3333-3333-3333-333333333333',
    'Mobile Application Development Intern (iOS / Android)',
    'Participate in building high-performance cross-platform mobile apps using Flutter or React Native.',
    'Experience with Flutter/Dart or React Native. Knowledge of REST APIs and mobile app lifecycles.',
    'Seattle, WA',
    '$2,100 / month'
),
(
    '44444444-4444-4444-4444-444444444444',
    'QA Automation & Testing Engineer Intern',
    'Write automated unit and end-to-end testing suites using Pytest and Selenium to ensure software quality.',
    'Basic programming skills in Python or Java, familiarity with software testing methodologies.',
    'Remote',
    '$1,500 / month'
),
(
    '11111111-1111-1111-1111-111111111111',
    'Associate Product Management Intern',
    'Gather user feedback, draft feature requirement documents, track sprint roadmaps, and work across tech and design teams.',
    'Excellent written and verbal communication, analytical mindset, and passion for tech products.',
    'Chicago, IL',
    '$1,850 / month'
),
(
    '22222222-2222-2222-2222-222222222222',
    'UI/UX Design Systems Intern',
    'Create Figma design systems, conduct user interviews, build interactive prototypes, and iterate on visual branding.',
    'Proficiency in Figma, user-centered design principles, and wireframing.',
    'Boston, MA',
    '$1,700 / month'
);
